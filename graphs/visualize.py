import matplotlib.pyplot as plt
import csv
import os

FILENAME = 'rooms.csv'

def get_aqi_color(value):
    # EPA PM2.5 Breakpoints
    if value <= 12: return '#00e400'    # Green
    elif value <= 35.4: return '#ffff00' # Yellow
    elif value <= 55.4: return '#ff7e00' # Orange
    elif value <= 150.4: return '#ff0000' # Red
    else: return '#8f3f97'               # Purple

def visualize():
    if not os.path.exists(FILENAME):
        print(f"No data file found ({FILENAME}). Run collect.py first.")
        return

    rooms = []
    values = []

    # Read data from file
    with open(FILENAME, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row: # Skip empty lines
                rooms.append(row[0])
                values.append(float(row[1]))

    if not rooms:
        print("File is empty.")
        return

    # Setup colors
    colors = [get_aqi_color(v) for v in values]

    # Create Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(rooms, values, color=colors, edgecolor='black')

    # Styling
    ax.set_ylabel('PM2.5 Concentration ($\mu g/m^3$)')
    ax.set_title('Home Air Quality Survey')
    ax.axhline(y=12, color='green', linestyle='--', alpha=0.5, label='Good Air Limit')

    # Add labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height}', ha='center', va='bottom')

    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize()
