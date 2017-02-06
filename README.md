# Teslameter
gaussmeter/teslameter based on Honeywell SS495A Hall Sensor and Arduino Nano

Hardware:
  - Honewell SS495A Linear Hall Effect Sensor
  - Arduino Nano (Clone with CH340  Serial2USB-Chip)
  
## Version 1: Connected to PC via USB, Display in a Tkinter Gui.
### Hardware:  
SS495A driven by Arduino's 5V, output connected to A7. The Arduino-Sketch reads A7 and writes the values to serial with 9600 baud.

### Pyhton Tkinter Gui 
Reads serial values, calculates Milli-Tesla, updates the main label every 10 values with the mean of the last values, updates the line after every read.
The units - and with this the postions of the grid-lines - can be cycled between mT, Gauss, A/cm.

I package the app with Pyinstaller --onefile ...

## Version 2: 4-digit-7-segment display and battery in a box

4-digit-7-segment display connectd to arduino nano. Nano powered by 9V battery on Vin.
One switch for power.
One pushbutton for offset-canceling (zero)
