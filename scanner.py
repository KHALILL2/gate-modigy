import requests
import serial
from time import sleep

# --------------------- CONFIG ---------------------
API_URL = "https://batu-gate-production.abdullah.top/api/v1/gate/check-access"

# Serial port - usually /dev/ttyACM0 or /dev/ttyUSB0
# Check with: ls /dev/tty*  (before and after plugging Arduino)
SERIAL_PORT = "/dev/ttyUSB0"   # Change to /dev/ttyUSB0 if needed
BAUD_RATE = 9600

# Open duration on Arduino side (must match Arduino delay)
GATE_OPEN_SECONDS = 5
# --------------------------------------------------

print("Connecting to Arduino...")
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    sleep(2)  # Wait for Arduino reset
    ser.flushInput()
    ser.flushOutput()
    print(ser.readline().decode().strip())  # Should print "Arduino Dual Relay Ready"
except Exception as e:
    print(f"Failed to connect to Arduino on {SERIAL_PORT}: {e}")
    print("Check cable and port name (ls /dev/tty*)")
    exit(1)

def open_gate():
    print("? Sending OPEN command to Arduino... (Both relays will activate)")
    ser.write(b"OPEN\n")
    # Optional: wait for confirmation
    while True:
        line = ser.readline().decode().strip()
        if line:
            print(f"   Arduino: {line}")
        if "Gate Closed" in line:
            break

def start_scanner():
    print("\nGate System Active - Connected to Production API & Arduino Dual Relays")
    print("Waiting for barcode scan...\n")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    while True:
        try:
            scanned_code = input("Scan: ").strip()
            if not scanned_code:
                continue

            payload = {"bar_code": scanned_code}
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("allowed") == True:
                    name_en = data["data"].get("student", "Student")
                    name_ar = data["data"].get("????? ???????", "")
                    welcome_msg = data.get("message", "Welcome! Entry recorded successfully")

                    print(f"? {welcome_msg}")
                    if name_ar:
                        print(f"   {name_en} - {name_ar}")
                    else:
                        print(f"   {name_en}")

                    open_gate()  # Arduino activates BOTH relays
                else:
                    print("? Access Denied (allowed: false)")
            else:
                try:
                    error_detail = response.json()
                    print(f"? API Error: {error_detail}")
                except:
                    print(f"? HTTP {response.status_code}: {response.text}")

        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        start_scanner()
    finally:
        ser.close()
        print("Serial connection closed.")
