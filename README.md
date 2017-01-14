# Teslameter
gaussmeter/teslameter based on Honeywell SS495A Hall Sensor, Arduino Nano and Tkinter Gui

## Hardware:
  - Honewell SS495A Linear Hall Effect Sensor
  - Arduino Nano (Clone with CH340  Serial2USB-Chip)
  

SS495A driven by Arduino's 5V, output connected to A7. The Arduino-Sketch reads A7, scales to mT and writes the values to serial with 9600 baud.

## Pyhton Tkinter Gui 
Reads serial values, updates the main label every 10 values with the mean of the last values, updates the line after every read.

I package the app with Pyinstaller --onefile ...
