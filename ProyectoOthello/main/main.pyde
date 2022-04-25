from Tablero import Tablero
from Tree import Tree
from InterfazTablero import TableroPanel, SidePanel, BotonFacil, BotonMedia, BotonDificil

'''
Archivo encargado de mostrar la interfaz grafica
'''

tab=Tablero()

interfazTab = TableroPanel(tab)
sidePanel = SidePanel(tab)
botonFacil = BotonFacil(tab)
botonMedia = BotonMedia(tab)
botonDificil = BotonDificil(tab)


#Creamos la ventana
def setup():
  size(640+300,640)
  noStroke()

#Pintamos el tablero de acuerdo a la variable tablero que es una matriz de 10x10x3
def draw():
    interfazTab.dibujar()
    sidePanel.dibujar()
    botonFacil.dibujar()
    botonMedia.dibujar()
    botonDificil.dibujar()

#Capturamos un click en la ventana
def mousePressed():
    
    if interfazTab.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
        interfazTab.onMousePressed(mouseX, mouseY)
    
    if botonFacil.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
        botonFacil.onMousePressed(mouseX, mouseY)
    
    if botonMedia.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
        botonMedia.onMousePressed(mouseX, mouseY)
    
    if botonDificil.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
        botonDificil.onMousePressed(mouseX, mouseY)
    
