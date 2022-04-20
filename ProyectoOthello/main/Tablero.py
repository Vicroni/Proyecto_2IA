from Tree import Tree

class Tablero:
  
    def __init__(self):
        self.tablero = [[[y,x,0]  for x in range(10)] for y in range(10)]
        self.turno = False
        self.colocarFicha(3, 4)
        self.cambiarTurno()
        self.colocarFicha(3, 3)
        self.cambiarTurno()
        self.colocarFicha(4, 3)
        self.cambiarTurno()
        self.colocarFicha(4, 4)
        self.cambiarTurno()
        self.tree = Tree(self.tablero)
        self.tree.generaHijos(2, self.turno)
        print(str(self.tree))
        
    def cambiarTurno(self):
        self.turno= not self.turno
        validas=Tree.generaPosiblesMovimiento(self.tablero, self.turno)
        for x,y,v in validas: 
            self.tablero[x][y]=[x,y,3]
            
    def colocarFicha(self, x, y):
        if(self.turno): 
            self.tablero[x+2][y+2][2] = Tree.BLANCO
        else:
            self.tablero[x+2][y+2][2] = Tree.NEGRO 
        Tree.limpiarPosiblesMovimientos(self.tablero)
     
