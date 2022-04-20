import re

class Tablero:
    BLANCO=1
    NEGRO=2
    POSIBLE=3
  
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
       
    def colocarFicha(self, x, y):
        if(self.turno): 
            self.tablero[x+2][y+2][2] = Tablero.BLANCO
        else:
            self.tablero[x+2][y+2][2] = Tablero.NEGRO 
        self.limpiarPosiblesMovimientos()
        
    def voltearFichas(self,x,y,matriz):
        copiaModificada=[[[k for k in i] for i in j] for j in matriz]
        if(self.turno): 
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,1,0,copiaModificada,matriz) #HorizontalesPositivos
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,-1,0,copiaModificada,matriz) #HorizontalesNegativos
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,0,1,copiaModificada,matriz) #VerticalesPostivos
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,0,-1,copiaModificada,matriz) #VerticalesNegativos
            #Diagonales
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,1,1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,1,-1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,-1,1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.BLANCO, Tablero.NEGRO,-1,-1,copiaModificada,matriz) 
        else:
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,1,0,copiaModificada,matriz) #HorizontalesPositivos
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,-1,0,copiaModificada,matriz) #HorizontalesNegativos
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,0,1,copiaModificada,matriz) #VerticalesPostivos
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,0,-1,copiaModificada,matriz) #VerticalesNegativos
            #Diagonales
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,1,1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,1,-1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,-1,1,copiaModificada,matriz) 
            self.voltearFichasDireccion(x,y,Tablero.NEGRO, Tablero.BLANCO,-1,-1,copiaModificada,matriz)
        
        return copiaModificada
        
    def voltearFichasDireccion(self,x,y, colorTiro, colorOpuesto, incrementoX, incrementoY, copiaModificada, matriz): 
        dx=incrementoX
        dy=incrementoY
        while(matriz[x+2+dx][y+2+dy][2]==colorOpuesto):
            dx=dx+incrementoX
            dy=dy+incrementoY
        if(matriz[x+2+dx][y+2+dy][2]==colorTiro): 
            dx=incrementoX
            dy=incrementoY
            while(matriz[x+2+dx][y+2+dy][2]==colorOpuesto):
                copiaModificada[x+2+dx][y+2+dy][2]=colorTiro
                dx=dx+incrementoX
                dy=dy+incrementoY
    
    def limpiarPosiblesMovimientos(self): 
        for i in self.tablero: 
            for x,y,v in i: 
                if(v==3): 
                    self.tablero[x][y]=[x,y,0]
  
    def cambiarTurno(self):
        self.turno= not self.turno
        validas=self.generaPosiblesMovimiento(self.tablero)
        for x,y,v in validas: 
            self.tablero[x][y]=[x,y,3]

    def generaPosiblesMovimiento(self, matriz):
        self.limpiarPosiblesMovimientos()
        #Genero las posibles combinaciones(Vertical, Horizontal, DiagonalD, DiagonalI)
        max_col = len(matriz[0])
        max_row = len(matriz)
        cols = [[] for _ in range(max_col)]
        rows = [[] for _ in range(max_row)]
        fdiag = [[] for _ in range(max_row + max_col - 1)]
        bdiag = [[] for _ in range(len(fdiag))]
        min_bdiag = -max_row + 1
        for x in range(max_col):
            for y in range(max_row):
                cols[x].append(matriz[y][x])
                rows[y].append(matriz[y][x])
                fdiag[x+y].append(matriz[y][x])
                bdiag[x-y-min_bdiag].append(matriz[y][x])
        posiblesCombinaciones=cols+rows+fdiag+bdiag
        
        #Buscar las casillas validas con regex
        validas=[]
        for cadena in posiblesCombinaciones:
            str1="".join([str(letra[2]) for letra in cadena])
            if(self.turno):
                for m in re.finditer(re.compile(r'02+1'), str1):
                    validas.append(cadena[m.start()])
                for m in re.finditer(re.compile(r'12+0'), str1):
                    validas.append(cadena[m.end()-1])
            else:
                for m in re.finditer(re.compile(r'01+2'), str1):
                    validas.append(cadena[m.start()])
                for m in re.finditer(re.compile(r'21+0'), str1):
                    validas.append(cadena[m.end()-1])
        return validas
