import RPi.GPIO as GPIO
from time import sleep

# Single relay pin
RELAY_PIN = 23  # GPIO 17 (physical pin 11)

# Set to True if relay activates on LOW (most common 5V modules)
# Set to False if it activates on HIGH
ACTIVE_LOW = True

GPIO.setmode(GPIO.BCM)      # Use BCM numbering
GPIO.setwarnings(False)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Start in safe OFF state
if ACTIVE_LOW:
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # OFF
else:
    GPIO.output(RELAY_PIN, GPIO.LOW)   # OFF

print("RPi.GPIO Relay Toggle Test")
print(f"ACTIVE_LOW = {ACTIVE_LOW}")
print("Relay toggles every 1 second. Press Ctrl+C to stop.\n")

try:
    while True:
        # HIGH state
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Pin ? HIGH")
        sleep(1)

        # LOW state
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Pin ? LOW")
        sleep(1)

except KeyboardInterrupt:
    print("\nTest stopped.")

finally:
    # Safe shutdown
    if ACTIVE_LOW:
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
    print("Relay OFF and GPIO cleaned up.")