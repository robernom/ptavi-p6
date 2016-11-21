#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import socket
import sys
import os

os.system("clear")
try:
    MET = sys.argv[1]
    USER = sys.argv[2]
    NAME, PORT = USER.split(':')[0:]
    IP = NAME.split('@')[1]

except ValueError:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((IP, int(PORT)))
    print(MET.upper())
    message = (MET.upper() + " sip:" + NAME + " SIP/2.0\r\n")
    my_socket.send(bytes(message, 'utf-8'))
    try:
        data = my_socket.recv(1024).decode('utf-8')
        print(data)
    except ConnectionRefusedError:
        sys.exit("No se puede conectar al servidor")
    expect = data.split("\r\n\r\n")[0:-1]
    if expect == ["SIP/2.0 100 Trying", "SIP/2.0 180 Ring", "SIP/2.0 200 OK"]:
        message = ("ACK sip:" + NAME + " SIP/2.0\r\n")
        my_socket.send(bytes(message, 'utf-8'))
