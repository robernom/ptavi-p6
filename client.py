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
    if MET.upper() == "INVITE":
        message = ("INVITE sip:" + NAME + " SIP/2.0\r\n")
    elif MET.upper() == "BYE":
        message = ("BYE sip:" + NAME + " SIP/2.0\r\n")
    my_socket.send(bytes(message, 'utf-8'))
    try:
        data = my_socket.recv(1024).decode('utf-8')
    except ConnectionRefusedError:
        sys.exit("No se puede conectar al servidor")
    expected = "SIP/2.0 100 Trying\r\nSIP/2.0 180 Ring\r\nSIP/2.0 200 OK\r\n\r\n"
    if data == expected:
        message = ("ACK sip:" + NAME + " SIP/2.0\r\n")
        my_socket.send(bytes(message, 'utf-8'))