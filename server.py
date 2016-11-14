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
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            # Si no hay más líneas salimos del bucle infinito
            print("El cliente nos manda " + line.decode('utf-8'))
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            
            

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
