import os 
from gps3 import gps3
from time import *

def get_coords():
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    sleep(10)
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            return (data_stream.TPV['lat'], data_stream.TPV['lon'])    

