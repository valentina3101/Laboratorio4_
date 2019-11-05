
from paquete import *
from constantes import *
from network import *
from socket import *

def create_socket(): #crea socket
	servidor = socket(AF_INET, SOCK_DGRAM)
	servidor.bind((RECEPTOR_IP,RECEPTOR_PORT))
	return servidor

def extract(paquete): #extrae paquete
    data= paquete.get_datos() # get datos (funcion definida) desde paquete.py 
    return data

def deliver_data(message): #envia los datos
	print(message)

def rdt_rcv(socket): #recive paquete
	data = socket.recv(2048) 
	emisor,paquete = loads(data) #descomprime
	return (emisor,paquete)
	

def corrupto(paquete):
	if calcular_checksum(paquete) == 0:
		return True
	else:
		return False


def make_pkt(data): #crea el paquete
	#atributos de la clase paquete (origen,destino,datos,secuencia)
	paquete = Paquete(RECEPTOR_PORT , EMISOR_PORT, data,0)
	resultado = calcular_checksum(paquete) #calcula checksum 
	paquete.set_checksum(resultado) #lo modifica al checksum
	return paquete


def udt_send(socket,emisor,paquete): # envia paquete
	datos = dumps((emisor,paquete)) #Comprimimos los datos
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

	secuencia=0
	while True:
		emisor, paquete=rdt_rcv(servidor)# Recibimos un paquete de la red
		print (emisor,paquete)
		if corrupto(paquete) ==0: #si esta corrupto el paquete que recibe
			print (1)
			emisor = (EMISOR_IP,EMISOR_PORT)
			pkt = make_pkt("NAK") #crea paquete con el mensaje de que esta corrupto
			udt_send(servidor,emisor,pkt) # y lo envia (para que se lo reenvien)
		else: #si no esta corrupto
			#print (1)
			emisor = (EMISOR_IP,EMISOR_PORT) 
			#print (2)
			pkt2 = make_pkt("ACK") #crea el paquete como ack (significa que le llego bien)
			#print (3)
			data= extract(paquete)# Extrae los datos
			deliver_data(data)# Entregamos los datos a la capa de aplicacion
			udt_send(servidor,emisor,pkt2) #los envia a la red y al emisor
			secuencia = (secuencia + 1) // 2 # suma uno a la secuencia para esperar el proximo
	close_socket(servidor)
