import serial
import struct
from collections import namedtuple
import json

DARREL = serial.Serial('COM3',115200)
STRUCT_SIZE = 56 # see ESP code for struct
MAGIC = 0xBEEFF00D

DARRELData_struct = struct.Struct('< I f f f f f f f f f d d') # 1 int 9 floats and 2 doubles
labels = [
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
]

import logging
from websocket_server import WebsocketServer

def new_client(client, server):
    while True:
        packet_b = DARREL.read(STRUCT_SIZE)
        packet_s = DARRELData_struct.unpack(packet_b)
        data = dict(zip(labels,packet_s))
        if data['magic'] != MAGIC:
            print('INVALID MAGIC')
            DARREL.read(1)
        else: server.send_message_to_all(json.dumps(data))

server = WebsocketServer(host='127.0.0.1', port=12345, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             packet_b = DARREL.read(STRUCT_SIZE)
#             packet_s = DARRELData_struct.unpack(packet_b)
#             data = DARRELData(*packet_s)
#             if data.magic != MAGIC:
#                 print('INVALID MAGIC')
#                 DARREL.read(1)
#             print(data)
