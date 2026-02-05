import serial
import matplotlib.pyplot as plt
import time

# ------------------- CONFIG -------------------
PORT = "COM3"
BAUD = 115200
DURATION = 10  # seconds

std_labels = ["PM1.0", "PM2.5", "PM10"]
atm_labels = ["PM1.0", "PM2.5", "PM10"]
count_labels = [">0.3", ">0.5", ">1.0", ">2.5", ">5.0", ">10"]

# ------------------- SERIAL -------------------
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.reset_input_buffer()

# Data buckets
pm_std = [[], [], []]
pm_atm = [[], [], []]
counts = [[] for _ in range(6)]

start = time.time()

# ------------------- COLLECT DATA -------------------
while time.time() - start < DURATION:
    line = ser.readline().decode("ascii", errors="ignore").strip()
    if not line:
        continue

    values = line.split(",")
    if len(values) != 12:
        continue

    try:
        values = [float(v) for v in values]
    except ValueError:
        continue

    (
        pm1s, pm25s, pm10s,
        pm1a, pm25a, pm10a,
        v03, v05, v10, v25, v50, v100
    ) = values

    pm_std[0].append(pm1s)
    pm_std[1].append(pm25s)
    pm_std[2].append(pm10s)

    pm_atm[0].append(pm1a)
    pm_atm[1].append(pm25a)
    pm_atm[2].append(pm10a)

    counts[0].append(v03)
    counts[1].append(v05)
    counts[2].append(v10)
    counts[3].append(v25)
    counts[4].append(v50)
    counts[5].append(v100)

ser.close()

# ------------------- AVERAGE -------------------
def avg(lst):
    return sum(lst) / len(lst) if lst else 0

std_avg   = [avg(x) for x in pm_std]
atm_avg   = [avg(x) for x in pm_atm]
count_avg = [avg(x) for x in counts]

# ------------------- PLOTTING -------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Std PM
axes[0].bar(std_labels, std_avg, color=["b", "g", "r"])
axes[0].set_title("PM Standard ("+ DURATION + " s avg)")
axes[0].set_ylabel("µg/m³")
axes[0].set_ylim(bottom=0)

# Atm PM
axes[1].bar(atm_labels, atm_avg, color=["b", "g", "r"])
axes[1].set_title("PM Atmospheric ("+ DURATION + " s avg)")
axes[1].set_ylabel("µg/m³")
axes[1].set_ylim(bottom=0)

# Particle counts
axes[2].bar(count_labels, count_avg, color="purple")
axes[2].set_title("Particle Counts ("+ DURATION + " s avg)")
axes[2].set_ylabel("counts / 0.1 L")
axes[2].set_ylim(bottom=0)

plt.tight_layout()
plt.show()

