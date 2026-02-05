import serial
import time
import csv
import statistics

# --- CONFIGURATION ---
SERIAL_PORT = 'COM3'      # CHANGE THIS to your Arduino's port
BAUD_RATE = 115200          # Match your Arduino's Serial.begin()
PM25_INDEX = 1            # Which item in the comma list is PM2.5? (0-based)
FILENAME = 'rooms.csv'
DURATION = 10             # Seconds to record

def collect_room_data():
    room_name = input("Enter name of the room (e.g., 'Kitchen'): ")
    
    print(f"Connecting to {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Give connection a moment to settle
    except serial.SerialException:
        print(f"Error: Could not open {SERIAL_PORT}. Check your connection.")
        return

    readings = []
    start_time = time.time()
    
    print(f"Collecting data for {DURATION} seconds...")
    
    # Flush existing buffer so we get fresh data
    ser.reset_input_buffer()

    while (time.time() - start_time) < DURATION:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                parts = line.split(',')
                
                # Check if we have enough data columns
                if len(parts) > PM25_INDEX:
                    val = float(parts[PM25_INDEX])
                    readings.append(val)
                    # Optional: Print live dots to show activity
                    print(".", end="", flush=True)
            except ValueError:
                continue # Skip malformed lines

    ser.close()
    print("\nDone.")

    if readings:
        avg_pm25 = statistics.mean(readings)
        print(f"Average PM2.5 for {room_name}: {avg_pm25:.2f}")
        
        # Append to file
        with open(FILENAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([room_name, round(avg_pm25, 2)])
        print(f"Saved to {FILENAME}")
    else:
        print("No valid data received. Check Arduino output format.")

if __name__ == "__main__":
    collect_room_data()
