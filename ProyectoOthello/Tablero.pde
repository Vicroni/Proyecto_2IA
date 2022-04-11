class Tablero{
  final static int BLANCO=1;
  final static int NEGRO=2;
  final static int POSIBLE=3;
  final static int tamano_casilla=80;
  int[][] tablero = new int[8][8];
  boolean turno; // BLANCO=true, NEGRO = false
  
  void display(){
    this.initializeBoard();
    this.updateBoard();
  }
  
  void initializeBoard(){
    turno=false; 
    colocarFicha(3, 4);
    cambiarTurno();
    colocarFicha(3, 3);
    cambiarTurno();
    colocarFicha(4, 3);
    cambiarTurno();
    colocarFicha(4, 4);
    cambiarTurno();
  }
  
  void updateBoard(){
    for(int i=0;i<8 ;i++){
      for(int j=0;j<8 ;j++){
        fill(0, 144, 103);
        stroke(0); 
        strokeWeight(1.2);
        rect(i*80,j*80,80,80);
        if(tablero[j][i]==BLANCO){
          fill(255); 
          strokeWeight(0.8);
          ellipse(i*tamano_casilla+tamano_casilla/2,j*tamano_casilla+tamano_casilla/2, 0.85*tamano_casilla,0.85*tamano_casilla);
        }else if(tablero[j][i]==NEGRO){
          fill(0); 
          strokeWeight(0.8);
          ellipse(i*tamano_casilla+tamano_casilla/2,j*tamano_casilla+tamano_casilla/2, 0.85*tamano_casilla,0.85*tamano_casilla);
        }else if(tablero[j][i]==POSIBLE){
          fill(0, 144, 103); 
          strokeWeight(0.8);
          ellipse(i*tamano_casilla+tamano_casilla/2,j*tamano_casilla+tamano_casilla/2, 0.85*tamano_casilla,0.85*tamano_casilla);
        }
      }
    }
  }
  
  void colocarFicha(int x, int y){
    tablero[y][x]= turno ? BLANCO : NEGRO;
  }
  
  
  void cambiarTurno(){
    turno=!turno;
  }
}
