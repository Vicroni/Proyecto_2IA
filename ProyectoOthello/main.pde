Tablero tab; 

void setup(){
  size(640,640); 
  noStroke();
  tab = new Tablero();
  tab.display();
}

void draw(){
    tab.updateBoard();
}

void mousePressed() {
  tab.colocarFicha(mouseX/Tablero.tamano_casilla,mouseY/Tablero.tamano_casilla);
  tab.cambiarTurno();
}
