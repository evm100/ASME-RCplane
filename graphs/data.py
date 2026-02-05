import serial
import matplotlib.pyplot as plt
from collections import deque

# ------------------- CONFIGURATION -------------------
PORT = "COM3"
BAUD = 115200
N = 100

# ------------------- SERIAL SETUP -------------------
ser = serial.Serial(PORT, BAUD, timeout=1)

# ------------------- DATA DEQUES -------------------
pm1_std   = deque(maxlen=N)
pm25_std  = deque(maxlen=N)
pm10_std  = deque(maxlen=N)

pm1_atm   = deque(maxlen=N)
pm25_atm  = deque(maxlen=N)
pm10_atm  = deque(maxlen=N)

p03 = deque(maxlen=N)
p05 = deque(maxlen=N)
p10 = deque(maxlen=N)
p25 = deque(maxlen=N)
p50 = deque(maxlen=N)
p100 = deque(maxlen=N)

datasets = [
    pm1_std, pm25_std, pm10_std,
    pm1_atm, pm25_atm, pm10_atm,
    p03, p05, p10,
    p25, p50, p100
]

titles = [
    "PM1.0 Std", "PM2.5 Std", "PM10 Std",
    "PM1.0 Atm", "PM2.5 Atm", "PM10 Atm",
    ">0.3 µm", ">0.5 µm", ">1.0 µm",
    ">2.5 µm", ">5.0 µm", ">10 µm"
]

colors = [
    'b','g','r','b','g','r',
    'c','m','y','k','orange','purple'
]

# ------------------- MATPLOTLIB SETUP -------------------
plt.ion()
fig, axes = plt.subplots(4, 3, figsize=(15, 12))
fig.subplots_adjust(hspace=0.8, wspace=0.4)
axes = axes.flatten()

lines = []

for ax, color, title in zip(axes, colors, titles):
    line, = ax.plot([], [], color=color)
    ax.set_title(title)
    ax.set_xlabel("Samples")
    if "PM" in title:
        ax.set_ylabel("µg/m³")
    else:
        ax.set_ylabel("counts / 0.1 L")
    ax.set_xlim(0, N)
    lines.append(line)

# ------------------- MAIN LOOP -------------------
while True:
    try:
        line = ser.readline().decode("ascii", errors="ignore").strip()
        if not line:
            continue

        values = line.split(",")
        if len(values) != 12:
            continue

        values = [float(v) for v in values]

        (
            pm1s, pm25s, pm10s,
            pm1a, pm25a, pm10a,
            v03, v05, v10, v25, v50, v100
        ) = values

        # Append data
        pm1_std.append(pm1s)
        pm25_std.append(pm25s)
        pm10_std.append(pm10s)

        pm1_atm.append(pm1a)
        pm25_atm.append(pm25a)
        pm10_atm.append(pm10a)

        p03.append(v03)
        p05.append(v05)
        p10.append(v10)
        p25.append(v25)
        p50.append(v50)
        p100.append(v100)

        # Update plots (NO CLEARING)
        for line_obj, data in zip(lines, datasets):
            x = range(len(data))
            line_obj.set_xdata(x)
            line_obj.set_ydata(data)

            # Auto-scale Y only
            ax = line_obj.axes
            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True)

        plt.pause(0.01)

    except KeyboardInterrupt:
        print("Exiting...")
        break
