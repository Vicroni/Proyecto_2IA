# -*- coding: utf-8 -*-
from Tablero import Tablero
from Tree import Tree

"""
Este modulo contiene los elementos para mostrar la interfaz del juego de Othello.
"""

"""
Esta clase modela una seccion rectangular de la ventana.
Se usa para saber si se hizo clic sobre cierto componente de la interfaz.
Las clases que heredan de Frame deben tener un metodo dibujar que define como
se debe ver el contenido del frame.
"""
class Frame:
    """
    Regresa True si la posicion (x,y) se encuentra dentro de este frame, False si no.
    """
    def posicionEstaDentroDeEsteFrame(self, x,y):
        return x >= self.posicion[0] and y>= self.posicion[1] and x <= self.posicion[0] + self.ancho and y <= self.posicion[1] + self.alto


"""
Clase que define un rectangulo (en el canvas) sobre el que se dibujara
el tablero.
"""
class TableroPanel(Frame):
    TAMANO_CASILLA_DEFAULT = 80
    CANT_CASILLAS = 8
    
    def __init__(self, tablero, sidePanel):
        self.tablero = tablero
        self.sidePanel = sidePanel
        self.posicion = (0,0)
        self.ancho = 80*8
        self.alto = 80*8
        self.casilla_tamanio = TableroPanel.TAMANO_CASILLA_DEFAULT

    def dibujar(self):
        # tablero.tablero es la matriz que tiene el objeto Tablero
        tab = self.tablero
        tablero = tab.tablero
        for i in range(8):
            for j in range(8):
                fill(0, 144, 103)
                stroke(0) 
                strokeWeight(1.2)
                rect(i*self.casilla_tamanio,j*self.casilla_tamanio,self.casilla_tamanio,self.casilla_tamanio)
                if(tablero[j+1][i+1][2] != 0):
                    if(tablero[j+1][i+1][2]==Tablero.BLANCO):
                        fill(255)
                    elif(tablero[j+1][i+1][2]==Tablero.NEGRO):
                        fill(0)
                    elif(tablero[j+1][i+1][2]==Tablero.POSIBLE):
                        fill(0, 144, 103)
                    elif(tablero[j+1][i+1][2]==Tablero.FUTURA):
                        fill(255, 0, 0)
                    strokeWeight(0.8)
                    ellipse(i*self.casilla_tamanio+self.casilla_tamanio/2,j*self.casilla_tamanio+self.casilla_tamanio/2, 0.85*self.casilla_tamanio,0.85*self.casilla_tamanio)
        
        # Si es el turno de la IA
        if tab.ia == tab.turno:
            print(": : : : : > Empieza turno de la IA < : : : : :")
            # Revisamos si hay casillas válidas para la IA
            validas = tab.generaPosiblesMovimiento()
            
            # Si las hay, la IA realiza su jugada
            if not validas:
                # print("Hay validas tab.ia == tab.turno")
                tab.colocaPosiblesMovimientos()
                tab.jugadaAutomatica()
                # print("jugadaAutomatica tab.ia == tab.turno")
                # Verificamos si el jueho terminó
                self.sidePanel.verificarFinDelJuego()
                # print("verificarFinDelJuego tab.ia == tab.turno")
                # Ademas de cambiar el turno
                tab.cambiarTurno()
                print(": : : : : > Turno del Humano < : : : : :")
                # print("cambiarTurno tab.ia == tab.turno")
                # Colocamos los posibles movimientos
                tab.colocaPosiblesMovimientos()
                # print("colocaPosiblesMovimientos tab.ia == tab.turno")
        else:
            tab.cambiarTurno()
            print(": : : : : > Turno del Humano < : : : : :")

    def onMousePressed(self, mouseX, mouseY):
        tab = self.tablero
        x=mouseY/self.casilla_tamanio
        y=mouseX/self.casilla_tamanio

        # Si no es el turno de la IA
        if tab.ia != tab.turno:
            # Si corresponde a una casilla válida para el humano
            if tab.tablero[x+1][y+1][2] == Tablero.POSIBLE:
                print("Hay posibles onMousePressed")
                # Colcamos la ficha y volteamos las fichas correspondientes
                print("Antes de colocarFicha \n" + str(tab))
                tab.colocarFicha(x,y)
                print("Despues de colocarFicha \n" + str(tab))
                print("Antes de voltearFichas")
                tab.tablero = Tree.voltearFichas(x,y, tab.tablero, tab.turno)
                print("Despues de voltearFichas \n" + str(tab))
                self.sidePanel.verificarFinDelJuego()
                tab.cambiarTurno()
                print(": : : : : > Turno de la IA < : : : : :")
                # print("Se cambiarTurno onMousePressed")
                # tab.colocaPosiblesMovimientos()
                # print("Se colocaPosiblesMovimientos onMousePressed")


    # """
    # Este se debe llamar cada que se coloque una ficha
    # """
    # def seColocoUnaFicha(self):
    #     self.sidePanel.verificarFinDelJuego()

"""
Clase que define la barra derecha que muestra la cuenta de fichas en el tablero,
el turno actual, y las opciones para seleccionar el nivel de dificultad.
"""
class SidePanel(Frame):
    ANCHO = 300
    COLOR_FONDO = (229,192,82)
    
    def __init__(self, tablero):
        self.posicion = (TableroPanel.TAMANO_CASILLA_DEFAULT *8,0)
        self.ancho = SidePanel.ANCHO
        self.alto = TableroPanel.TAMANO_CASILLA_DEFAULT*8
        self.tablero = tablero
        self.juegoTerminado = False
    
    def getJuegoTerminado(self):
        return self.juegoTerminado
    
    def dibujar(self):
        posTexto1 = (self.posicion[0]+70,self.posicion[1]+100)
        posTexto2 = (self.posicion[0]+70,self.posicion[1]+150)
        posTexto3 = (self.posicion[0]+70,self.posicion[1]+200)
        posTextoFinDelJuego = (self.posicion[0]+70,self.posicion[1]+450)
        posElipse = (self.posicion[0]+150,self.posicion[1]+300)

        fill(SidePanel.COLOR_FONDO[0], SidePanel.COLOR_FONDO[1], SidePanel.COLOR_FONDO[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text("No. fichas negras:  " + str(self.getFichas(True)) , posTexto1[0], posTexto1[1])
        text("No. fichas blancas: " + str(self.getFichas(False)), posTexto2[0], posTexto2[1])
    
        if(not self.tablero.turno) :
        # blancas = true, negras = false
            text("Es turno de las negras", posTexto3[0], posTexto3[1])
            fill(0)
        else :
            text("Es turno de las blancas", posTexto3[0], posTexto3[1])
            fill(250)
        
        stroke(0)
        ellipse(posElipse[0],posElipse[1],120,120)

        if(self.juegoTerminado):
            fill(0)
            textSize(16)
            text("Fin del juego. Gana: " + self.getGanador(), posTextoFinDelJuego[0], posTextoFinDelJuego[1])
    
    def getFichas(self, color):
        """
        color == true, negro
        color == false, blanco
        """
        tablero = self.tablero.tablero
        fichas = 0
        for i in range(8):
            for j in range(8):
                if color:
                    if(tablero[j+1][i+1][2]==Tablero.NEGRO):
                        fichas += 1
                else:
                    if(tablero[j+1][i+1][2]==Tablero.BLANCO):
                        fichas += 1
        return fichas
    
    """
    Cambia la variable juegoTerminado a True si ninguno de los jugadores puede tirar en el tablero en su estado actual.
    """
    def verificarFinDelJuego(self):
        tablero = self.tablero.tablero
        posiblesMovimientosJugador1 = Tree.generaPosiblesMovimiento(tablero, True)
        posiblesMovimientosJugador2 = Tree.generaPosiblesMovimiento(tablero, False)
        self.juegoTerminado = (not posiblesMovimientosJugador1) and (not posiblesMovimientosJugador2)
    
    """
    Si el juego se acabara en este momento, este metodo regresa que fichas ganaron (Negras, Blancas o Empate)
    """
    def getGanador(self):
        totalNegras = self.getFichas(True)
        totalBlancas = self.getFichas(False)
        if totalNegras > totalBlancas :
            return "Negras"
        elif totalNegras < totalBlancas :
            return "Blancas"
        else:
            return "Empate"
