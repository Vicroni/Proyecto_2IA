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
    
    def __init__(self, tablero):
        self.tablero = tablero
        self.posicion = (0,0)
        self.ancho = 80*8
        self.alto = 80*8
        self.casilla_tamanio = TableroPanel.TAMANO_CASILLA_DEFAULT

    def dibujar(self):
        # tablero.tablero es la matriz que tiene el objeto Tablero
        tablero = self.tablero.tablero
        for i in range(8):
            for j in range(8):
                fill(0, 144, 103)
                stroke(0) 
                strokeWeight(1.2)
                rect(i*self.casilla_tamanio,j*self.casilla_tamanio,self.casilla_tamanio,self.casilla_tamanio)
                if(tablero[j+1][i+1][2]==Tablero.BLANCO):
                    fill(255)
                    strokeWeight(0.8)
                    ellipse(i*self.casilla_tamanio+self.casilla_tamanio/2,j*self.casilla_tamanio+self.casilla_tamanio/2, 0.85*self.casilla_tamanio,0.85*self.casilla_tamanio)
                elif(tablero[j+1][i+1][2]==Tablero.NEGRO):
                    fill(0)
                    strokeWeight(0.8)
                    ellipse(i*self.casilla_tamanio+self.casilla_tamanio/2,j*self.casilla_tamanio+self.casilla_tamanio/2, 0.85*self.casilla_tamanio,0.85*self.casilla_tamanio)
                elif(tablero[j+1][i+1][2]==Tablero.POSIBLE):
                    fill(0, 144, 103)
                    strokeWeight(0.8)
                    ellipse(i*self.casilla_tamanio+self.casilla_tamanio/2,j*self.casilla_tamanio+self.casilla_tamanio/2, 0.85*self.casilla_tamanio,0.85*self.casilla_tamanio)

    def onMousePressed(self, mouseX, mouseY):
        tab = self.tablero
        x=mouseY/self.casilla_tamanio
        y=mouseX/self.casilla_tamanio
        
        #Si corresponde a una casilla valida
        if tab.tablero[x+1][y+1][2] == Tablero.POSIBLE:
            #Colcamos la ficha y volteamos las fichas correspondientes
            tab.colocarFicha(x,y)
            tab.tablero = Tree.voltearFichas(x,y, tab.tablero, tab.turno) # <------ THIS LINE IS THE PROBLEM 
            #Ademas de cambiar el turno
            tab.cambiarTurno()
            #Colocamos los posibles movimientos
            tab.colocaPosiblesMovimientos()

"""
Clase que define la barra derecha que muestra la cuenta de fichas en el tablero,
el turno actual, y las opciones para seleccionar el nivel de dificultad.
"""
class SidePanel(Frame):
    ANCHO = 300
    COLOR_FONDO = (229,192,82)

    BOTON_ANCHO = 120
    BOTON_ALTO = 35
    COLOR_BOTON =  (252, 219, 121)
    COLOR_BOTON_SELECCIONADO = (214,175,57)
    
    def __init__(self, tablero):
        self.posicion = (TableroPanel.TAMANO_CASILLA_DEFAULT *8,0)
        self.ancho = SidePanel.ANCHO
        self.alto = TableroPanel.TAMANO_CASILLA_DEFAULT*8
        self.tablero = tablero
    
    def dibujar(self):
        posTexto1 = (self.posicion[0]+70,self.posicion[1]+100)
        posTexto2 = (self.posicion[0]+70,self.posicion[1]+150)
        posTexto3 = (self.posicion[0]+70,self.posicion[1]+200)
        posElipse = (self.posicion[0]+150,self.posicion[1]+300)

        fill(SidePanel.COLOR_FONDO[0], SidePanel.COLOR_FONDO[1], SidePanel.COLOR_FONDO[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text("No. fichas negras: ____", posTexto1[0], posTexto1[1])
        text("No. fichas blancas:____", posTexto2[0], posTexto2[1])
    
        if(not self.tablero.turno) :
        # blancas = true, negras = false
            text("Es turno de las negras", posTexto3[0], posTexto3[1])
            fill(0)
        else :
            text("Es turno de las blancas", posTexto3[0], posTexto3[1])
            fill(250)
        
        stroke(0)
        ellipse(posElipse[0],posElipse[1],120,120)

"""
Clase que define el boton para seleccionar la dificultad Facil.
"""
class BotonFacil(Frame):
    def __init__(self, tablero):
        self.posicion = (TableroPanel.TAMANO_CASILLA_DEFAULT *8 + 90,500)
        self.ancho = SidePanel.BOTON_ANCHO
        self.alto = SidePanel.BOTON_ALTO
        self.tablero = tablero
    
    def dibujar(self):
        fill(SidePanel.COLOR_BOTON[0], SidePanel.COLOR_BOTON[1], SidePanel.COLOR_BOTON[2])
        if self.tablero.dificultad == Tablero.DIFICULTAD_FACIL:
            fill(SidePanel.COLOR_BOTON_SELECCIONADO[0], SidePanel.COLOR_BOTON_SELECCIONADO[1], SidePanel.COLOR_BOTON_SELECCIONADO[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text("Facil", self.posicion[0]+10, self.posicion[1]+20)

    def onMousePressed(self, mouseX, mouseY):
        print("dificultad facil")

"""
Clase que define el boton para seleccionar la dificultad Facil.
"""
class BotonMedia(Frame):
    def __init__(self, tablero):
        self.posicion = (TableroPanel.TAMANO_CASILLA_DEFAULT *8 + 90, 500 + SidePanel.BOTON_ALTO + 5)
        self.ancho = SidePanel.BOTON_ANCHO
        self.alto = SidePanel.BOTON_ALTO
        self.tablero = tablero
    
    def dibujar(self):
        fill(SidePanel.COLOR_BOTON[0], SidePanel.COLOR_BOTON[1], SidePanel.COLOR_BOTON[2])
        if self.tablero.dificultad == Tablero.DIFICULTAD_MEDIA:
            fill(SidePanel.COLOR_BOTON_SELECCIONADO[0], SidePanel.COLOR_BOTON_SELECCIONADO[1], SidePanel.COLOR_BOTON_SELECCIONADO[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text("Intermedio", self.posicion[0]+10, self.posicion[1]+20)
    
    def onMousePressed(self, mouseX, mouseY):
        print("dificultad media")

"""
Clase que define el boton para seleccionar la dificultad Facil.
"""
class BotonDificil(Frame):
    def __init__(self, tablero):
        self.posicion = (TableroPanel.TAMANO_CASILLA_DEFAULT *8 + 90, 500 + SidePanel.BOTON_ALTO*2 + 10)
        self.ancho = SidePanel.BOTON_ANCHO
        self.alto = SidePanel.BOTON_ALTO
        self.tablero = tablero
    
    def dibujar(self):
        fill(SidePanel.COLOR_BOTON[0], SidePanel.COLOR_BOTON[1], SidePanel.COLOR_BOTON[2])
        if self.tablero.dificultad == Tablero.DIFICULTAD_DIFICIL:
            fill(SidePanel.COLOR_BOTON_SELECCIONADO[0], SidePanel.COLOR_BOTON_SELECCIONADO[1], SidePanel.COLOR_BOTON_SELECCIONADO[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text("Dificil", self.posicion[0]+10, self.posicion[1]+20)

    def onMousePressed(self, mouseX, mouseY):
        print("dificil")
    
