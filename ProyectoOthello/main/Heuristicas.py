# -*- coding: UTF-8 -*-
import math

class Heuristicas:
    def __init__(self, blancas):
        self.evaluacion=[[0,0,0,0,0,0,0,0,0,0], [0,50,-1,5,2,2,5,-1,50,0], [0,-1,-5,1,1,1,1,-5,-1,0],[0,5,1,1,1,1,1,1,5,0], 
                   [0,2,1,1,1,1,1,1,2,0], [0,2,1,1,1,1,1,1,2,0], [0,5,1,1,1,1,1,1,5,0], [0,-1,-5,1,1,1,1,-5,-1,0], 
                   [0,50,-1,5,2,2,5,-1,50,0], [0,0,0,0,0,0,0,0,0,0]]
        if blancas:
            from Tree import Tree
            self.yo = Tree.BLANCO
            self.oponente = Tree.NEGRO
        else:
            from Tree import Tree
            self.yo = Tree.NEGRO
            self.oponente = Tree.BLANCO


    #eval es usado así para evitar reconstruir la matriz cada quien, pero esta pensado con construirVariacion
    #Esta pensada para ser la suma entre los valores de las fichas descritos en la matriz construirVariacion y la movilidad.
    #Tab es el tablero a evaluar, eval está pensado para recibir la variable en donde se guarde construirVariacion para no reconstruir la matriz cada vez que se quiera
    #evaluar
    def heuristicaCanon(self,tab):
        return self.tableroEvaluacion(tab,self.evaluacion)

    #Tab es el tablero a evaluar, cuenta directa del número de fichas del color propio que hay en el tablero
    def cuentaNormal(self, tab):
        cuenta = 0
        for x in tab:
            for y in x:
                if y[2] == self.yo:
                    cuenta += 1
        return cuenta

    #Tab es el tablero a evaluar, eval es una matriz de 10 * 10 que asigna puntaje a cada casilla, de forma que el valor regresado es la suma de todas las
    #casillas en las que hay ficha del color propio.
    def tableroEvaluacion(self, tab, eval):
        cuenta = 0
        for x in tab:
            for y in x:
                if y[2] == self.yo:
                    cuenta += eval[y[0]][y[1]]
        return cuenta
