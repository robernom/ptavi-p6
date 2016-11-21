#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):
    """SIP server class."""

    def handle(self):
        """Cada vez que un cliente envia una peticion se ejecuta."""
        data = self.rfile.read().decode('utf-8')
        allowed = ["INVITE", "ACK", "BYE"]
        print(data)
        met = data.split()[0]
        c_ip = self.client_address[0]
        to_send = ""
        if met == "INVITE":
            to_send = ("SIP/2.0 100 Trying\r\n\r\nSIP/2.0 180 Ring\r\n\r\n" +
                       "SIP/2.0 200 OK\r\n\r\n")
        elif met == "BYE":
            to_send = "SIP/2.0 200 OK\r\n\r\n"
        elif met == "ACK":
            os.system("./mp32rtp -i " + c_ip + " -p 23032 <" + SONG)
        elif met not in allowed:
            to_send = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
        else:
            to_send = "SIP/2.0 400 Bad Request\r\n\r\n"
        if to_send != "":
            self.wfile.write(bytes(to_send, 'utf-8'))

if __name__ == "__main__":
    # Creamos servidor y escuchamos
    try:
        IP, PORT, SONG = sys.argv[1:]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 server.py IP port audio_file")
    SERV = socketserver.UDPServer((IP, int(PORT)), SIPHandler)
    print("Listening...")
    try:
        SERV.serve_forever()
    except KeyboardInterrupt:
        sys.exit("\r\nClosed")
