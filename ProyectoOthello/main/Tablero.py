# -*- coding: utf-8 -*-
from Tree import Tree
from Heuristicas import Heuristicas
import random
import time
import math
'''
Clase encargada de tener un control del tablero
que se muestra en pantalla, tambien controla y actualiza el arbol 
dependiendo de la jugadas en pantalla
'''
class Tablero:
    BLANCO  = Tree.BLANCO
    NEGRO   = Tree.NEGRO
    POSIBLE = Tree.POSIBLE
    FUTURA  = Tree.FUTURA


    #Inicializamos el tablero
    def __init__(self, dificultad):
        print("inicia __init__ Tablero")
        # Creamos la matriz de 8 x 8 x 3, veamos que cada casilla
        # de la matriz se representa como [x,y,v] donde x,y 
        # es la posicion de la casilla dentro del tablero 
        # v representa el valor de la casilla, es decir,
        # 1 = blanca, 2 = negra o 3 = posible
        self.tablero = [[[y,x,0]  for x in range(10)] for y in range(10)]
        # Turno esta representado por un booleano
        # Siempre empiezan las negras (FalseI)
        self.turno = False
        # Al azar decidimos a qué jugador (IA o humano) 
        # le toca iniciar (fichas negras)
        self.ia = random.random() <= 0.5
        # Colocamos las cuatro fichas iniciales
        self.tablero[4][5][2] = Tree.NEGRO
        self.tablero[5][5][2] = Tree.BLANCO
        self.tablero[5][4][2] = Tree.NEGRO
        self.tablero[4][4][2] = Tree.BLANCO
        # Evaluamos la dificultad
        if dificultad == "facil":
            self.profundidad = 2
        elif dificultad == "media":
            self.profundidad = 4
        else:
            self.profundidad = 6
        # Definimos los posibles movimientos del jugador que inicia
        print("__init__ Tablero ANTES colocaPosiblesMovimientos")
        self.colocaPosiblesMovimientos()
        print("__init__ Tablero DESPUES colocaPosiblesMovimientos")
        # Matriz de 10 x 10 que usaremos para la heurística.
        # Sus valores nunca cambian.
        self.evaluacion = Heuristicas.construirVariacion()
        # Posibles jugadas inmediatas de la IA, uno de estos es el mejor 
        # siguiente movimiento, son de la forma [estado, valor_heurístico]
        self.inmediatasEvaluadas = []
        
        # Si la IA inicia la partida (e.d, negras), generamos el árbol 
        # desde el tablero inicial y realizamos la mejor jugada posible
        if not self.ia:
            print(": : : : : > Inicia la IA < : : : : :")
            self.jugadaAutomatica()
            self.cambiarTurno()
            print(": : : : : > Turno del Humano < : : : : :")
            self.colocaPosiblesMovimientos()
        else: 
            print(": : : : : > Inicia el Humano < : : : : :")
        print("termina __init__ Tablero")

    def getTablero(self):
        return self.tablero
    
    def jugadaAutomatica(self):
        print("--> inicia jugadaAutomatica")
        # Como en InterfazTablero se generan los posibles movimiento
        # ya no es necesario generar el árbol de nevo
        # self.tree = Tree(self.tablero)
        # self.tree.generaHijos(self.profundidad, self.turno)
        print(" # # # # # # # # # # ")
        print(self.tree)
        if self.tree.children:
            for child in self.tree.children:
                print("Hijo")
                print(child)
                if child.children:
                    print("Nietos")
                    for grandChild in child.children:
                        print(grandChild)
        print(" # # # # # # # # # # ")
        # Calculamos minimax con poda alfa-beta
        print("\t antes minimax")
        valor = self.minimax(self.tree, self.profundidad, float('-inf'), float('inf'), self.ia)
        print("\t despues minimax")
        # Obtenemos el estado del tablero más favorable para la IA
        # junto con las coordenadas de la posición de la nueva ficha 
        siguiente, coordenadas = self.getJugada(valor)
        # Si hay diferencia entre el anterior y el siguiente movimiento
        # coloreamos la posición de la nueva ficha 
        if coordenadas:
            self.tablero[coordenadas[0]][coordenadas[1]][2] = 4
        # Esperamos un poco para que se note la posición de la nueva ficha
        print("\t jugadaAutomatica ANTES time.sleep(2)")
        time.sleep(2)
        print("\t jugadaAutomatica DESPUES time.sleep(2)")
        # Si hay diferencia nos quedamos con el tablero anterior.
        if siguiente:
            print("\t jugadaAutomatica Si hubo jugada siguiente")
            self.tablero = siguiente
        # Después de realizar la jugada, olvidamos las hojas previas.
        self.inmediatasEvaluadas = []
        Tree.limpiarPosiblesMovimientos(self.tablero)
        print("termina jugadaAutomatica <--")


    def getJugada(self, valor):
        print("\t--> inicia getJugada")
        mejor_jugada = []
        valores = []
        i = 0
        for n,v in self.inmediatasEvaluadas:
            if v == valor:
                valores.append(">" + str(v) + "< ")
                mejor_jugada = n
                i += 1
                print("\tgetJugada n " + str(i) + " \n" + self.imprimeValores(n))
            else:
                valores.append(str(v))
        print("\t".join(valores))
        coordenadas = self.posicionDiferente(mejor_jugada)
        print("\tNuevas posicion = " + str(coordenadas))
        print("\ttermina getJugada <--")
        return mejor_jugada, coordenadas


    def posicionDiferente(self, nueva):
        # Identifica la posicion diferente
        print("\t\t--> inicia posicionDiferente")
        coordenadas = []
        copia = [[[k for k in i] for i in j] for j in self.tablero]
        print("\t\tposicionDiferente DESPUES copia")
        Tree.limpiarPosiblesMovimientos(copia)
        print("\t\tcopia \n" + self.imprimeValores(copia))
        print("\t\tnueva \n" + self.imprimeValores(nueva))
        for i in range(8):
            for j in range(8):
                if (copia[j+1][i+1][2] != nueva[j+1][i+1][2]):
                    print("\t\t posicionDiferente tablero [" + 
                        str(copia[j+1][i+1][2]) + 
                        "] != [" + 
                        str(nueva[j+1][i+1][2]) + 
                        "] nueva"
                        )
                    coordenadas = [j+1, i+1]
        print("\t\t termina posicionDiferente <--")
        return coordenadas

    def imprimeValores(self, matriz):
        cadena=""
        for i in matriz: 
            for _,_,v in i: 
                cadena = cadena+str(v)+" "
            cadena=cadena +"\n"
        return cadena

    def minimax(self, nodo, profundidad, alfa, beta, jugador_maximizar):
        """ 
        Implementación del algoritmo minimax con poda alfa-beta
        """
        # print("inicia minimax -> p = " + str(profundidad))
        # En Python, la lista vacía es False
        if profundidad == 0 or not nodo.children:
            # Obtenemos la evaluación heurística
            h = Heuristicas(jugador_maximizar)
            # copia = [[[k for k in i] for i in j] for j in nodo.data]
            # Tree.limpiarPosiblesMovimientos(copia)
            # valor = h.heuristicaCanon(copia, self.evaluacion)
            # Si el nodo actual corresponde a un nodo hijo de la raíz
            # entonces guardamos dicho nodo junto con su valor.
            # Sabemos que estos hijos están a profundidad 1, 
            # pero en esta función recursiva el conteo es inverso.
            if profundidad == self.profundidad:
                # print("minimax --> se agrega a inmediatas \n" + str(copia))
                # self.inmediatasEvaluadas.append([copia, valor])
                self.inmediatasEvaluadas.append([nodo.data, valor])
            return valor 
        
        if jugador_maximizar:
            maximo = float('-inf')
            for hijo in nodo.children: 
                valor = self.minimax(hijo, profundidad - 1, alfa, beta, False)
                maximo = max(maximo, valor)
                alfa = max(alfa, valor)
                # Nos quedamos con el hijo de la raíz y su valor
                if profundidad == self.profundidad:
                    # copia = [[[k for k in i] for i in j] for j in nodo.data]
                    # Tree.limpiarPosiblesMovimientos(copia)
                    # print("maximo --> se agrega a inmediatas \n" + self.imprimeValores(copia))
                    # self.inmediatasEvaluadas.append([copia, maximo])
                    self.inmediatasEvaluadas.append([nodo.data, maximo])
                if beta <= alfa:
                    break
            return maximo
        
        else:
            minimo = float('inf')
            for hijo in nodo.children: 
                valor = self.minimax(hijo, profundidad - 1, alfa, beta, True)
                minimo = min(minimo, valor)
                # Nos quedamos con el hijo de la raíz y su valor
                if profundidad == self.profundidad:
                    # copia = [[[k for k in i] for i in j] for j in nodo.data]
                    # Tree.limpiarPosiblesMovimientos(copia)
                    # print("minimo --> se agrega a inmediatas \n" + self.imprimeValores(copia))
                    # self.inmediatasEvaluadas.append([copia, minimo])
                    self.inmediatasEvaluadas.append([nodo.data, maximo])
                beta = min(beta, valor)
                if beta <= alfa:
                    break
            return minimo

    #Realiza el cambio de turno
    def cambiarTurno(self):
        #Primero cambia el turno en booleno 
        self.turno= not self.turno


    def generaPosiblesMovimiento(self):
            return Tree.generaPosiblesMovimiento(self.tablero, self.turno)


    #Coloca las posibles jugadas en el tablero
    def colocaPosiblesMovimientos(self):
        #Obtiene los posibles movimientos del tablero, 
        #estos estan representados como [x,y,v], donde x,y es 
        #la posicion del posible movimiento y v siempre vale 0, 
        #puesto que esa casilla debe estar vacia
        validas = self.generaPosiblesMovimiento()
        #Pintamos los posibles movimientos en el tablero
        if validas == []: 
            self.turno = not self.turno
        validas = self.generaPosiblesMovimiento()
        for x,y,v in validas: 
            self.tablero[x][y]=[x,y,3]
        #Actualizamos el arbol
        #Esta actualizacion podria ser mejorada empleando generadores(yield)
        #lo cual impactaria directamente en omitir el calculo de ciertos niveles 
        #y podria ahorra bastante tiempo pero por el momento genera todo el arbol 
        #en cada iteracion
        self.tree = Tree(self.tablero)
        self.tree.generaHijos(self.profundidad, self.turno)
        #Para imprimir
#        print(self.tree)
#        if self.tree.children != []:
#            for child in self.tree.children:
#                print("Hijo")
#                print(child)
#                if child.children != []:
#                    print("Nietos")
#                    for grandChild in child.children:
#                        print(grandChild)
#        print("##########")
        
        
    #Funcion que coloca una ficha en el tablero 
    #y como cuando colocas una ficha tienes que limpiar 
    #los posibles movimientos, tambien lo hace    
    def colocarFicha(self, x, y):
        if(self.turno): 
            self.tablero[x+1][y+1][2] = Tree.BLANCO
        else:
            self.tablero[x+1][y+1][2] = Tree.NEGRO 
        Tree.limpiarPosiblesMovimientos(self.tablero)

    def __str__(self):
        cadena=""
        for i in self.tablero: 
            for _,_,v in i: 
                cadena = cadena+str(v)+" "
            cadena=cadena +"\n"
        return cadena