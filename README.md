# Air Quality Monitoring RC Aircraft Platform
### ASME @ UCSD | 2024-2025 Capstone Project

![Project Status](https://img.shields.io/badge/Status-In_Development-yellow)
![Platform](https://img.shields.io/badge/Platform-ArduPilot-blue)
![Language](https://img.shields.io/badge/Data_Processing-Python-green)

---

## 📖 Project Overview
This repository hosts the source code, CAD assets, and system architecture documentation for the **ASME UCSD Air Quality Monitoring Aircraft**. 

This project involves the design and development of a remote-controlled fixed-wing aircraft engineered to collect atmospheric air quality data. Operating at higher altitudes than standard ground stations, this platform enables broader regional sampling to support air quality assessment in regions affected by wildfires and other environmental events.

<div align="center">
  <img src="images/cad_render.png" alt="Aircraft CAD Design" width="80%">
  <p><em>Final Airframe Design: Plywood Fuselage with Foam Wings</em></p>
</div>

---

## 📂 Repository Structure

| Folder | Description |
| :--- | :--- |
| `/CAD` | SolidWorks/STEP files for the fuselage, wings, and sensor housing. |
| `/Avionics` | Wiring diagrams, pinout sheets, and ArduPilot parameter files. |
| `/Software` | (In Progress) Python scripts for data extraction and logging. |
| `/Docs` | Technical reports, posters, and presentation slides. |

---

## 🚀 System Architecture

### 1. The Airframe (Structural)
The aircraft is designed for stability and consistent sensor exposure.
* **Fuselage:** Lightweight Birch Plywood for structural rigidity and ease of manufacturing.
* **Wing Airfoil:** **Clark Y** (Selected for predictable lift and gentle stall characteristics at low speeds).
* **Empennage:** **NACA 0008** (Symmetrical shape for balanced control authority).
* **Sensor Housing:** Custom integrated static air chamber to minimize turbulence and ensure accurate sampling.

### 2. Avionics & Hardware
* **Flight Controller:** MATEKSYS Wing v2 F405
* **Firmware:** ArduPilot (Plane)
* **Air Quality Sensor:** PMS5003 (PM2.5/PM10 concentration)
* **Telemetry:** 915MHz / 433MHz Telemetry Radio
* **FPV:** 5.8 GHz Camera system

### 3. Software & Data Flow
The system utilizes a Ground Control Station (GCS) loop for real-time monitoring, with a planned post-flight processing suite.

1.  **Data Collection:** PMS5003 captures particulate data $\rightarrow$ Logged via FC.
2.  **Transmission:** MAVLink stream sends data to Mission Planner via Telemetry.
3.  **Processing:** Python scripts (Currently in development) will parse flight logs.
4.  **Visualization (Goal):** The final objective is to overlay this data onto a digital map, creating a heat map of pollution concentration zones relative to GPS coordinates.

<div align="center">
  <img src="images/system_diagram.png" alt="System Block Diagram" width="80%">
</div>

---

## 📍 Project Roadmap & Future Goals

We are currently in the **Flight Testing & Data Analysis** phase. 

### ✅ Completed
* Airframe CAD design and manufacturing.
* Avionics integration and wiring.
* Basic sensor data logging via ArduPilot.

### 🚧 In Progress / Future Goals
* **Map Visualization Tool:** We are currently developing a Python-based tool to extract geolocation and sensor data from ArduPilot logs (`.tlog` or `.bin`) and generate a visual heat map.
* **Data Validation:** Comparing airborne sensor data against standard ground-station metrics to ensure accuracy.
* **Full Autonomous Flight:** Optimizing waypoint navigation for grid-based air

--

**ASME @ UCSD**

---

## 📜 License & Acknowledgments
* Developed for the ASME UCSD Chapter Engineering Project.
* Based on ArduPilot open-source firmware.
