import time
import csv
import datetime
from pymavlink import mavutil

# --- CONFIGURATION ---
# Connect to the UDP port forwarded by Mission Planner
# source_system=255 means we act as a GCS (Ground Control Station)
CONNECTION_STRING = 'udpin:127.0.0.1:14550'
LOG_FILENAME = f'air_quality_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def main():
    print(f"Connecting to {CONNECTION_STRING}...")
    # Create the connection
    master = mavutil.mavlink_connection(CONNECTION_STRING)

    # Open CSV file for logging
    with open(LOG_FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Timestamp', 'Lat', 'Lon', 'Alt_m', 'PM2_5', 'Message_Type'])
        print(f"Logging data to {LOG_FILENAME}")

        # Variables to hold the latest data (so we can sync them)
        current_lat = None
        current_lon = None
        current_alt = None
        
        # Wait for a heartbeat before sending commands
        print("Waiting for heartbeat...")
        master.wait_heartbeat()
        print("Heartbeat received! Listening for data...")

        while True:
            try:
                # Receive the next message
                msg = master.recv_match(blocking=True)
                if not msg:
                    continue

                # Handle GPS / Position Data
                if msg.get_type() == 'GLOBAL_POSITION_INT':
                    # ArduPilot sends lat/lon as integers (degrees * 1e7)
                    current_lat = msg.lat / 1e7
                    current_lon = msg.lon / 1e7
                    current_alt = msg.relative_alt / 1000.0 # Convert mm to meters

                # Handle Air Quality Data
                # ArduPilot sends Air Quality as a 'NAMED_VALUE_FLOAT'
                # The name field will usually contain "DustDensity" or "AQ_PM25"
                if msg.get_type() == 'NAMED_VALUE_FLOAT':
                    # Decode the name field (it comes as bytes)
                    try:
                        name = msg.name.replace('\x00', '') # Clean null bytes
                    except:
                        name = str(msg.name)

                    # Check if this is the dust sensor
                    # Adjust 'DustDensity' based on what you see in the console print below
                    if 'Dust' in name or 'AQ' in name:
                        pm_value = msg.value
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Print to console
                        print(f"[{timestamp}] Lat:{current_lat} Lon:{current_lon} Alt:{current_alt} | {name}: {pm_value}")
                        
                        # Write to CSV
                        writer.writerow([timestamp, current_lat, current_lon, current_alt, pm_value, name])
                        file.flush() # Ensure data is written immediately

            except KeyboardInterrupt:
                print("\nStopping log...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    main()
