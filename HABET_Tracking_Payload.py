# HABET Basic Tracking Payload CircuitPython Script
# Recieves GPS data and transmits it via LoRa radio module
# Utilizes Adafruit Feather M4 Express, Ultimate GPS FeatherWing, RFM95W 433 MHz FeatherWing
# Last updated 9/2/2020 by Austin Trask

import time
import board
import busio
import digitalio
import analogio
import adafruit_rfm9x

# Device ID
FEATHER_ID = b'1'

print("startup")

# For monitoring battery voltage
vbat_voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)

# Define CS pin for RFM95W LoRa
CS = digitalio.DigitalInOut(board.D10)

# Initialize SPI bus for RFM95W LoRa
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Define radio frequency
RADIO_FREQ_MHZ = 433.0

# Define RESET pin
RESET = digitalio.DigitalInOut(board.D11)

# Initialize LoRa Radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Set transmit power (to maximum)
rfm9x.tx_power = 23

# Define RX and TX pins for the GPS
RX = board.RX
TX = board.TX

# Set the UART serial connection for the GPS module
uart = busio.UART(TX, RX, baudrate=9600, timeout=1)

# Define the send message function
def sendMessage(message):
    try:
        # Measures battery voltage and formats it to transmit
        battery_voltage = get_voltage(vbat_voltage)
        v = "{:.2f}".format(battery_voltage)
        rfm9x.send(FEATHER_ID+b','+message+',V,'+v)
    except:
        print("Message failed to send")

# Define the get voltage function
def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

current = time.monotonic()
old = current
newGPS = False

while True:
    current = time.monotonic()
    
    # Checks for new GPS data
    if uart.in_waiting > 0:
        gps_string = uart.readline()
        print(gps_string)
        if "GPGGA" in gps_string:
            gps_str = str(gps_string)
            newGPS = True
            
    # Sends GPS data every 5 seconds (or 5 times whatever your later sleep value is)
    if current-old>5:
        old = current
        if newGPS:
            print(gps_str)
            sendMessage(gps_str)
            newGPS = False
        else:
            # Message for if there is no GPS
            sendMessage("No GPS")
            print("No GPS")
            
    # Pauses for 1 second before restaring the cycle
    time.sleep(.1)
