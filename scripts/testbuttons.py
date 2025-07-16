#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define button pins for Waveshare 2.13 e-Paper HAT (BCM numbering)
BUTTON_PINS = {
    'Key1': 5,   # GPIO 5
    'Key2': 6,   # GPIO 6
    'Key3': 13,  # GPIO 13
    'Key4': 19   # GPIO 19
}

def button_callback(channel):
    """Callback function to handle button presses."""
    for key, pin in BUTTON_PINS.items():
        if channel == pin:
            logging.info(f"{key} (GPIO {pin}) pressed!")

try:
    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Configure each button pin as input with pull-up resistor
    for key, pin in BUTTON_PINS.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=200)
        logging.info(f"Monitoring {key} on GPIO {pin}")

    logging.info("Button test script running. Press any button (Key1-Key4) to test. Press Ctrl+C to exit.")
    
    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    logging.info("Exiting script...")
    
finally:
    GPIO.cleanup()  # Clean up GPIO resources
    logging.info("GPIO cleanup complete.")
