
import socket
import struct
import csv
import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# TCP CONFIGURATION

HOST = '127.0.0.1'
PORT = 5005

# 4 float64 values = 32 bytes
PACKET_SIZE = 32

# Little-endian 4 doubles
FORMAT = '<dddd'

# CSV LOGGING

csv_filename = "sensor_log.csv"

csv_file = open(csv_filename, mode='w', newline='')

csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "Time (s)",
    "Level (m)",
    "Pressure (Pa)",
    "Temperature (C)",
    "Flow (m3/s)"
])

# SOCKET SETUP

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)
print("Waiting for Simulink connection...")
conn, addr = server.accept()
print(f"Connected by {addr}")

# DATA STORAGE

MAX_POINTS = 300
time_data = deque(maxlen=MAX_POINTS)
level_data = deque(maxlen=MAX_POINTS)
pressure_data = deque(maxlen=MAX_POINTS)
temp_data = deque(maxlen=MAX_POINTS)
flow_data = deque(maxlen=MAX_POINTS)
start_time = time.time()

# RECEIVE EXACT PACKET SIZE

def recv_exact(sock, size):

    data = b''

    while len(data) < size:

        packet = sock.recv(size - len(data))

        if not packet:
            return None

        data += packet

    return data


# MATPLOTLIB FIGURE
fig, axs = plt.subplots(4, 1, figsize=(12, 12))
fig.suptitle("Real-Time Digital Twin Telemetry Dashboard")

# UPDATE FUNCTION

def update(frame):

    raw = recv_exact(conn, PACKET_SIZE)

    if raw is None:
        print("Connection closed")
        return

    try:

        # Decode telemetry packet
        level, pressure, temp, flow = struct.unpack(FORMAT, raw)

        current_time = time.time() - start_time

        # PRINT LIVE VALUES

        print(
            f"Level={level:.3f} m | "
            f"Pressure={pressure:.3f} Pa | "
            f"Temp={temp:.3f} C | "
            f"Flow={flow:.5f} m3/s"
        )

        # SAVE CSV

        csv_writer.writerow([
            current_time,
            level,
            pressure,
            temp,
            flow
        ])

        csv_file.flush()
        # STORE GRAPH DATA
        time_data.append(current_time)
        level_data.append(level)
        pressure_data.append(pressure)
        temp_data.append(temp)
        flow_data.append(flow)

        # CLEAR OLD PLOTS

        for ax in axs:
            ax.clear()

        # LEVEL GRAPH

        axs[0].plot(time_data, level_data)
        axs[0].set_title("Tank Level")
        axs[0].set_ylabel("Level (m)")
        axs[0].set_xlabel("Time (s)")
        axs[0].legend(["Level"])
        axs[0].grid(True)

        # PRESSURE GRAPH
        
        axs[1].plot(time_data, pressure_data)
        axs[1].set_title("Pressure Sensor")
        axs[1].set_ylabel("Pressure (Pa)")
        axs[1].set_xlabel("Time (s)")
        axs[1].legend(["Pressure"])
        axs[1].grid(True)
    
        # TEMPERATURE GRAPH

        axs[2].plot(time_data, temp_data)
        axs[2].set_title("Temperature Sensor")
        axs[2].set_ylabel("Temperature (C)")
        axs[2].set_xlabel("Time (s)")
        axs[2].legend(["Temperature"])
        axs[2].grid(True)

        # FLOW GRAPH

        axs[3].plot(time_data, flow_data)
        axs[3].set_title("Pump Flow Rate")
        axs[3].set_ylabel("Flow (m3/s)")
        axs[3].set_xlabel("Time (s)")
        axs[3].legend(["Flow"])
        axs[3].grid(True)

        plt.tight_layout()

    except Exception as e:

        print("Error:", e)

# REAL-TIME ANIMATION

ani = animation.FuncAnimation(
    fig,
    update,
    interval=100
)

plt.show()

# CLEANUP

conn.close()
csv_file.close()

