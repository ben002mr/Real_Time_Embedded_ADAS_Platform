# Real-Time Embedded ADAS Platform

## Driver Monitoring and Forward Collision Warning System using Raspberry Pi

A real-time embedded Advanced Driver Assistance System (ADAS) prototype developed using Raspberry Pi, computer vision, ultrasonic sensing, serial communication, and embedded electronics.

This project combines:
- Driver Drowsiness Detection
- Forward Collision Warning (FCW)
- Real-Time Embedded Processing
- Hardware-Software Integration
- System Monitoring and Logging

The platform continuously monitors:
- driver eye state
- vehicle obstacle distance
- system performance metrics

and generates:
- visual alerts
- buzzer alerts
- system logs
- real-time console outputs

---

# Project Objectives

The objective of this project is to design a low-cost embedded ADAS prototype capable of:

- Detecting driver drowsiness in real time
- Monitoring obstacle distance using ultrasonic sensing
- Generating warning and danger alerts
- Demonstrating embedded hardware/software co-design
- Performing real-time edge AI processing on Raspberry Pi

---

# Features

## Driver Monitoring System
- Face detection using OpenCV Haar Cascades
- Eye detection for drowsiness monitoring
- Drowsiness state classification:
  - ALERT
  - EYES_CLOSED
  - DROWSY
  - NO_FACE

## Forward Collision Warning (FCW)
- Ultrasonic distance measurement
- Real-time collision risk estimation
- Warning states:
  - SAFE
  - WARNING
  - DANGER

## Embedded Alert System
- Green LED → Safe state
- Yellow LED → Warning state
- Red LED → Danger state
- Buzzer alerts for warning/danger conditions

## Real-Time Monitoring
- FPS monitoring
- CPU usage monitoring
- CSV telemetry logging
- Console-based live system visualization

---

# Hardware Used

| Component | Purpose |
|---|---|
| Raspberry Pi 3B+ | Main embedded computing platform |
| Raspberry Pi Camera Module | Driver monitoring |
| HC-SR04 Ultrasonic Sensor | Distance measurement |
| NodeMCU ESP8266 | Embedded FCW controller |
| LEDs | Visual alert indicators |
| Buzzer | Audio warning system |
| Breadboard + Jumper Wires | Circuit connections |

---

# Software Stack

| Technology | Purpose |
|---|---|
| Python | Main ADAS application |
| OpenCV | Computer vision |
| Picamera2 | Raspberry Pi camera interface |
| PySerial | Serial communication |
| Arduino IDE | NodeMCU firmware development |
| Embedded C/C++ | FCW controller firmware |

---

# System Architecture

```text
Raspberry Pi Camera
        ↓
Driver Monitoring System
(OpenCV Eye Detection)
        ↓
Driver State Classification
        ↓
Serial Communication
        ↓
NodeMCU FCW Controller
        ↓
Ultrasonic Distance Detection
        ↓
LED + Buzzer Alerts