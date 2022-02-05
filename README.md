# Overview
A collection of old telemetry projects that are no longer active, but are preserved for future reference.

# Projects
## EagleBrain2
The code that ran on the old (Pre-Torch) telemetry module. This module consisted of an ESP32 which polled and relayed sensor data and a Raspberry Pi which recorded and transmitted this data. DARREL is the code that ran on the ESP32, polling all of the sensors and sending that via serial to the RasPi. DART is the code which ran on the RasPi. It reads the live flight data from serial and then records it in a txt and transmits it via radio. FAAP processes the sensor data to determine extra measurements (like altitude) and plots it. The origins of the acronyms are unknown. FlightData hold raw telemetry data from past flights

## GUI2
The graphical utility which allows for the in-browser visualization of recorded flight data. Consists of an HTML file for visual layout and JS file to extract and graph data from flight logs.

## PythonServer
The original (but never used) code for a Client-Server ground station system. Much of the code was written by visiting members.

## TUI
"Textual User Interface" A live visualization tool for flight data. Python files contain code which resembles that of DART as it also reads, unpacks, and records data from the serial bus. In this case, the computer reads the data from a USB radio transceiver. 