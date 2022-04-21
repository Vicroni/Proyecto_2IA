import re
class Tree:
    BLANCO=1
    NEGRO=2
    POSIBLE=3
    
    def __init__(self, data):
        copia=[[[k for k in i] for i in j] for j in data]
        self.data = copia
        self.children = []

    def generaHijos(self, profundidad, turno):
        if profundidad != 0: 
            movimientos = self.generaPosiblesMovimiento(self.data, turno)
            if movimientos == 0: 
                turno = not turno
                movimientos = self.generaPosiblesMovimiento(self.data, turno)
            for x,y,v in movimientos: 
                    copia=[[[k for k in i] for i in j] for j in self.data]
                    if(turno): 
                        copia[x][y][2] = Tree.BLANCO
                    else:
                        copia[x][y][2] = Tree.NEGRO
                    copia=Tree.voltearFichas(x-1,y-1, copia, turno) 
                    t=Tree(copia)
                    t.generaHijos(profundidad-1, not turno)
                    self.children.append(t)
            
                
    def __str__(self):
        cadena=""
        for i in self.data: 
            for x,y,v in i: 
                cadena = cadena+str(v)+" "
            cadena=cadena +"\n"
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
        while(matriz[x+1+dx][y+1+dy][2]==colorOpuesto):
            dx=dx+incrementoX
            dy=dy+incrementoY
        if(matriz[x+1+dx][y+1+dy][2]==colorTiro): 
            dx=incrementoX
            dy=incrementoY
            while(matriz[x+1+dx][y+1+dy][2]==colorOpuesto):
                copiaModificada[x+1+dx][y+1+dy][2]=colorTiro
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
        validasSinOrillas = []
        for x,y,v in validas:            
            if x > 0 and x < 9 and y > 0 and y < 9 :
                validasSinOrillas.append([x,y,v])
        return validasSinOrillas
