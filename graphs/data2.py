import serial
import matplotlib.pyplot as plt
from collections import deque
import numpy as np

# ------------------- CONFIGURATION -------------------
PORT = "/dev/cu.usbmodem101"       # Update this to your actual port
BAUD = 115200
MAX_SAMPLES = 100   # Window size for the time-series graph

# ------------------- SERIAL SETUP -------------------
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Connected to {PORT}...")
except:
    print(f"Error: Could not open {PORT}. Check connection.")
    exit()

# ------------------- DATA STORAGE -------------------
# We only need deque for the Atmospheric concentrations (Time Series)
pm1_data  = deque(maxlen=MAX_SAMPLES)
pm25_data = deque(maxlen=MAX_SAMPLES)
pm10_data = deque(maxlen=MAX_SAMPLES)

# We don't need history for particle counts, just the current snapshot
particle_counts = [0] * 6
particle_labels = ['>0.3µm', '>0.5µm', '>1.0µm', '>2.5µm', '>5.0µm', '>10µm']

# ------------------- VISUALIZATION SETUP -------------------
plt.style.use('dark_background') # Looks professional and better for FPV/Outdoor monitors
fig = plt.figure(figsize=(12, 8))
grid = plt.GridSpec(2, 2, height_ratios=[2, 1])

# --- TOP PLOT: Time Series (Concentration) ---
ax_ts = fig.add_subplot(grid[0, :])
line_pm1,  = ax_ts.plot([], [], color='#00FFFF', linewidth=1, label='PM 1.0 (Ultra-fine)')
line_pm25, = ax_ts.plot([], [], color='#FFD700', linewidth=2, label='PM 2.5 (Standard)')
line_pm10, = ax_ts.plot([], [], color='#FF4500', linewidth=1, label='PM 10 (Coarse)')

ax_ts.set_title("Live Air Quality Concentration (Atmospheric)", fontsize=14, color='white')
ax_ts.set_ylabel("Concentration (µg/m³)")
ax_ts.legend(loc='upper left')
ax_ts.grid(True, linestyle='--', alpha=0.3)
ax_ts.set_xlim(0, MAX_SAMPLES)
ax_ts.set_ylim(0, 50) # Initial scale, will auto-adjust

# --- BOTTOM LEFT: Live Dashboard Text ---
ax_text = fig.add_subplot(grid[1, 0])
ax_text.axis('off')
text_pm25 = ax_text.text(0.5, 0.6, "00", ha='center', va='center', fontsize=60, color='#FFD700')
text_label = ax_text.text(0.5, 0.3, "PM 2.5 µg/m³", ha='center', va='center', fontsize=12, color='gray')
text_aqi = ax_text.text(0.5, 0.1, "Initializing...", ha='center', va='center', fontsize=14, color='white')

# --- BOTTOM RIGHT: Particle Size Spectrum (Bar Chart) ---
ax_bar = fig.add_subplot(grid[1, 1])
bars = ax_bar.bar(particle_labels, [1]*6, color='#00FF00', alpha=0.7)
ax_bar.set_title("Instantaneous Particle Count Spectrum", fontsize=10)
ax_bar.set_yscale('log') # Log scale is crucial because 0.3um counts are usually 1000x higher than 10um
ax_bar.set_ylim(1, 10000)

plt.tight_layout()
plt.ion() # Interactive mode on

# ------------------- HELPER: AQI ESTIMATOR -------------------
def get_aqi_status(pm25):
    if pm25 <= 12: return "Good", '#00FF00'
    elif pm25 <= 35.4: return "Moderate", '#FFFF00'
    elif pm25 <= 55.4: return "Unhealthy for Sensitive", '#FF7E00'
    elif pm25 <= 150.4: return "Unhealthy", '#FF0000'
    else: return "Hazardous", '#800080'

# ------------------- MAIN LOOP -------------------
x_vals = np.arange(0, MAX_SAMPLES)

while True:
    try:
        line = ser.readline().decode("ascii", errors="ignore").strip()
        if not line: continue

        values = line.split(",")
        if len(values) != 12: continue
        values = [float(v) for v in values]

        # Unpack based on PMS5003 Protocol
        # We ignore indices 0-2 (Standard) and focus on 3-5 (Atmospheric)
        pm1_atm_val  = values[3]
        pm25_atm_val = values[4]
        pm10_atm_val = values[5]
        
        # Indices 6-11 are particle counts
        current_counts = values[6:12]

        # --- UPDATE DATA BUFFERS ---
        pm1_data.append(pm1_atm_val)
        pm25_data.append(pm25_atm_val)
        pm10_data.append(pm10_atm_val)

        # --- UPDATE TIME SERIES PLOT ---
        # We need to construct x-arrays that match the current length of the deque
        curr_len = len(pm1_data)
        x_data = np.arange(MAX_SAMPLES - curr_len, MAX_SAMPLES)
        
        line_pm1.set_data(x_data, pm1_data)
        line_pm25.set_data(x_data, pm25_data)
        line_pm10.set_data(x_data, pm10_data)
        
        # Dynamic Y-Axis scaling (keeps the graph readable if pollution spikes)
        current_max = max(pm10_data) if pm10_data else 10
        ax_ts.set_ylim(0, max(20, current_max * 1.2))

        # --- UPDATE DASHBOARD TEXT ---
        status, status_color = get_aqi_status(pm25_atm_val)
        text_pm25.set_text(f"{int(pm25_atm_val)}")
        text_pm25.set_color(status_color)
        text_aqi.set_text(f"Status: {status}")
        text_aqi.set_color(status_color)

        # --- UPDATE BAR CHART ---
        for bar, height in zip(bars, current_counts):
            # Avoid log(0) errors by ensuring min height is 1
            bar.set_height(max(1, height))

        plt.pause(0.01)

    except KeyboardInterrupt:
        print("Monitoring Stopped.")
        ser.close()
        break
    except Exception as e:
        print(f"Error: {e}")
