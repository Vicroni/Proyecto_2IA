from Tablero import Tablero
from Tree import Tree
'''
Archivo encargado de la visualizacion grafica del tablero
asi como de los contadores de fichas 
'''
#Declaramos el tablero y el tamaño de las casillas
tab=Tablero()
TAMANO_CASILLA=80

#Creamos la ventana
def setup():
  size(640,640)  
  noStroke()

#Pintamos el tablero de acuerdo a la variable tablero que es una matriz de 10x10x3
def draw():
    for i in range(8):
        for j in range(8):
            fill(0, 144, 103)
            stroke(0) 
            strokeWeight(1.2)
            rect(i*TAMANO_CASILLA,j*TAMANO_CASILLA,TAMANO_CASILLA,TAMANO_CASILLA)
            if(tab.tablero[j+1][i+1][2]==Tree.BLANCO):
                fill(255)
                strokeWeight(0.8)
                ellipse(i*TAMANO_CASILLA+TAMANO_CASILLA/2,j*TAMANO_CASILLA+TAMANO_CASILLA/2, 0.85*TAMANO_CASILLA,0.85*TAMANO_CASILLA)
            elif(tab.tablero[j+1][i+1][2]==Tree.NEGRO):
                fill(0)
                strokeWeight(0.8)
                ellipse(i*TAMANO_CASILLA+TAMANO_CASILLA/2,j*TAMANO_CASILLA+TAMANO_CASILLA/2, 0.85*TAMANO_CASILLA,0.85*TAMANO_CASILLA)
            elif(tab.tablero[j+1][i+1][2]==Tree.POSIBLE):
                fill(0, 144, 103)
                strokeWeight(0.8)
                ellipse(i*TAMANO_CASILLA+TAMANO_CASILLA/2,j*TAMANO_CASILLA+TAMANO_CASILLA/2, 0.85*TAMANO_CASILLA,0.85*TAMANO_CASILLA)

#Capturamos un click en la ventana
def mousePressed():
    x=mouseY/TAMANO_CASILLA
    y=mouseX/TAMANO_CASILLA
    
    #Si corresponde a una casilla valida
    if tab.tablero[x+1][y+1][2] == Tree.POSIBLE:
        #Colcamos la ficha y volteamos las fichas correspondientes
        tab.colocarFicha(x,y)
        tab.tablero=Tree.voltearFichas(x,y, tab.tablero, tab.turno)
        #Ademas de cambiar el turno
        tab.cambiarTurno()
        #Colocamos los posibles movimientos
        tab.colocaPosiblesMovimientos()
