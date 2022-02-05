from collections import namedtuple
from datetime import datetime
import struct
import time

import serial
radio = serial.Serial('/dev/ttyUSB0', 9600)
DARREL = serial.Serial('/dev/ttyUSB1', 115200)

STRUCT_SIZE = 56 # see ESP code for struct
MAGIC = 0xBEEFF00D
mode = 'normal'
DARRELData_struct = struct.Struct('< I f f f f f f f f f d d') # 1 int 9 floats and 2 doubles
DARRELData = namedtuple('DARRELData', [
    'magic',
    'time',
    'latitude',
    'longitude',
    'altitude',
    'accx',
    'accy',
    'accz',
    'mA',
    'V',
    'temp',
    'pressure'
])

# check that the ports are correct
time.sleep(0.5)
while DARREL.in_waiting <= 0:
    print("SWAPPING PORTS")
    DARREL = serial.Serial('/dev/ttyUSB0', 115200)
    radio = serial.Serial('/dev/ttyUSB1', 9600)
    time.sleep(1)

if mode == 'debug':
    # just pretty prints out datapoints we are getting from the esp
    print('DEBUG MODE')
    try:
        while True:
            packet_b = DARREL.read(STRUCT_SIZE)
            packet_s = DARRELData_struct.unpack(packet_b)
            data = DARRELData(*packet_s)
            if packet_named.magic != MAGIC:
                print('INVALID MAGIC')
                DARREL.read(1)
            print(data)
    except KeyboardInterrupt:
        DARREL.close()
        radio.close()
elif mode == 'normal':
    # collects data from the esp, saves it to a file locally, and transmits it to the ground
    print('NORMAL MODE')
    date = datetime.now().isoformat()
    f = open(f'flightData-{date}.txt', 'w')
    try:
        while True:
            packet_b = DARREL.read(STRUCT_SIZE)
            packet_s = DARRELData_struct.unpack(packet_b)
            packet_named = DARRELData(*packet_s)
            if packet_named.magic != MAGIC:
                print('INVALID MAGIC')
                DARREL.read(1)
            print('read')
            # dump to file
            packet_string = ' '.join([str(v) for v in packet_s])
            f.write(packet_string + '\n')
            print('recorded')
            # send over radio
            sent = radio.write(packet_b)
            if sent != STRUCT_SIZE:
                print('failed to send to radio!')
            print('sent')
            time.sleep(.1)
    except KeyboardInterrupt:
        f.close()
        DARREL.close()
        radio.close()
