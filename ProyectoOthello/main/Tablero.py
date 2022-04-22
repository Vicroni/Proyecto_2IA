from Tree import Tree
'''
Clase encargada de tener un control del tablero
que se muestra en pantalla, tambien controla y actualiza el arbol 
dependiendo de la jugadas en pantalla
'''
class Tablero:
  
    #Inicializamos el tablero
    def __init__(self):
        #Creamos la matroz de 8x8x3, veamos que la matriz cada casilla se representa como [x,y,v]
        #donde x,y es la posicion de la casilla dentro del tablero y v representa el valor 
        #de la casilla(Es decir si esta ocupada por una ficha blanca, una negra o es un movimiento posible) 
        self.tablero = [[[y,x,0]  for x in range(10)] for y in range(10)]
        #Turno esta representado por un booleano
        self.turno = False
        #Colocamos las cuatro fichas iniciales
        self.tablero[4][5][2] = Tree.NEGRO
        self.tablero[5][5][2] = Tree.BLANCO
        self.tablero[5][4][2] = Tree.NEGRO
        self.tablero[4][4][2] = Tree.BLANCO
        self.colocaPosiblesMovimientos()
        #Inicializamos el primero arbol con el tablero actual
        self.tree = Tree(self.tablero)
        self.tree.generaHijos(3, self.turno)
        
    #Realiza el cambio de turno
    def cambiarTurno(self):
        #Primero cambia el turno en booleno 
        self.turno= not self.turno
        
    #Coloca las posibles jugadas en el tablero
    def colocaPosiblesMovimientos(self):    
        #Obtiene los posibles movimientos del tablero, 
        #estos estan representados como [x,y,v], donde x,y es 
        #la posicion del posible movimiento y v siempre vale 0, 
        #puesto que esa casilla debe estar vacia
        validas=Tree.generaPosiblesMovimiento(self.tablero, self.turno)
        #Pintamos los posibles movimientos en el tablero
        if validas == []: 
            self.turno = not self.turno
        validas=Tree.generaPosiblesMovimiento(self.tablero, self.turno)
        for x,y,v in validas: 
            self.tablero[x][y]=[x,y,3]
        #Actualizamos el arbol
        #Esta actualizacion podria ser mejorada empleando generadores(yield)
        #lo cual impactaria directamente en omitir el calculo de ciertos niveles 
        #y podria ahorra bastante tiempo pero por el momento genera todo el arbol 
        #en cada iteracion
        self.tree = Tree(self.tablero)
        self.tree.generaHijos(3, self.turno)
        '''
        print(self.tree)
        if self.tree.children != []:
            print(self.tree.children[0])
            if self.tree.children[0].children != []:
                print(self.tree.children[0].children[0])
        print("##########")
        '''
        
    #Funcion que coloca una ficha en el tablero 
    #y como cuando colocas una ficha tienes que limpiar 
    #los posibles movimientos, tambien lo hace    
    def colocarFicha(self, x, y):
        if(self.turno): 
            self.tablero[x+1][y+1][2] = Tree.BLANCO
        else:
            self.tablero[x+1][y+1][2] = Tree.NEGRO 
        Tree.limpiarPosiblesMovimientos(self.tablero)
     
