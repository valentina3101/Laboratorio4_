
from paquete import *
from constantes import *
from network import *

def create_socket(): #crea socket
	servidor = socket(AF_INET, SOCK_DGRAM)
	servidor.bind((RECEPTOR_IP,RECEPTOR_PORT))
	return servidor

def extract(paquete): #extrae paquete
    data=paquete.get_data()
    return data

def rdt_rcv(socket): #recive paquete
	data = socket.recv(2048) 
	emisor,paquete = loads(data) #comprime
	return (emisor,paquete)
	

def corrupto(paquete):
	if calcular_checksum(paquete)  == 0:
		return True
	else:
		return False


def make_pkt(receptor,emisor,datos, secuencia): #crea el paquete
	paquete = Paquete(RECEPTOR_PORT , EMISOR_PORT, datos,0)
	resultado = calcular_checksum(paquete)
	paquete.set_checksum(resultado)
	return paquete


def udt_send(emisor,paquete): # envia paquete
	datos = dumps(emisor,confirmacion) #Comprimimos los datos
	socket.sendto(datos,(NETWORK_IP,NETWORK_PORT)) # envia dato a la red
	return (datos)


def close_socket(socket, signal, frame):
	print ("\n\rCerrando socket")
	socket.close()
	exit(0)

if __name__ == "__main__":
	servidor= create_socket()# Creamos el socket "receiver"
	# Registramos la senial de salida
	signal.signal(signal.SIGINT, partial(close_socket, servidor))
	print ("listo para recibir mensajes..")# Imprimimos el cartel "Listo para recibir mensajes..."
	while True:
		secuencia=0
		paquete=rdt_rcv(servidor)# Recibimos un paquete de la red
		if rdt_rcv(paquete) and corrupto(paquete):
			udt_send("NAK")
		if rdt_rcv(paquete) and not corrupto(paquete):
			print ("llegando")
			data=extract(paquete,data)# Extraemos los datos
			deliver_data(data)# Entregamos los datos a la capa de aplicacion
			paquete = make_pkt("ACK",get_checksum())
			udt_send(paquete)
			secuencia = (secuencia + 1) // 2
	close_socket(servidor)
