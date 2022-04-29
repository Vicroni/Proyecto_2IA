# -*- coding: UTF-8 -*-
from Tablero import Tablero
from Tree import Tree
import math

class Heuristicas:
    def __init__(self, blancas):
        if blancas:
            self.yo = Tablero.BLANCO
            self.oponente = Tablero.NEGRO
        else:
            self.yo = Tablero.NEGRO
            self.oponente = Tablero.BLANCO


    #eval es usado así para evitar reconstruir la matriz cada quien, pero esta pensado con construirVariacion
    #Esta pensada para ser la suma entre los valores de las fichas descritos en la matriz construirVariacion y la movilidad.
    #Tab es el tablero a evaluar, eval está pensado para recibir la variable en donde se guarde construirVariacion para no reconstruir la matriz cada vez que se quiera
    #evaluar
    def heuristicaCanon(self,tab, eval):
        return self.movilidad(tab) + self.tableroEvaluacion(tab,eval)

    #Tab es el tablero a evaluar, cuenta directa del número de fichas del color propio que hay en el tablero
    def cuentaNormal(self, tab):
        cuenta = 0
        for x in tab.tablero:
            for y in x:
                if y[2] == self.yo:
                    cuenta += 1
        return cuenta

    #Tab es el tablero a evaluar, diferencia entre fichas propias y del contrincante.
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

    #Tab es el tablero a evaluar, eval es una matriz de 10 * 10 que asigna puntaje a cada casilla, de forma que el valor regresado es la suma de todas las
    #casillas en las que hay ficha del color propio.
    def tableroEvaluacion(self, tab, eval):
        cuenta = 0
        for x in tab.tablero:
            for y in x:
                if y[2] == self.yo:
                    cuenta += eval[y[0]][y[1]]
        return cuenta

    #Método que devuelve una matriz de evaluación con 1 en las casillas del centro, 3 en los bordes y 5 en las orillas.
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

    #Método que devuelve una matriz de evaluación, donde el valor de la casilla es la distancia de taxista al centro del tablero.
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

    #Tab es el tablero a evaluar, esta heuristica cuenta el número de tiradas validas que puede hacer el jugador en el tablero actual.
    def movilidad(self,tab):
        if self.yo == Tablero.BLANCO:
            return len(self.noDuplicados(Tree.generaPosiblesMovimiento(tab.tablero,True)))
        else:
            return len(self.noDuplicados(Tree.generaPosiblesMovimiento(tab.tablero,False)))

    #Método que devuelve una matriz de evaluación, basada en los valores propuestos en el siguiente paper: https://www.it.uc3m.es/jvillena/irc/practicas/07-08/Othello.pdf
    def construirVariacion(self):
        eval = [[] for y in range(10)]
        eval[0]=[0,0,0,0,0,0,0,0,0,0]
        eval[1]=[0,50,-1,5,2,2,5,-1,50,0]
        eval[2]=[0,-1,-5,1,1,1,1,-5,-1,0]
        eval[3]=[0,5,1,1,1,1,1,1,5,0]
        eval[4]=[0,2,1,1,1,1,1,1,2,0]
        eval[5]= eval[4]
        eval[6]= eval[3]
        eval[7]= eval[2]
        eval[8]= eval[1]
        eval[9]= eval[0]
        return eval
    
    #Función auxiliar para eliminar duplicados de una lista.
    def noDuplicados(self, list):
        newList = []
        for x in list:
            if x not in newList:
                newList.append(x)
        return newList
