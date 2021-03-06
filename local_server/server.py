# -*- coding: utf-8 -*-
import json
from math import *
import time

import httplib2
import bluetooth


def get_required_data(): # get the temperature and humidity data required from the client
	
	# from client (you need change it)
	temp = 23
	humi = 29
	return temp, humi
	



def main():
    temp, humi = get_required_data()
    bd_addr = "D4:36:39:D1:C3:C3" # EV3 Bluetooth Address
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    while(1):
        try:
            sock.connect((bd_addr, port))
            break
        except:
            continue

    temp = str(temp)
    sock.send(temp)
    while True:
        if sock.recv(1).decode('utf-8') == 'r': # if receive 'r', means robot has already get the temperature and humidity data, so stop send it
            print("ok")
            break

    while True:
        count = sock.recv(1).decode('utf-8')
        if count != '':
            h = httplib2.Http()
            change_position = h.request(
                uri='http://api.asnteam09.tk/locations',
                method='POST',
                headers={
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    'location_id': count,
                })
            )
    sock.close()
        

if __name__ == '__main__':
    main()
