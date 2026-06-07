# Real-Time Digital Twin Sensor Data Logger

## Overview

This project simulates an industrial process tank in MATLAB/Simulink and streams real-time sensor telemetry to a Python-based monitoring dashboard using TCP/IP communication.

The system acts as a simple Digital Twin by simulating process dynamics, generating virtual sensor data, transmitting measurements over a network connection, visualizing them in real time, and logging all data for further analysis.

---

## Features

### Simulated Sensors

The Simulink model generates realistic sensor measurements including:

- Tank Level Sensor (m)
- Pressure Sensor (Pa)
- Temperature Sensor (°C)
- Flow Sensor (m³/s)

---

### Real-Time TCP/IP Communication

The simulation continuously transmits sensor data from Simulink to Python using TCP/IP sockets.

Data is transmitted as:

- 64-bit floating point values
- Little-endian byte order
- Continuous real-time stream

---

### Python Telemetry Dashboard

The Python application:

- Receives live telemetry data
- Displays real-time sensor values
- Continuously updates trend graphs
- Provides visualization similar to a lightweight SCADA system

Graphs include:

1. Tank Level
2. Pressure
3. Temperature
4. Flow Rate

---

### Data Logging

All incoming sensor measurements are automatically stored in:

```text
sensor_log.csv
```

The CSV file contains:

| Timestamp | Level | Pressure | Temperature | Flow |
|------------|------------|------------|------------|------------|

This data can later be imported into:

- MATLAB
- Excel
- Python
- Power BI
- Tableau

for further analysis.

---

## System Architecture

```text
+--------------------+
| Simulink Plant     |
| Simulation         |
+----------+---------+
           |
           |
           v
+--------------------+
| Virtual Sensors    |
| Level              |
| Pressure           |
| Temperature        |
| Flow               |
+----------+---------+
           |
           |
           v
+--------------------+
| TCP/IP Send Block  |
+----------+---------+
           |
           |
           v
+--------------------+
| Python TCP Server  |
+----------+---------+
           |
     +-----+-----+
     |           |
     v           v
CSV Logger   Live Dashboard
```

---

## Technologies Used

### MATLAB / Simulink

Used for:

- Process simulation
- Sensor modeling
- Dynamic system behavior
- TCP/IP communication

### Python

Used for:

- Socket programming
- Data acquisition
- Real-time plotting
- CSV data logging

### Libraries

```bash
pip install matplotlib numpy
```

---

## Project Structure

```text
project/
│
├── sensor_logger.py
├── sensor_log.csv
├── simulink_model.slx
├── README.md
└── screenshots/
```

---

## Running the Project

### Step 1

Start the Python dashboard:

```bash
python sensor_logger.py
```

---

### Step 2

Run the Simulink model.

---

### Step 3

Observe:

- Live telemetry values
- Real-time graphs
- Automatic CSV generation

---

## Example Telemetry Output

```text
Level=4.412 m
Pressure=433.364 Pa
Temp=27.934 C
Flow=0.50000 m3/s
```

---

## Learning Outcomes

This project demonstrates:

- Digital Twin fundamentals
- Industrial sensor simulation
- TCP/IP networking
- Real-time telemetry acquisition
- Data visualization
- Process monitoring
- Engineering data logging
- MATLAB–Python integration

---

## Future Improvements

Potential extensions include:

- PID control implementation
- Alarm management
- MQTT communication
- OPC-UA integration
- Database storage
- Web dashboard
- Predictive maintenance analytics
- Machine learning-based fault detection

---

## Author

Smruti Ranjan Mishra

Electronics and Instrumentation Engineering

Real-Time Industrial Digital Twin and Telemetry Monitoring Project
