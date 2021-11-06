//
// aitetris.cc
// from http://www.liacs.leidenuniv.nl/~kosterswa/AI/
// January 27, 2021
// Walter Kosters, w.a.kosters@liacs.leidenuniv.nl
//
// Tetris playing programme
//
// Compile: g++ -Wall -Wextra -O2 -o aitetris aitetris.cc 
// Usage: ./aitetris <height> <width> <print: 0/1> <games> <playouts> <seed>
//    play games games on a height by width board
//    if print is 1, much more output is generated
//    seed seeds the random number generator
//    and Monte Carlo (MC) uses playouts
//
// Every piece has a unique name (see below), orientation (0/1/2/3),
// and starting position (0...width of game board - 1), indicating
// the column of the leftmost square of the position of the piece.
// Note that possible orientation and position depend on the piece!
// As an example: move 7 (out of 34, being 0..33) for piece LG (a Left 
// Gun), on a width 10 board, corresponds with orientation 0, starting 
// in column 7. There is perhaps no need to know this.
//
// The program generates a random series of pieces, and then needs
// an orientation and position (random in this version, see the function
// playrandomgame (print)); the piece then drops as required. 
// After that rows are cleared, and the board is displayed.
//
// The board is of size h (height) times w (width);
// bottom left is (0,0); the top 3 rows are "outside" the board: 
// if part of a piece ends here, the game stops.
//
// If you have a piece, the function call possibilities (piece) 
// returns the number of possible moves possib. These moves are 
// denoted by 0,1,...,possib-1. Given a number n in this range, 
// the function dothemove (piece,n) then does the corresponding move.
//

//
// The 7 pieces, with orientations:
//
//  LS  0:  XX     1:  X                          Left Snake
//           XX       XX
//                    X
//
//  RS  0:   XX    1: X                           Right Snake
//          XX        XX
//                     X
//
//  I   0:  XXXX   1:  X                          I
//                     X
//                     X
//                     X
//
//  Sq  always 0: XX                              Square
//                XX
//                
//  T   0:   XXX   1:  X     2:   X      3:   X   T
//            X        XX        XXX         XX
//                     X                      X
//
//  LG  0:  XXX    1:  XX    2:  X       3:   X   Left Gun
//            X        X         XXX          X
//                     X                     XX
//
//  RG  0:  XXX    1:  X     2:    X     3:  XX   Right Gun
//          X          X         XXX          X
//                     XX                     X
//                   

#include <iostream>
#include <ctime>         // for time stuff
#include <cstdlib>       // for rand ( )
using namespace std;

enum PieceName {Sq,LG,RG,LS,RS,I,T};

const int wMAX = 20;     // maximum width of the game board
const int hMAX = 15;     // maximum total height of the game board

class Tetris {
  private:
    int h, w;               // actual height and width
    bool board[hMAX][wMAX]; // the game board; board[i][j] true <=> occupied
    int piececount;         // number of pieces that has been used so far
    int rowscleared;        // number of rows cleared so far
    int theplayouts;        // used by Monte Carlo
    int highestPositionMove; //The Highest row touched by doing a certain move with let it fall. 

    void getrandompiece (PieceName & piece);
    void clearrows ( );
    void displayboard ( );
    void letitfall (PieceName piece, int orientation, int position);
    void infothrowpiece (PieceName piece, int orientation, int position);
    bool endofgame ( );
    int possibilities (PieceName piece);
    void computeorandpos (PieceName piece, int & orientation, int & position, int themove);
    void dorandommove (PieceName piece);
    void doMCmove (PieceName piece);
    void toprow (bool therow[wMAX], int & numberrow, int & empties);
    int numberempties (int numberrow);
    void dothemove (PieceName piece, int themove);
    void dosmartmove(PieceName piece);
    int numberofclosedspaces ( );
    bool fullrow ( );
    int countshaft ( );
    
  public:
    Tetris ( );
    Tetris (int height, int width, int playouts);
    void reset ( );
    void statistics ( );
    void playrandomgame (bool print);
    void playMCgame (bool print);
    void playsmartgame (bool print);
    
    
};//Tetris

// default constructor
Tetris::Tetris ( ) {
  int i, j;
  piececount = 0;
  rowscleared = 0;
  h = hMAX;
  w = wMAX;
  for ( i = 0; i < hMAX; i++ )
    for ( j = 0; j < wMAX; j++ )
      board[i][j] = false;
}//Tetris::Tetris

// constructor
Tetris::Tetris (int height, int width, int playouts) {
  int i, j;
  piececount = 0;
  rowscleared = 0;
  theplayouts = playouts;
  if ( height < hMAX )
    h = height;
  else
    h = hMAX;
  if ( 4 <= width && width < wMAX )
    w = width;
  else
    w = wMAX;
  for ( i = 0; i < hMAX; i++ )
    for ( j = 0; j < wMAX; j++ )
      board[i][j] = false;
}//Tetris::Tetris

// reset the game
void Tetris::reset ( ) {
  int i, j;
  piececount = 0;
  rowscleared = 0;
  for ( i = 0; i < hMAX; i++ )
    for ( j = 0; j < wMAX; j++ )
      board[i][j] = false;
}//Tetris::reset

// some statistics
void Tetris::statistics ( ) {
  cout << endl << "Done! We have "
       << rowscleared << " row(s) cleared, using "
       << piececount << " pieces." << endl;
}//Tetris::statistics

// how many empties has row numberrow?
int Tetris::numberempties (int numberrow) {
  int j, theempties = w;
  for ( j = 0; j < w; j++ )
    if ( board[numberrow][j] )
      theempties--;
  return theempties;
}//Tetris::numberempties

// gives number of empties in heighest non-empty row,
// and copies this row into therow; its row index being numberrow
// if this is -1, the whole field is empty
void Tetris::toprow (bool therow[wMAX], int & numberrow, int & empties) {
  int i, j, theempties;
  numberrow = -1;
  empties = w;
  for ( i = 0; i < h; i++ ) {
    theempties = numberempties (i);
    if ( theempties < w ) {
      for ( j = 0; j < w; j++ )
        therow[j] = board[i][j];
      empties = theempties;
      numberrow = i;
    }//if
  }//for
}//Tetris::toprow

// checks for full rows --- and removes them
void Tetris::clearrows ( ) {
  int i, j, k;
  bool full;
  for ( i = h-2; i >= 0; i-- ) {
    full = true;
    j = 0;
    while ( full && j < w )
      if ( !board[i][j] )
	full = false;
      else
        j++;  
    if ( full ) {
      //cout << "Row cleared ..." << endl;
      rowscleared++;
      for ( k = i; k < h-1; k++ )
	for ( j = 0; j < w; j++ )
	  board[k][j] = board[k+1][j];
      for ( j = 0; j < w; j++ )
	board[h-1][j] = false;
    }//if
  }//for
}//Tetris::clearrows

// displays current board on the screen
void Tetris::displayboard ( ) {
  int i, j;
  for ( i = h-1; i >= 0; i-- ) {
    if ( i < h-3 )
      cout << "|";
    else
      cout << " ";
    for ( j = 0; j < w; j++ )
      if ( board[i][j] )
        cout << "X";
      else
	cout << " ";
    if ( i < h-3 )
      cout << "|" << endl;
    else
      cout << endl;
  }//for
  for ( j = 0; j < w+2; j++ )
    cout << "-";
  cout << endl;
  cout << " ";
  for ( j = 0; j < w; j++ )
    cout << j % 10;
  cout << endl;
  cout << "This was move "<< piececount << "." << endl;
}//Tetris::displayboard

// let piece fall in position and orientation given
// assume it still fits in top rows
void Tetris::letitfall (PieceName piece, int orientation, int position) { //positions is equal to the move 
  int x[4] = {0};
  int y[4] = {0};
  int i;
  highestPositionMove = 0;
  piececount++;
  switch (piece) {
    case Sq: x[0] = position; y[0] = h-2;        
             x[1] = position; y[1] = h-1;      
	     x[2] = position+1; y[2] = h-2;           
	     x[3] = position+1; y[3] = h-1;
	     break;
    case LG: switch (orientation) {
	       case 0: x[0] = position+2; y[0] = h-2;
                       x[1] = position+2; y[1] = h-1;
	               x[2] = position+1; y[2] = h-1;
	               x[3] = position; y[3] = h-1;
		       break;
	       case 1: x[0] = position; y[0] = h-3;
                       x[1] = position; y[1] = h-2;
	               x[2] = position; y[2] = h-1;
	               x[3] = position+1; y[3] = h-1;
		       break;
	       case 2: x[0] = position; y[0] = h-2;
                       x[1] = position+1; y[1] = h-2;
	               x[2] = position+2; y[2] = h-2;
	               x[3] = position; y[3] = h-1;
		       break;
	       case 3: x[0] = position; y[0] = h-3;
                       x[1] = position+1; y[1] = h-1;
	               x[2] = position+1; y[2] = h-2;
	               x[3] = position+1; y[3] = h-3;
		       break;
	     }//switch
	     break;
    case RG: switch (orientation) {
	       case 0: x[0] = position; y[0] = h-2;
                       x[1] = position+2; y[1] = h-1;
	               x[2] = position+1; y[2] = h-1;
	               x[3] = position; y[3] = h-1;
		       break;
	       case 1: x[0] = position; y[0] = h-3;
                       x[1] = position; y[1] = h-2;
	               x[2] = position; y[2] = h-1;
	               x[3] = position+1; y[3] = h-3;
		       break;
	       case 2: x[0] = position; y[0] = h-2;
                       x[1] = position+1; y[1] = h-2;
	               x[2] = position+2; y[2] = h-2;
	               x[3] = position+2; y[3] = h-1;
		       break;
	       case 3: x[0] = position+1; y[0] = h-3;
                       x[1] = position+1; y[1] = h-1;
	               x[2] = position+1; y[2] = h-2;
	               x[3] = position; y[3] = h-1;
		       break;
	     }//switch
	     break;
    case LS: switch (orientation) {
	       case 0: x[0] = position+1; y[0] = h-2;
                       x[1] = position+1; y[1] = h-1;
	               x[2] = position+2; y[2] = h-2;
	               x[3] = position; y[3] = h-1;
		       
		       break;
	       case 1: x[0] = position; y[0] = h-3;
                       x[1] = position; y[1] = h-2;
	               x[2] = position+1; y[2] = h-1;
	               x[3] = position+1; y[3] = h-2;
		       break;
	     }//switch
	     break;
    case RS: switch (orientation) {
	       case 0: x[0] = position+1; y[0] = h-2;
                       x[1] = position+1; y[1] = h-1;
	               x[2] = position+2; y[2] = h-1;
	               x[3] = position; y[3] = h-2;
		       break;
	       case 1: x[0] = position+1; y[0] = h-3;
                       x[1] = position; y[1] = h-2;
	               x[2] = position+1; y[2] = h-2;
	               x[3] = position; y[3] = h-1;
		       break;
	     }//switch
	     break;
    case I : switch (orientation) {
	       case 0: x[0] = position; y[0] = h-1;
                       x[1] = position+1; y[1] = h-1;
	               x[2] = position+2; y[2] = h-1;
	               x[3] = position+3; y[3] = h-1;
		       break;
	       case 1: x[0] = position; y[0] = h-4;
                       x[1] = position; y[1] = h-3;
	               x[2] = position; y[2] = h-2;
	               x[3] = position; y[3] = h-1;
		       break;
	     }//switch
	     break;
    case T : switch (orientation) {
	       case 0: x[0] = position+1; y[0] = h-2;
                       x[1] = position; y[1] = h-1;
	               x[2] = position+1; y[2] = h-1;
	               x[3] = position+2; y[3] = h-1;
		       break;
	       case 1: x[0] = position; y[0] = h-3;
                       x[1] = position; y[1] = h-2;
	               x[2] = position; y[2] = h-1;
	               x[3] = position+1; y[3] = h-2;
		       break;
	       case 2: x[0] = position; y[0] = h-2;
                       x[1] = position+1; y[1] = h-2;
	               x[2] = position+2; y[2] = h-2;
	               x[3] = position+1; y[3] = h-1;
		       break;
	       case 3: x[0] = position+1; y[0] = h-3;
                       x[1] = position+1; y[1] = h-2;
	               x[2] = position+1; y[2] = h-1;
	               x[3] = position; y[3] = h-2;
		       break;
	     }//switch
	     break;
  }//switch
  while ( y[0] > 0 && !board[y[0]-1][x[0]] 
          && !board[y[1]-1][x[1]] && !board[y[2]-1][x[2]]
          && !board[y[3]-1][x[3]] )
    for ( i = 0; i < 4; i++ )
      y[i]--;//Move it down
  for ( i = 0; i < 4; i++ ){
    board[y[i]][x[i]] = true;
    if (y[i] > highestPositionMove) 
      highestPositionMove = y[i]; //Store the row where the highest part of the piece can be found.
  }
  clearrows ( );
}//Tetris::letitfall

// give piece a chance: info to the screen
void Tetris::infothrowpiece (PieceName piece, int orientation, int position) {
  int j;
  cout << endl;
  for ( j = 0; j < w+5; j++ )
    cout << "=";	  
  if ( piececount < 10 )
    cout << "   ";
  else if ( piececount < 100 )
    cout << "  ";
  else
    cout << " ";
  cout << piececount << ": ";
  switch ( piece ) {
    case Sq: cout << "Square      "; break;
    case LG: cout << "Left gun    "; break;
    case RG: cout << "Right gun   "; break;
    case LS: cout << "Left snake  "; break;
    case RS: cout << "Right snake "; break;
    case I:  cout << "I           "; break;
    case T:  cout << "T           "; break;
  }//switch
  cout << orientation << " " << position << endl;
}//Tetris::infothrowpiece

// check whether top 3 rows are somewhat occupied (so game has ended?)
bool Tetris::endofgame ( ) {
  int j;
  for ( j = 0; j < w; j++ ) 
    if ( board[h-3][j] )
      return true;
  return false;
}//Tetris::endofgame

// how many possibilities has piece?

int Tetris::possibilities (PieceName piece){
  if ( piece == Sq )
    return (w-1);
  if ( ( piece == LS ) || ( piece == RS ) || ( piece == I ) )
    return (2*w-3);
  return (4*w-6);// the x in x*w-6 etc is equal to the number of rotations of the piece.
}//Tetris::possibilities

// compute orientation and position for move themove from piece
void Tetris::computeorandpos (PieceName piece, int & orientation, int & position, int themove) {
  orientation = 0;//Standard rotation for everyone
  position = themove; //The move is the column
  switch ( piece ) {
    case LS: 
    case RS: if ( themove > w-3 ) {// If the rotation doesn't fit the board
               orientation = 1;// Change rotation
	       position = themove - (w-2);
	     }//if
	     break;
    case I:  if ( themove > w-4 ) {
               orientation = 1;
	       position = themove - (w-3);
	     }//if
	     break;
    case Sq: break;
    case T:  
    case LG: 
    case RG: if ( themove > 3*w-6 ) {
               orientation = 3;
	       position = themove - (3*w-5);
	     }//if
	     else if ( themove > 2*w-4 ) {
               orientation = 2;
	       position = themove - (2*w-3);
	     }//if
             else if ( themove > w-3 ) {
               orientation = 1;
	       position = themove - (w-2);
	     }//if
	     break;
  }//switch
}//Tetris::computeorandpos

// generate a random piece
void Tetris::getrandompiece (PieceName & piece) {
    int intpiece = rand ( ) % 7;
    switch (intpiece) {
      case 0: piece = LS; break;
      case 1: piece = RS; break;
      case 2: piece = I; break;
      case 3: piece = Sq; break;
      case 4: piece = T; break;
      case 5: piece = LG; break;
      case 6: piece = RG; break;
    }//switch
}//Tetris::getrandompiece

// do themove for the given piece
// assume thet 0 <= themove < possibilities (piece)
void Tetris::dothemove (PieceName piece, int themove) {
  int orientation;
  int position;
  computeorandpos (piece,orientation,position,themove);
  letitfall (piece,orientation,position);
}//Tetris::dothemove

// do a random move for piece
void Tetris::dorandommove (PieceName piece) {
  int themove = rand ( ) % possibilities (piece); //
  dothemove (piece,themove);
}//Tetris::dorandommove

// do a MC move for piece
void Tetris::doMCmove (PieceName piece) {
  int bestmove = 0;
  int mostrowscleared = 0;
  int mostmoves = 0;
    for (int move = 0; move < possibilities(piece); move++){
    int totalrowscleared = 0;
    int totalmoves = 0;
    //Return the rows cleared and the number of moves.
    for (int x = 0; x < theplayouts; x++){
      Tetris copy = *this;
      copy.dothemove(piece,move);
      copy.playrandomgame(false);
      totalrowscleared += copy.rowscleared;
      totalmoves += copy.piececount;
     }//for
     if (totalrowscleared > mostrowscleared){
        mostrowscleared = totalrowscleared;
        bestmove = move;
      }else if (totalrowscleared == mostrowscleared){
        if (totalmoves > mostmoves){
          mostmoves = totalmoves;
          bestmove = move;
        }
      }
  }//for
  dothemove(piece, bestmove);
}//Tetris::doMCmove

void Tetris::dosmartmove (PieceName piece) {
  int bestmove = 0;
  int bestScore = INT32_MIN;
  int currentclosedspaces = 0; 
  for (int move = 0; move < possibilities(piece); move++){
    Tetris copy = *this;
    int premove_openshaftspots = copy.countshaft();
    copy.dothemove(piece,move);
    int aftermove_openshaftspots = copy.countshaft();
    currentclosedspaces = copy.numberofclosedspaces();
    int currentscore = 0;
    if (copy.endofgame() == false){
      /*calculate the score of a move based on certain properties
      that are changed by doing the move.*/
      currentscore += copy.rowscleared;
      currentscore += 1 * (h - copy.highestPositionMove);
      currentscore -= 4 * currentclosedspaces;
      currentscore += 1 * (premove_openshaftspots-aftermove_openshaftspots);
      if (currentscore > bestScore){
        bestScore = currentscore;
        bestmove = move;
      }
    }
  }
    dothemove(piece, bestmove);
}

//Check the number of shafts there are in a board. A shaft is defined by an one space wide opening.
int Tetris::countshaft(){//
int openspaces = 0;
for (int column = 0; column < w; column++){ 
  for (int row = h-1; row >=0 ; row--){ 
    if (board[row][column]) break; 
    if (//Checks if a space is enclosed from the right and left.
       (board[row][column+1] && board[row][column-1]) || 
       (board[row][column+1] && column == 0) || 
       (board[row][column-1] && column == w-1)){
          openspaces+=1;
          while (row < h && row > 0){//Counts the openspaces of a shaft when a shaft is found.
          if (board[row-1][column]){break;} 
          row--;
          openspaces+=1;
      }
    }
  }
}
  return openspaces;
}

//Find the number of spaces which are not accesible by a piece at the moment.
int Tetris::numberofclosedspaces(){
  int totalclosedpositions = 0;
  for (int row = 0; row < h; row++){
    for (int column = 0; column < w; column++){
      if (!board[row][column]){//If there is no piece
      for (int a = row; a < h-1; a++){//Looks up to see open space is closed off.
        if (board[a+1][column]){
          totalclosedpositions = totalclosedpositions + 1;//Counts all the spaces in the column that are closed off.
          break;
        }
      }
    }
   }
  }
  return totalclosedpositions;
}

//play a random game
void Tetris::playrandomgame (bool print) {
  PieceName piece;
  int nr, emp;
  bool therow[wMAX];
  if ( print )
    displayboard ( );
  while ( ! endofgame ( ) ) {
    getrandompiece (piece);    // obtain random piece
    dorandommove (piece);      // and drop it randomly
    if ( print ) {
      displayboard ( );        // print the board
      toprow (therow,nr,emp);  // how is top row?
      if ( nr != -1 ) 
        cout << "Top row " << nr << " has " << emp << " empties" << "." << endl;
    }//if
  }//while
}//Tetris::playrandomgame

//play a MC game
void Tetris::playMCgame (bool print) {
  PieceName piece;
  int nr, emp;
  bool therow[wMAX];
  if ( print )
    displayboard ( );
  while ( ! endofgame ( ) ) {
    getrandompiece (piece);    // obtain random piece
    doMCmove (piece);          // and drop it using MC
    if ( print ) {
      displayboard ( );        // print the board
      toprow (therow,nr,emp);  // how is top row?
      if ( nr != -1 ) 
        cout << "Top row " << nr << " has " << emp << " empties" << "." << endl;
    }//if
  }//while
}//Tetris::playMCgame

void Tetris::playsmartgame (bool print) {
  PieceName piece;
  int nr, emp;
  bool therow[wMAX];
  if ( print )
    displayboard ( );
  while ( ! endofgame ( ) ) {
    getrandompiece (piece);    // obtain random piece
    dosmartmove(piece);          // and drop it using MC
    if ( print ) {
      displayboard ( );        // print the board
      toprow (therow,nr,emp);  // how is top row?
      if ( nr != -1 ) 
        cout << "Top row " << nr << " has " << emp << " empties" << "." << endl;
    }//if
  }//while
}//Tetris::playMCgame

int main (int argc, char* argv[ ]) {
  if ( argc != 7 ) {
    cout << "Usage: " << argv[0] << " <height> <width> <print: 0/1> "
	 << "<games> <playouts> <seed>" << endl;
    return 1;
  }//if
  int h = atoi (argv[1]);
  int w = atoi (argv[2]);
  bool print = ( atoi (argv[3]) == 1 );
  int numberofgames = atoi (argv[4]);
  int playouts = atoi (argv[5]);
  Tetris board (h,w,playouts);
  int i;
  srand (atoi (argv[6]));
  for ( i = 1; i <= numberofgames; i++ ) {
    if ( print ) {
      cout << "Game "<< i << ":"<< endl;
    }//if
    board.reset ( );
    //board.numberofclosedspaces();
    //board.playrandomgame(print); 
    //board.playMCgame(print);
    board.playsmartgame(print);
    board.statistics ( );
  }//if
  return 0;
}//main