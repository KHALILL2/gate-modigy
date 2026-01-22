import requests
import RPi.GPIO as GPIO
import time

API_URL = "https://batu-gate-production.abdullah.top/api/v1/gate/check-access"
  # REPLACE THIS!

RELAY_PINS = [14, 15]
ACTIVE_HIGH = True  # Change to False if active LOW works in test

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW if ACTIVE_HIGH else GPIO.HIGH)  # Safe OFF state

def open_gate(duration=5):
    print("? Gate Opening... (Both relays activated)")
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.HIGH if ACTIVE_HIGH else GPIO.LOW)  # Activate
    time.sleep(duration)
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.LOW if ACTIVE_HIGH else GPIO.HIGH)  # Deactivate
    print("? Gate Closed")

def start_scanner():
    print("Gate System Active - Connected to Production API")
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    while True:
        try:
            scanned_code = input("Scan: ").strip()
            if not scanned_code: continue

            payload = {"bar_code": scanned_code}
            response = requests.post(API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("allowed") == True:
                    name = data["data"].get("student", {}).get("name", "Student")
                    print(f"? WELCOME! {data.get('message', '')}")
                    print(f"   {name}")
                    open_gate(duration=5)
                else:
                    print("? Access Denied")
            else:
                print(f"? Error: {response.text}")
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        start_scanner()
    finally:
        for pin in RELAY_PINS:
            GPIO.output(pin, GPIO.LOW if ACTIVE_HIGH else GPIO.HIGH)  # Safe OFF
        GPIO.cleanup()