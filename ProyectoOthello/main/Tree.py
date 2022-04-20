import re
class Tree:
    BLANCO=1
    NEGRO=2
    POSIBLE=3
    
    def __init__(self, data):
        copia=[[[k for k in i] for i in j] for j in data]
        self.data = copia
        self.children = []
        self.profundidad=0

    def generaHijos(self, profundidad, turno):
        if profundidad != 0: 
            for x,y,v in self.generaPosiblesMovimiento(self.data, turno): 
                copia=[[[k for k in i] for i in j] for j in self.data]
                if(turno): 
                    copia[x][y][2] = Tree.BLANCO
                else:
                    copia[x][y][2] = Tree.NEGRO 
                t=Tree(copia)
                t.generaHijos(profundidad-1, not turno)
                self.profundidad=profundidad
                self.children.append(t)
                
    def __str__(self):
        if self.profundidad == 0:
           return str(self.profundidad)
        else: 
            cadena=str(self.profundidad)+":"
            for i in self.children: 
                cadena=cadena+str(i)
            return cadena

    @staticmethod     
    def limpiarPosiblesMovimientos(matriz): 
        for i in matriz: 
            for x,y,v in i: 
                if(v==3): 
                    matriz[x][y]=[x,y,0]
        
    @staticmethod    
    def voltearFichas(x,y,matriz, turno):
        copiaModificada=[[[k for k in i] for i in j] for j in matriz]
        if(turno): 
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,1,0,copiaModificada,matriz) #HorizontalesPositivos
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,-1,0,copiaModificada,matriz) #HorizontalesNegativos
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,0,1,copiaModificada,matriz) #VerticalesPostivos
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,0,-1,copiaModificada,matriz) #VerticalesNegativos
            #Diagonales
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,1,1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,1,-1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,-1,1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.BLANCO, Tree.NEGRO,-1,-1,copiaModificada,matriz) 
        else:
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,1,0,copiaModificada,matriz) #HorizontalesPositivos
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,-1,0,copiaModificada,matriz) #HorizontalesNegativos
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,0,1,copiaModificada,matriz) #VerticalesPostivos
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,0,-1,copiaModificada,matriz) #VerticalesNegativos
            #Diagonales
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,1,1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,1,-1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,-1,1,copiaModificada,matriz) 
            Tree.voltearFichasDireccion(x,y,Tree.NEGRO, Tree.BLANCO,-1,-1,copiaModificada,matriz)
        return copiaModificada
    
    @staticmethod     
    def voltearFichasDireccion(x,y, colorTiro, colorOpuesto, incrementoX, incrementoY, copiaModificada, matriz): 
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
            
    @staticmethod         
    def generaPosiblesMovimiento(matriz, turno):
        Tree.limpiarPosiblesMovimientos(matriz)
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
            if(turno):
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
