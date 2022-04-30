import re
'''
Clase encargada de almacenar el arbol, 
de igual forma tiene metodos utiles estaticos 
para voltearFichas, limpiarPosiblesMovimientos, generaPosiblesMovimiento
'''
class Tree:
    #Constantes de clase para evitar errores al momento de comparar 
    #tanto en el tablero como en el main que se encarga de la visualizacion
    BLANCO=1
    NEGRO=2
    POSIBLE=3
    
    '''
    Inicializa el arbol, recibiendo en data un tablero 
    con cierta configuracion
    '''
    def __init__(self, data, movimiento, turno):
        #Elimina las referencias
        copia=[[[k for k in i] for i in j] for j in data]
        #Inicializa las variables de la clase
        self.data = copia
        self.children = []
        self.movimiento = movimiento
        self.turno = turno

    '''
    Metodo recursivo que recibe dos argumentos profundidad
    (que indica que tan profundo es el arbol que se va generar) 
    y el turno.
    El caso base es cuando la profundidad es 0, puesto que en ese caso, 
    no es necesario generar ningun hijo 
    El caso recursivo es cuando la profundidad es mayor a 0, entonces genera los posibles movimientos,
    y crea arboles con los tableros que se generan con esos movimientos. Posteriormente los 
    agrega a la lista de hijos y les ordena generar hijos con una profundidad=profundidad-1
     
    Si no hay posibles movimientos entonces cambia de turno y
    genera los posibles movimientos del otro jugador
    '''
    def generaHijos(self, profundidad, turno):
        #Verificamos que no estemos en el caso base
        if profundidad != 0: 
            #Generamos los movimientos
            movimientos = self.generaPosiblesMovimiento(self.data, turno)
            #Checamos que haya movimientos si no los hay entonces cambiamos 
            #de turno y generamos otros movimientos
            if movimientos == []: 
                turno = not turno
                movimientos = self.generaPosiblesMovimiento(self.data, turno)
            #Por cada movimiento generamos una copia del tablero
            for x,y,v in movimientos: 
                    copia=[[[k for k in i] for i in j] for j in self.data]
                    #Y colocamos la ficha correspondiente al movimiento
                    if(turno): 
                        copia[x][y][2] = Tree.BLANCO
                    else:
                        copia[x][y][2] = Tree.NEGRO
                    #Voltamos las fichas de acuerdo al movimiento
                    copia=Tree.voltearFichas(x-1,y-1, copia, turno)
                    #Creamos un arbol que inicializamos con el tablero correspondiente 
                    #al movimiento que acabamos de hacer 
                    t=Tree(copia, [x,y,v], turno)
                    #Y le ordenamos que genere hijos con profundidad-1, ademas de que cambie de turno
                    t.generaHijos(profundidad-1, not turno)
                    #Agregamos este arbol como hijo
                    self.children.append(t)
    @staticmethod             
    def calculaMejorMovimiento(arbol): 
        print("")
        valor, nodoPosible = Tree.minimax_alpha_beta(arbol, float('-inf'), float('inf'), False)
        print([nodoPosible.movimiento[0]-1,nodoPosible.movimiento[1]-1,0])
        return [nodoPosible.movimiento[0]-1,nodoPosible.movimiento[1]-1,0]
                    
    @staticmethod            
    #self.minimax(self, float('-inf'), float('inf'), self.turno)
    def minimax_alpha_beta(nodo, alfa, beta, turnoIA): 
        nodoPosible = None
        if(nodo.children == []):
            return 1, nodo #Aqui va la heuristica
        if nodo.turno==turnoIA:
            maximo = float('-inf')
            for hijo in nodo.children: 
                valor, nodoPosible = Tree.minimax_alpha_beta(hijo, alfa, beta,turnoIA)
                if(valor > maximo): 
                    maximo = valor
                    nodoPosible = nodo
                alfa = max(alfa, valor)
                if(valor > alfa): 
                    alfa = valor
                if beta <= alfa:
                    break
            return maximo, nodoPosible
        else:
            minimo = float('inf')
            for hijo in nodo.children: 
                valor, nodoPosible = Tree.minimax_alpha_beta(hijo, alfa, beta,turnoIA)
                minimo = min(minimo, valor)
                if(minimo > valor): 
                    minimo = valor
                    nodoPosible = nodo
                if(beta > valor): 
                    beta = valor
                beta = min(beta, valor)
                if beta <= alfa:
                    break
            return minimo, nodoPosible
        
            
    '''
    Perzonalizacion del toString que permite que cuando imprimas un arbol, 
    puedas ver la matriz que contiene el nodo padre, eliminando informacion 
    que no es util de visualizar como la posicion de las casillas
    '''             
    def __str__(self):
        cadena=""
        for i in self.data: 
            for x,y,v in i: 
                cadena = cadena+str(v)+" "
            cadena=cadena +"\n"
        return cadena
    
    '''
    Metodo que recibe una matriz y la modifica para eliminar los posibles movimientos
    '''
    @staticmethod     
    def limpiarPosiblesMovimientos(matriz): 
        for i in matriz: 
            for x,y,v in i: 
                if(v==3): 
                    matriz[x][y]=[x,y,0]
    '''
    Metodo que voltea las fichas de una matriz, conociendo 
    en donde se realizo el tiro, la matriz y el turno
    '''
    @staticmethod    
    def voltearFichas(x,y,matriz, turno):
        #Eliminamos la referencias
        copiaModificada=[[[k for k in i] for i in j] for j in matriz]
        #Dependiendo del turno, verificamos en todas las direcciones 
        #cuales deben ser volteadas y las volteamos
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
    '''
    Metodo auxiliar para voltear las fichas en donde se 
    recibe un incremento en X y en y para que vaya validando solo 
    en una direcion cuales fichas deben ser volteadas
    '''
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
    
    '''
    Metodo que genera los posibles movimientos recibe una matriz que representa el tablero 
    y el turno que es booleano y dice si el tiro es de los negros o de los blancos
    turno=true->Blanco 
    turno= false->Negro
    Devuelve los posibles movimientos como una lista de la forma [[x1,y1,v1],[x2,y2,v2],...]
    Donde x->la posicion en x en la matriz, y-> la posicion en y de la matriz, v-> valor de la casilla(siempre sera 0)
    '''
    @staticmethod         
    def generaPosiblesMovimiento(matriz, turno):
        #Genera las posibles combinaciones de la matriz(Filas, Columnas, Diagonales Derechas, Diagonales Izquierdas)
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
        
        #Busca las casillas validas con regex
        #buscandos los conjunto {02^+1} y {12^+0} para las blancas
        #y para las negras {01^+2} y {21^+0}. 
        #Hay que notar que las casillas validas pueden tener repeticiones 
        #pero a la hora de alterar el tablero esto no afectara porque solo 
        #cambiaremos el valor dos veces a 3
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
        #Finalmente eliminamos las casillas de las orillas como posibles movimientos, 
        #pues estas casillas corresponden con jugadas que no son realmente posibles
        validasSinOrillas = []
        for x,y,v in validas:            
            if x > 0 and x < 9 and y > 0 and y < 9 :
                validasSinOrillas.append([x,y,v])
        return validasSinOrillas
