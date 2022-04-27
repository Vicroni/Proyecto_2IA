from Tablero import Tablero
import math

class Heuristicas:
    def __init__(self, blancas):
        if blancas:
            self.yo = Tablero.BLANCO
            self.oponente = Tablero.NEGRO
        else:
            self.yo = Tablero.NEGRO
            self.oponente = Tablero.BLANCO

    def cuentaNormal(self, tab):
        cuenta = 0
        for x in tab.tablero:
            for y in x:
                if y[2] == self.yo:
                    cuenta += 1
        return cuenta

    def diferencia(self, tab):
        cuentaYo = 0
        cuentaOponente = 0
        for x in tab.tablero:
            for y in x:
                if y[2] == self.yo:
                    cuentaYo += 1
                if y[2] == self.oponente:
                    cuentaOponente +=1
        return cuentaYo - cuentaOponente

    def tableroEvaluacion(self, tab, eval):
        cuenta = 0
        for x in tab.tablero:
            for y in x:
                if y[2] == self.yo:
                    cuenta += eval[y[0]][y[1]]
        return cuenta

    def construirOrillasyEsquinas(self):
        eval = [[0 for x in range(10)] for y in range(10)]
        for y in range(10):
            for x in range(10):
                if x == 0 or x == 9 or y == 0 or y == 9: 
                    eval[y][x] = 0
                elif (x == 1 or x == 8) and (y == 1 or y == 8):
                    eval[y][x] = 5
                elif (x == 1 or x == 8 or y == 1 or y == 8):
                    eval[y][x] = 3
                elif (x > 1 and x < 8 and y > 1 and y < 8):
                    eval[y][x] = 1
        return eval

    def distanciaTaxi(self):
        eval = [[0 for x in range(10)] for y in range(10)]
        for y in range(10):
            for x in range(10):
                if x == 0 or x == 9 or y == 0 or y == 9:
                    eval[y][x] = 0
                else:
                    vdis = abs(y - 4.5)
                    hdis = abs(x - 4.5)
                    taxidis = math.floor(vdis + hdis)
                    eval[y][x] = taxidis
        return eval


h = Heuristicas(True)
tablero = Tablero()
print("Cuenta normal: {cuenta}".format(cuenta = h.cuentaNormal(tablero)))
print("Diferencia: {dif}".format(dif = h.diferencia(tablero)))
eval = h.construirOrillasyEsquinas()
for x in eval:
    print(x)
print("OrillasYEsquinas: {oye}".format(oye = h.tableroEvaluacion(tablero, eval)))
eval = h.distanciaTaxi()
for x in eval:
    print(x)
print("distanciaTaxi: {dT}".format(dT=h.tableroEvaluacion(tablero, eval)))