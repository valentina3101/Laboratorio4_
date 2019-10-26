import math

class Paquete:
    def __init__(self, origen, destino, datos, secuencia):
        self.origen     = origen
        self.destino    = destino
        self.checksum   = 0
        self.longitud   = len(datos) + 8
        self.datos      = datos
        self.secuencia  = secuencia

    def set_checksum(self, new_checksum):
        self.checksum = new_checksum

    def get_origen(self):
        return self.origen

    def get_destino(self):
        return self.destino

    def get_longitud(self):
        return self.longitud

    def get_checksum(self):
        return self.checksum

    def get_datos(self):
        return self.datos

    def get_secuencia(self):
        return self.secuencia


def complemento_uno(number):
    num_bits = int(math.log2(number)) + 1
    complemento = ((0b1 << num_bits) - 1) ^ number
    return complemento

def calcular_checksum(packet):
    sum_aux = packet.get_origen() + packet.get_destino()
    sum_aux += packet.get_longitud() + packet.get_checksum()
    resultado = complemento_uno(sum_aux)
    return resultado



