from Tablero import Tablero
from Tree import Tree
from InterfazTablero import TableroPanel, SidePanel, Frame

'''
Archivo encargado de mostrar la interfaz grafica
'''

# Dimensiones:
ANCHO_VENTANA = 300 + 8*80
ALTO_VENTANA = 8*80
BOTON_ANCHO = 120
BOTON_ALTO = 35
# Colores:
COLOR_FONDO_MENU = (229,192,82)
COLOR_BOTON = (252, 219, 121)
COLOR_BOTON_SELECCIONADO = (214,175,57)


"""
Clase que define un boton.
"""
class Boton(Frame):
    def __init__(self, posicion, texto):
        self.posicion = posicion
        self.ancho = BOTON_ANCHO
        self.alto = BOTON_ALTO
        self.texto = texto
        self.color_fondo = COLOR_BOTON
        self.color_selected = COLOR_BOTON_SELECCIONADO

    def dibujar(self):
        fill(self.color_fondo[0], self.color_fondo[1], self.color_fondo[2])
        stroke(0)
        strokeWeight(1.2)
        rect(self.posicion[0],self.posicion[1],self.ancho,self.alto)

        fill(0)
        textSize(16)
        text(self.texto, self.posicion[0]+10, self.posicion[1]+20)


# -----------------------------------------------------------

# Inicializo los componentes de la interfaz:
botonFacil = Boton((400,300), "Facil")
botonMedia = Boton((400,300 + BOTON_ALTO + 5), "Media")
botonDificil = Boton((400,300 + 2*(BOTON_ALTO + 5)), "Dificil")
botonMenuPrincipal = Boton((80*8+90,500), "Volver al menu")

mostrar_menu = True


#Creamos la ventana
def setup():
  size(640+300,640)
  noStroke()

#Pintamos el tablero de acuerdo a la variable tablero que es una matriz de 10x10x3
def draw():
    if mostrar_menu :
        dibujarMenu()
    else:
        tableroPanel.dibujar()
        sidePanel.dibujar()
        botonMenuPrincipal.dibujar()

#Capturamos un click en la ventana
def mousePressed():

    if mostrar_menu :
        if botonFacil.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
            print("facil")
            iniciarJuego("facil")
    
        if botonMedia.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
            print("medio")
            iniciarJuego("medio")
    
        if botonDificil.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
            print("dificil")
            iniciarJuego("dificil")
    else:
        if tableroPanel.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
            tableroPanel.onMousePressed(mouseX, mouseY)
        
        if botonMenuPrincipal.posicionEstaDentroDeEsteFrame(mouseX, mouseY):
            global mostrar_menu
            mostrar_menu = True


def iniciarJuego(dificultad):
    #print("inicia iniciarJuego")
    global mostrar_menu
    mostrar_menu = False
    #print("antes tab = Tablero(dificultad)")
    tab = Tablero(dificultad)
    #print("despues tab = Tablero(dificultad)")
    global sidePanel
    sidePanel = SidePanel(tab)
    global tableroPanel
    tableroPanel = TableroPanel(tab, sidePanel)
    #print("termina iniciarJuego")


def dibujarMenu():
    posTexto1 = (380,280)

    fill(COLOR_FONDO_MENU[0], COLOR_FONDO_MENU[1], COLOR_FONDO_MENU[2])
    stroke(0)
    strokeWeight(1.2)
    rect(0,0,ANCHO_VENTANA,ALTO_VENTANA)

    fill(0)
    textSize(16)
    text("Elige un nivel de dificultad:", posTexto1[0], posTexto1[1])
    
    botonFacil.dibujar()
    botonMedia.dibujar()
    botonDificil.dibujar()
