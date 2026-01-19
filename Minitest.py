import sys
from Globals import *

sys.setrecursionlimit(1000000)

Board = []
BoardScore = []
Size = 15
Turn = 0

for Count1 in range (Size):
        BoardRow = []
        for Count2 in range (Size):
            BoardPosition = ' '
            BoardRow.append(BoardPosition)
        Board.append(BoardRow)
#abs(size -(x*y)) - danny b
#or hard code it
for Count1 in range (Size):
        Boardcount = []
        for Count2 in range (Size):
            Score = 0#add calc
            Boardcount.append(BoardPosition)
        BoardScore.append(BoardRow)

def Win_Check(Board, Size):
      for x in range (2, Size-2):
        for y in range (2, Size-2):
          if Board[x-2][y] == Board[x-1][y] == Board[x][y] == Board[x+1][y] == Board [x+2][y] != ' ':
            return True
          elif Board[x][y-2] == Board[x][y-1] == Board[x][y] == Board[x][y+1] == Board [x][y+2] != ' ':
            return True
          elif Board[x-2][y-2] == Board[x-1][y-1] == Board[x][y] == Board[x+1][y+1] == Board [x+2][y+2] != ' ':
            return True
          elif Board[x-2][y+2] == Board[x-1][y+1] == Board[x][y] == Board[x+1][y-1] == Board [x+2][y-2] != ' ':
            return True

def Check_Draw(Board, Size):
      for x in range (Size):
        for y in range (Size):
          if Board[x][y] == ' ':
            return False
      return True

def Player_Turn(Board, Turn):
  valid_move = False
  while valid_move == False:
    x = int(input('X: '))
    y = int(input('Y: '))
    if Board[x][y] == ' ':
      Board [x][y] = 'O'
      valid_move = True
    Turn += 1
  return Board, Turn

#score calc ideas:
#score positions and multiply by lines made?
#+1 if blocking (prioritise defence)
#make a definition of open four etc that should count to inf or whatever

def Score_calc(Turn):
    piece = "X" if Turn%2 != 0 else 'O'
    best = 0
    for New_x in range (Size):
          for New_y in range (Size):
              hcount = vcount = ldcount = rdcount = 0
              for i in range (4):
                try:
                    if Board[New_x + i][New_y] == piece:
                        hcount += 1
                except: pass
                try:
                    if Board[New_x][New_y + i] == piece:
                        vcount += 1
                except: pass
                try:
                    if Board[New_x + i][New_y + i] == piece:
                        rdcount += 1
                except: pass
                try:
                    if Board[New_x - i][New_y + 1] == piece:
                        ldcount += 1
                except: pass
                try:
                    if Board[New_x + i][New_y - 1] == piece:
                        ldcount += 1
                except: pass
                try:
                    if Board[New_x - i][New_y - i] == piece:
                        rdcount += 1
                except: pass
                best = max((hcount, vcount, ldcount, rdcount, best))
    return best

# Minimax algorithm with Alpha-Beta Pruning for finding the best move on the game board.
def Ai_Move(Board, depth, alpha, beta, maximizingPlayer):
    valid_locations = GetAvailableMoves(Board, Size)
    is_terminal = Win_Check(Board, Size) or Check_Draw(Board, Size)
 
    # Base case: If the depth is zero or the game is over, return the current board's score.
    if depth == 0 or is_terminal:
        if is_terminal:
            if Win_Check(Board, Size):
                return (None, float('inf') * (1 if maximizingPlayer else -1))
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, Score_calc(Turn) - Score_calc(Turn + 1))
            #return (None, score_position(board, AI_PIECE)) #fix score
    
    player_symbol = 'X' if Turn %2 != 0 else 'O'
    # Maximize the score if it's the maximizing player's turn
    if maximizingPlayer:
        value = float('-inf')
        Best_move = valid_locations[0]
        for move in valid_locations:
            if move == [3, 2]: raise Exception
            new_score = Ai_Move(Board, depth-1, alpha, beta, False)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score > value:
                value = new_score
                Best_move = move
            alpha = max(alpha, value)
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value
 
    else: # Minimize the score if it's the minimizing player's turn.
        value = float('inf')
        Best_move = valid_locations[0]
        for move in valid_locations:
            if move == [3, 2]: raise Exception
            Board[move[0]][move[1]] = 'O'
            
            new_score = Ai_Move(Board, depth-1, alpha, beta, True)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score < value:
                value = new_score
                Best_move = move
            beta = min(beta, value)
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value
    
def GetAvailableMoves(Board, Size):
        Moves = []
        for i in range (Size):
            for j in range (Size):
                if Board[i][j] == ' ':
                    Moves.append([i, j])
        return Moves

while True:
    if not Win_Check(Board, Size) or Check_Draw(Board, Size):
      if Turn % 2 == 0:
          Board, Turn = Player_Turn(Board, Turn)
      else:
          Best_move, Max_score  = Ai_Move(Board, 2, float('-inf'), float('inf'), True)
          Board[Best_move[0]][Best_move[1]] = 'X'
          Turn += 1
    else:
       print('it ended btw')