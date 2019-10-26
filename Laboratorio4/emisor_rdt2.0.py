from constantes import *
from socket import *
from paquete import *

def create_socket():
	UDPsocket = socket(AF_INET, SOCK_DGRAM) # creo el socket protocolo de red IP, protocolo transporte UDP
	return UDPsocket


def rdt_send():
    data=input('ingrese un mensaje:  ')
    return(data.encode('utf-8'))


def make_pkt(data):
    pkt = Paquete(EMISOR_PORT , RECEPTOR_PORT, data, 0)
    cksum = calcular_checksum(pkt)
    pkt.set_checksum(cksum)
    return pkt  
	


def udp_send(socket, mensaje, receiver): #data y reciber
	mensaje=dumps((mensaje, receiver))
	socket.sendto(mensaje, (NETWORK_IP,NETWORK_PORT))#con esto mando a la red  



def close_socket(socket, signal, frame):
	print ("\n\rCerrando socket")
	socket.close()
	exit(0)


if __name__ == "__main__":

	cliente=create_socket() # Creamos el socket
	
	signal.signal(signal.SIGINT, partial(close_socket, cliente))#esta funcion toma el socketal final
    
	while True: # Iteramos indefinidamente
		data=rdt_send() # Leemos el mensaje desde teclado
		paquete=make_pkt(data) # Hacemos el paquete
		destinatario = (RECEPTOR_IP, RECEPTOR_PORT) # Establecemos el destinatario
		udp_send(cliente, paquete, destinatario) # Enviamos el mensaje
	close_socket(cliente)  
		
