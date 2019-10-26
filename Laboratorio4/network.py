#!/usr/bin/env python
# encoding: utf-8
"""
network.py
"""

from constantes import *

def recv_pckt(socket):
	data, emisor = socket.recvfrom(1024)
	receptor, pckt = loads(data)
	return emisor, receptor, pckt

def send_pckt(socket, emisor, receptor, pckt):
	data = dumps((emisor, pckt))
	socket.sendto(data, receptor)

def process_pkt(pckt):
	addrs = (pckt)
	return pckt, addrs

def shut_down(socket, signal, frame):
	socket.close()
	exit(0)

if __name__ == "__main__":
	# Creamos el socket para la red
	sock = socket(AF_INET, SOCK_DGRAM)
	# Lo ligamos a su direccion
	sock.bind((NETWORK_IP, NETWORK_PORT))
	# Registramos la senial de salida
	signal.signal(signal.SIGINT, partial(shut_down, sock))
	# Imprimimos mensaje
	print('Red Habilitada')
	while True:
		sender, receiver, pckt = recv_pckt(sock)
		send_pckt(sock, sender, receiver, pckt)

