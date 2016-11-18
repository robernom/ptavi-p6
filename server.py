#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os 

os.system("clear")


class SIPHandler(socketserver.DatagramRequestHandler):
    """
    SIP server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        """Cada vez que un cliente envia una peticion se ejecuta."""
        data = self.rfile.read().decode('utf-8')
        print(data)
        c_data = data.split()
        c_ip = self.client_address[0]
        met = c_data[0]
        if met == "INVITE":
        	self.wfile.write(b"SIP/2.0 100 Trying\r\n")
        	self.wfile.write(b"SIP/2.0 180 Ring\r\n")
        	self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif met == "BYE":
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif met == "ACK":
            print("Envio RTP")
            os.system("./mp32rtp -i " + c_ip +" -p 23032 < cancion.mp3")
        else:
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")

if __name__ == "__main__":
    # Creamos servidor y escuchamos
    try:
        IP, PORT, CANCION = sys.argv[1:]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 server.py IP port audio_file")
    serv = socketserver.UDPServer((IP, int(PORT)), SIPHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit("\r\nClosed")
