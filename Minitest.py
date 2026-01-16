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

def Update_HeatMap(HeatMap, Move, HeatTruth):
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

def Score_calc(piece, Maximising):
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
        return best

def Reset_Depth():
      return 20

def Ai_Move(Board, HeatMap, Turn, Size, Depth, Alpha, Beta, Optimal_score, Maximising):
        AvailableMoves = GetAvailableMoves(Size, HeatMap)
        if (Win_Check(Board, Size) == True or Check_Draw(Board, Size) == True) or Depth <= 0:
            if Check_Draw(Board, Size):
              return 0
            if Depth == 0:
              print('idk')
              Current_Score = max((Score_calc('X', Maximising), Score_calc('O', Maximising)))
              Optimal_score = max((Optimal_score, Current_Score))
              Alpha = max((Alpha, Current_Score))
              return Optimal_score, None, None
            elif Turn == 1:
              return -10, curent_best_move[0], curent_best_move[1] 
            elif Turn == 2:
              return +10, curent_best_move[0], curent_best_move[1]

        if Maximising:
              curent_best_move = None
              for i in AvailableMoves:
                print(AvailableMoves)
                Current_score = float('-inf')
                if Board[i[0]][i[1]] == ' ':
                  print('actually max')
                  Board[i[0]][i[1]] = 'X'
                  HeatMap = Update_HeatMap(HeatMap, [i[0], i[1]], HeatTruth)
                  print(Board)
                  Current_Score, x, y = Ai_Move(Board, HeatMap, Turn, Size, Depth -1, Alpha, Beta, Optimal_score, False)
                  if Current_score > Optimal_score:
                    Optimal_score = Current_score
                    current_best_move = [[i[0]],[i[1]]]
                  Alpha = max((Alpha, Current_Score))
                  Board[i[0]][i[1]] = ' '
                  if Beta <= Alpha:
                    break

        else:
              '''for j in AvailableMoves:
                if Board[j[0]][j[1]] == ' ':
                  print('min')
                  Board[j[0]][j[1]] = 'O'
                  HeatMap = Update_HeatMap(HeatMap, [j[0], j[1]], HeatTruth)
                  AvailableMoves = GetAvailableMoves(Size, HeatMap)
                  print(Board)
                  Current_Score, x, y = Ai_Move(Board, HeatMap, Turn, Size, Move, Depth - 1, Alpha, Beta, Max, Min, True)
                  Optimal_score= max((Min_score, Current_Score))
                  Beta = max((Beta, Current_Score))
                  Board[j[0]][j[1]] = ' '
                  if Optimal_score == Current_Score:
                    Move = [j[0], j[1]]
                  Depth = Reset_Depth()
                  if Beta <= Alpha:
                     break
                else:
                  Current_Score, x, y = Ai_Move(Board, HeatMap, Turn, Size, Move, Depth, Alpha, Beta, Max, Min, Maximising)'''
              curent_best_move = None
              for i in AvailableMoves:
                Current_score = float('inf')
                if Board[i[0]][i[1]] == ' ':
                  print('min')
                  Board[i[0]][i[1]] = 'O'
                  HeatMap = Update_HeatMap(HeatMap, [i[0], i[1]], HeatTruth)
                  print(Board)
                  Current_Score, x, y = Ai_Move(Board, HeatMap, Turn, Size, Depth -1, Alpha, Beta, Optimal_score, True)
                  if Current_score < Optimal_score:
                    Optimal_score = Current_score
                    current_best_move = [i[0][i[1]]]
                  Beta = min((Beta, Current_Score))
                  Board[i[0]][i[1]] = ' '
                  if Beta <= Alpha:
                    break
        return Optimal_score, Move[0], Move[1]

def GetAvailableMoves(Size, HeatMap):
        AvailableMoves = []
        print(HeatMap)
        for i in range (Size):
            for j in range (Size):
                if int(HeatMap[i][j]) >= 1:
                    append = [i, j, int(HeatMap[i][j])]
                    AvailableMoves.append(append)
        AvailableMoves.sort(reverse = True, key = get_Heat)
        return AvailableMoves

while True:
    if not Win_Check(Board, Size) or Check_Draw(Board, Size):
      if Turn % 2 == 0:
          Board, Turn, Move = Player_Turn(Board, Turn, Move)
          HeatMap = Update_HeatMap(HeatMap, Move, HeatTruth)
      else:
          Depth = Reset_Depth()
          Max_score, x, y = Ai_Move(Board, HeatMap, Turn, Size, Depth, Alpha, Beta, Optimal_score, Maximising)
          print(Max_score)
          Max_score = float('-inf')
          Board[x][y] = 'X'
          HeatMap = Reset_HeatMap(HeatMap)
          Update_HeatMap(HeatMap, [x, y], HeatTruth)
          print(Board)
          Turn += 1
    else:
       print('it ended btw')