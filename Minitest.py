import sys
from Globals import *

sys.setrecursionlimit(1000000)

Board = []
HeatMap = []
HeatTruth = []
Move = [0, 0, 0]
Depth = 0
Size = 15
Turn = 0
Depth = 20
Maximising = True
Optimal_score = 0
Alpha = 0
Beta = 0
valid_move = False

for Count1 in range (Size):
        BoardRow = []
        for Count2 in range (Size):
            BoardPosition = ' '
            BoardRow.append(BoardPosition)
        Board.append(BoardRow)

for Count1 in range (Size):
        HeatRow = []
        for Count2 in range (Size):
            HeatValue = 0
            HeatRow.append(HeatValue)
        HeatMap.append(HeatRow)

for Count1 in range (Size):
        TruthRow = []
        for Count2 in range (Size):
            HeatBool = False
            TruthRow.append(HeatBool)
        HeatTruth.append(TruthRow)

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

def Player_Turn(Board, Turn, Move):
  valid_move = False
  while valid_move == False:
    x = int(input('X: '))
    y = int(input('Y: '))
    Move[0] = x
    Move[1] = y
    if Board[y][x] == ' ':
      Board [y][x] = 'O'
      valid_move = True
    Turn += 1
  return Board, Turn, Move

'''def Update_HeatMap(HeatMap, Move, HeatTruth):
    Move_X = int(Move[0])
    Move_Y = int(Move[1])
    HeatMap[Move_X][Move_Y] = -1
    for k in range (2):
          X_pos = min((14, Move_X + k))
          X_neg = max((0, Move_X - k))
          print(X_neg)
          Y_pos = min((14, Move_Y + k))
          Y_neg = max((0, Move_Y - k))
          if HeatMap[X_pos][Y_pos] > -1 and not HeatTruth[X_pos][Y_pos]: HeatMap[X_pos][Y_pos] += 1; HeatTruth[X_pos][Y_pos] = True
          if HeatMap[X_pos][Y_neg] > -1 and not HeatTruth[X_pos][Y_neg]: HeatMap[X_pos][Y_neg] += 1; HeatTruth[X_pos][Y_neg] = True
          if HeatMap[X_neg][Y_pos] > -1 and not HeatTruth[X_neg][Y_pos]: HeatMap[X_neg][Y_pos] += 1; HeatTruth[X_neg][Y_pos] = True
          if HeatMap[X_neg][Y_neg] > -1 and not HeatTruth[X_neg][Y_neg]: HeatMap[X_neg][Y_neg] += 1; HeatTruth[X_neg][Y_neg] = True
    HeatTruth = Reset_HeatTruth(HeatTruth)
    return HeatMap

def Reset_HeatTruth(HeatTruth):
    for i in range (len(HeatTruth)):
        for j in range (len(HeatTruth)):
            HeatTruth[i][j] = False
    return HeatTruth

def Reset_HeatMap(HeatMap):
    for i in range (len(HeatMap)):
        for j in range (len(HeatMap)):
            HeatMap[i][j] = 0
    return HeatMap

def get_Heat(list):
  return list[2]
'''
########
'''def Score_calc(piece, Maximising):
      best = 0
      New_x = Move[0]
      New_y = Move[1]
      search = 4
      for New_x in range (Size):
          for New_y in range (Size):
              hcount = vcount = ldcount = rdcount = 0
              if (Size - New_x) <= 4 or (Size - New_y) <= 4:
                 search = min((Size - New_x -1, Size - New_y - 1))
              for i in range (search):
                if Board[New_x + i][New_y] == piece:
                  hcount += 1
                if Board[New_x][New_y + i] == piece:
                  vcount += 1
                if Board[New_x + i][New_y + i] == piece:
                    rdcount += 1
                if Board[New_x + i][New_y - i] == piece:
                    ldcount += 1
                if Board[New_x - i][New_y + i] == piece:
                    ldcount += 1
                if Board[New_x - i][New_y - i] == piece:
                    rdcount += 1
                best = max((hcount, vcount, ldcount, rdcount, best))
      if Maximising:
        return best
      else:
        #best *= -1
        return best'''

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

def Reset_Depth():
      return 20

# Minimax algorithm with Alpha-Beta Pruning for finding the best move on the game board.
def Ai_Move(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = GetAvailableMoves(Size)
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
    
    player_symbol = "X" if Turn%2 != 0 else 'O'
    # Maximize the score if it's the maximizing player's turn
    if maximizingPlayer:
        value = float('-inf')
        Best_move = valid_locations[0]
        for move in valid_locations:
            Board[move[0]][move[1]] = player_symbol
            new_score = Ai_Move(Board, depth-1, alpha, beta, False)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score > value:
                value = new_score
                Best_move = Move
            alpha = max(alpha, value)
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value
 
    else: # Minimize the score if it's the minimizing player's turn.
        value = float('inf')
        Best_move = valid_locations[0]
        for move in valid_locations:
            Board[move[0]][move[1]] = player_symbol
            new_score = Ai_Move(Board, depth-1, alpha, beta, True)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score > value:
                value = new_score
                Best_move = Move
            alpha = max(alpha, value)
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value
    
def GetAvailableMoves(Size):
        Moves = []
        for i in range (Size):
            for j in range (Size):
                if Board[i][j] == ' ':
                    Moves.append([i, j])
        return Moves

while True:
    if not Win_Check(Board, Size) or Check_Draw(Board, Size):
      if Turn % 2 == 0:
          Board, Turn, Move = Player_Turn(Board, Turn, Move)
          #HeatMap = Update_HeatMap(HeatMap, Move, HeatTruth)
      else:
          Depth = Reset_Depth()
          Max_score, x, y = Ai_Move(Board, Depth, Alpha, Beta, Maximising)
          print(Max_score)
          Max_score = float('-inf')
          Board[x][y] = 'X'
          #HeatMap = Reset_HeatMap(HeatMap)
          #Update_HeatMap(HeatMap, [x, y], HeatTruth)
          print(Board)
          Turn += 1
    else:
       print('it ended btw')