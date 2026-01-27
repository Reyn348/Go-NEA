from Globals import *
import sys
import random
import math
import numpy
from abc import ABC

#sys.setrecursionlimit(100000)

def Update_HeatMap(HeatMap, Move, HeatTruth):
    Move_X = Move[0]
    Move_Y = Move[1]
    HeatMap[Move_X][Move_Y] = -1
    for k in range (2):
          X_pos = min((14, Move_X + k))
          X_neg = max((0, Move_X - k))
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
 
def Open_row_search(x, y, Piece): #all except three here is pointless tbh since it wins anyway
    Three = False
    Open_Three = False #split multiple definitions at once
    Four = False
    Open_Four = False
    #horizontal
    #if Board[x][y] == Board[x+1][y] and Board[x+2][y] == Board[x][y] and Board[x][y] == Piece: #make similar lines like this (and everything)
    if Board[x][y] == Board[x+1][y] == Board[x+2][y] == Piece:
        Three = True
        '''if Board[x-1][y] == Board[x+3][y] == ' ':
            Open_Three = True
        elif Board[x+3][y] == Piece:
            Four = True
            if Board[x-1][y] == Board[x+4][y] == ' ':
                Open_Four = True'''

    #vertical
    if Board[x][y] == Board[x][y+1] == Board[x][y+2] == Piece:
        Three = True
        '''if Board[x][y-1] == Board[x][y+3] == ' ':
            Open_Three = True
        elif Board[x][y+3] == Piece:
            Four = True
            if Board[x][y-1] == Board[x][y+4] == ' ':
                Open_Four = True'''

    #left diagonal
    if Board[x][y] == Board[x+1][y+1] == Board[x+2][y+2] == Piece:
        Three = True
        '''if Board[x-1][y-1] == Board[x+3][y+3] == ' ':
            Open_Three = True
        elif Board[x+3][y+3] == Piece:
            Four = True
            if Board[x-1][y-1] == Board[x+4][y+4] == ' ':
                Open_Four = True'''

    #right diagonal
    if Board[x][y] == Board[x-1][y+1] == Board[x-2][y+2] == Piece:
        Three = True
        '''if Board[x+1][y-1] == Board[x-3][y+3] == ' ':
            Open_Three = True
        elif Board[x-3][y+3] == Piece:
            Four = True
            if Board[x+1][y-1] == Board[x-4][y+4] == ' ':
                Open_Four = True'''

    '''if Open_Four:
        print('open four')
        print(Piece)
        return 10000000000
    elif Four:
       print('four')
       print(Piece)
       return 1000000000
    elif Open_Three:
       print('open three')
       print(Piece)
       return 10000000'''
    if Three:
       return 100000
    else:
       return 0

def Score_calc(maximisingPlayer):
    Piece = 'O' if maximisingPlayer else 'X'
    Opponent = 'X' if maximisingPlayer else 'O'
    best = 0
    for x in range (1, Size-4):
       for y in range (1, Size-4):
         if Board[x][y] != ' ':
          Open = Open_row_search(x, y, Piece)
          best = max((Open, best))
          '''if Board[x][y] == Piece:
            best += Open
          else:
            best -= Open'''

    for New_x in range (Size): #may need to entirely redo the scoring, since open threes etc progress towards win, but otherwise it has no idea what it is doing
          for New_y in range (Size):
              hcount = vcount = ldcount = rdcount = 0
              hscore = vscore = ldscore = rdscore = 0
              for i in range (4):
                try:
                    if Board[New_x + i][New_y] == Piece:
                        hcount += 1
                        hscore += int(BoardScore[New_x + i][New_y])*(hcount+1)
                    elif Board[New_x + i][New_y] == Opponent:
                        hscore += 1
                except: pass
                try:
                    if Board[New_x][New_y + i] == Piece:
                        vcount += 1
                        vscore += int(BoardScore[New_x][New_y +i])*(vcount+1)
                    elif Board[New_x][New_y + i] == Opponent:
                        vscore += 1
                except: pass
                try:
                    if Board[New_x - i][New_y + i] == Piece:
                        ldcount += 1
                        ldscore += int(BoardScore[New_x - i][New_y + i])*(ldcount+1)
                    elif Board[New_x - i][New_y + i] == Opponent:
                        ldscore += 1
                except: pass
                try:
                    if Board[New_x - i][New_y - i] == Piece:
                        rdcount += 1
                        rdscore += int(BoardScore[New_x - i][New_y - i])*(rdcount+1)
                    elif Board[New_x - i][New_y - 1] == Opponent:
                        rdscore += 1
                except: pass
                best = max((hscore, vscore, ldscore, rdscore, best))
    return best

#Minimax algorithm with Alpha beta Pruning for finding the best move on the game board.
def Ai_Move(Board, depth, alpha, beta, maximisingPlayer):
    valid_locations = GetAvailableMoves(Size)
    if Game.Win_Check(Board, Size) or Game.Check_Draw(Board, Size): 
      is_terminal = True
      if not Game.Win_Check(Board, Size):
        raise Exception
    else: is_terminal = False

    #If the depth is zero or the game is over, return the current board's score.
    if depth == 0 or is_terminal:
        if is_terminal:
            if Game.Win_Check(Board, Size):
                print((10000000000000 + depth) * (1 if maximisingPlayer else -1))
                print(Board)
                return (None, (10000000000000 + depth) * (1 if maximisingPlayer else -1))
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, Score_calc(True) - Score_calc(False))
            #return (None, 0)
    
    Player_symbol = 'O' if maximisingPlayer else 'X'
    # Maximize the score if it's the maximizing player's turn
    if maximisingPlayer:
        value = float('-inf')
        Best_move = [-1, -1]
        for move in valid_locations:
            Board[move[0]][move[1]] = Player_symbol
            if Game.Win_Check(Board, Size):
              print('max win')
              new_score = Ai_Move(Board, depth, alpha, beta, True)[1]
            else:
              print('max not win')
              new_score = Ai_Move(Board, depth-1, alpha, beta, False)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score > value:
                value = new_score
                Best_move = move
            alpha = max((alpha, value))
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value
 
    else: # Minimize the score if it's the minimizing player's turn.
        value = float('inf')
        Best_move = [-1, -1]
        for move in valid_locations:
            Board[move[0]][move[1]] = Player_symbol
            if Game.Win_Check(Board, Size):
              new_score = Ai_Move(Board, depth, alpha, beta, False)[1]
            else:
                new_score = Ai_Move(Board, depth-1, alpha, beta, True)[1]
            Board[move[0]][move[1]] = ' '
 
            # Update the best move and alpha value.
            if new_score < value:
                value = new_score
                Best_move = move
            beta = min((beta, value))
 
            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        return Best_move, value

def GetAvailableMoves(Size):
  AvailableMoves = []
  for i in range (Size):
    for j in range (Size):
      if Board[i][j] == ' ':
        if HeatMap[i][j] > 0:
          AvailableMoves.append([i, j, HeatMap[i][j]])
  AvailableMoves.sort(reverse=True, key=get_Heat)
  return AvailableMoves

class TextInput(pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, height=50, color= BLACK, bgcolor=WHITE, selectedColor=(190,195,198)):
        super().__init__()
        self.text_value = ''
        self.isSelected = False
        self.color = color
        self.bgcolor = bgcolor
        self.selectedColor = selectedColor
        self.font = FONT40
        self.text = self.font.render(self.text_value, True, self.color)
        self.bg = pygame.Rect(x, y, width, height)
       
    def clicked(self, mousePos):
        if self.bg.collidepoint(mousePos):
            self.isSelected = not(self.isSelected)
            return True
        return False
       
    def update_text(self, new_text):
        temp = self.font.render(new_text, True, self.color)
        if temp.get_rect().width >= (self.bg.width - 20):
            return
        self.text_value = new_text
        self.text = temp
        return self.text_value
       
    def render(self, display):
        self.pos = self.text.get_rect(center = (self.bg.x + self.bg.width/2, self.bg.y + self.bg.height/2))
        if self.isSelected:
            pygame.draw.rect(display, self.selectedColor, self.bg)
        else:
            pygame.draw.rect(display, self.bgcolor, self.bg)
        display.blit(self.text, self.pos)
       
class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.current = None
       
    def current(self):
        return self.current
  
class basePlayer(ABC):
   def __init__(self):
      pass
   
   def move(self, Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth):
      Temp_Board = numpy.copy(Board) #just for the undo function
      Updated = False
      if not (CPU and Turn == 2):
        if Size == 15:
          if x % 35 <= 10:
            XIndex = math.floor(x/35)
          elif x % 35 >= 20:
            XIndex = math.ceil(x/35)

          if y % 35 <= 10:
            YIndex = math.floor(y/35)
          elif y % 35 >= 25:
            YIndex = math.ceil(y/35)
          
        elif Size == 19:
          if x % 30 <= 10:
            XIndex = math.floor(x/30)
          elif x % 30 >= 20:
            XIndex = math.ceil(x/30)
          
          if y % 30 <= 10:
            YIndex = math.floor(y/30)
          elif y % 30 >= 20:
            YIndex = math.ceil(y/30)
      else:
         XIndex = x
         YIndex = y

      if Board[XIndex][YIndex] == ' ':
        if Turn == 1:
            Board[XIndex][YIndex] = 'X'
        else:
            Board[XIndex][YIndex] = 'O'  
        Game.Update_Board(Turn, XIndex, YIndex)
        HeatMap = Update_HeatMap(HeatMap, [XIndex, YIndex], HeatTruth)
        Line_Check = Game.Win_Check(Board, Size)
        Updated = True 
        if Line_Check:
          X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Winner(Turn)
          return Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier
        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn)
      return Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, [140, 360, 1175, 1275], [650, 740, 510, 610], ['Rules', 'Undo'], 'GAME'
   
   def Move_calc(self, Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth):
        Updated = False
        if Size == 15:
            x = (mouse_pos[0]-610)
            y = (mouse_pos[1]-313)
            if(x % 35 <= 10 or x % 35 >= 25) and (y % 35 <= 10 or y % 35 >= 25) and (-10 <= x <= 500 and -10 <= y <= 500):
                Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = self.move(Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth)
                Line_Check = Game.Win_Check(Board, Size)
                return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
            else:
               return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
          
        elif Size == 19:
            x = (mouse_pos[0]-580)
            y = (mouse_pos[1]-290)
            if (x % 30 <= 10 or x % 30 >= 20) and (y % 30 <= 10 or y % 30 >= 20) and (-10 <= x <= 600 and -10<= y <+ 600):
                Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = self.move(Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth)
                Line_Check = Game.Win_Check(Board, Size)
                return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
            else:
               return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
   
class humanPlayer(basePlayer):
  def __init__(self):
      super().__init__()
      pass
  
class computerPlayer(basePlayer):
  def __init__(self):
      super().__init__()
      pass

class Drawing():
  def __init__(self):
      pass
   
  def Main_Menu():
      for i in range (5):
        pygame.draw.rect(screen, WHITE, (MAIN_MENU_RECT[i]), 4)
        pygame.display.flip()
        
      MENUT0 = FONT100.render('Main Menu', True, BLACK)
      MenuRect0 = MENUT0.get_rect()
      MenuRect0.center = (200, 50)
      screen.blit(MENUT0, MenuRect0)
      
      MENUT1 = FONT75.render('Gomoku Player', True, BLACK)
      MenuRect1 = MENUT1.get_rect()
      MenuRect1.center = (720, 150)
      screen.blit(MENUT1, MenuRect1)
      
      MENUT2 = FONT100.render('Play Vs Computer', True, BLACK)
      MenuRect2 = MENUT2.get_rect()
      MenuRect2.center = (720, 320)
      screen.blit(MENUT2, MenuRect2)
      
      MENUT3 = FONT100.render('Play Vs Human', True, BLACK)
      MenuRect3 = MENUT3.get_rect()
      MenuRect3.center = (720,  470)
      screen.blit(MENUT3, MenuRect3)
      
      MENUT4 = FONT100.render('Rules', True, BLACK)
      MenuRect4 = MENUT4.get_rect()
      MenuRect4.center = (720, 650)
      screen.blit(MENUT4, MenuRect4)
      pygame.display.flip()
      
      #formula of coords is 2i (for less extreme) and 2i+1 (for more extreme) for i>=0
      X_LIST = [395, 1045, 445, 995, 590, 850]
      Y_LIST = [270, 370, 420, 520, 600, 700]
      BUTTON_LIST = ['AI_opponent','Player_name', 'Rules']
      Identifier = 'MENU'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def Rules(temp):
      Redraw = False
      for i in range (5):
        pygame.draw.rect(screen, WHITE, (RULES_RECT[i]), 4)
        pygame.display.flip()

      RULEST0 = FONT100.render('The Rules', True, BLACK)
      RulesRect0 = RULEST0.get_rect()
      RulesRect0.center = (180, 50)
      screen.blit(RULEST0, RulesRect0)
      
      RULEST1 = FONT53.render('   Gomoku is played on a 15x15 ', True, BLACK)
      RulesRect1 = RULEST1.get_rect()
      RulesRect1.center = (345, 200)
      screen.blit(RULEST1, RulesRect1)
      
      RULEST2 = FONT53.render('board. ', True, BLACK)
      RulesRect2 = RULEST2.get_rect()
      RulesRect2.center = (125, 240)
      screen.blit(RULEST2, RulesRect2)
      
      RULEST3 = FONT53.render('   Black plays first, and players ', True, BLACK)
      RulesRect3 = RULEST3.get_rect()
      RulesRect3.center = (345, 315)
      screen.blit(RULEST3, RulesRect3)
      
      RULEST4 = FONT53.render('alternate in placing a stone of their ', True, BLACK)
      RulesRect4 = RULEST4.get_rect()
      RulesRect4.center = (375, 355)
      screen.blit(RULEST4, RulesRect4)
      
      RULEST5 = FONT53.render('colour on an empty intersection. ', True, BLACK)
      RulesRect5 = RULEST5.get_rect()
      RulesRect5.center = (351, 395)
      screen.blit(RULEST5, RulesRect5)
      
      RULEST6 = FONT53.render('   The winner is the first player to ', True, BLACK)
      RulesRect6 = RULEST6.get_rect()
      RulesRect6.center = (360, 470)
      screen.blit(RULEST6, RulesRect6)
      
      RULEST7 = FONT53.render('form an unbroken chain of five ', True, BLACK)
      RulesRect7 = RULEST7.get_rect()
      RulesRect7.center = (334, 510)
      screen.blit(RULEST7, RulesRect7)
      
      RULEST8 = FONT53.render('stones horizontally, vertically, or ', True, BLACK)
      RulesRect8 = RULEST8.get_rect()
      RulesRect8.center = (350, 550)
      screen.blit(RULEST8, RulesRect8)
      
      RULEST9 = FONT53.render('diagonally. ', True, BLACK)
      RulesRect9 = RULEST9.get_rect()
      RulesRect9.center = (160, 590)
      screen.blit(RULEST9, RulesRect9)
      
      RULEST10 = FONT53.render('   Once placed, stones cannot be ', True, BLACK)
      RulesRect10 = RULEST10.get_rect()
      RulesRect10.center = (355, 665)
      screen.blit(RULEST10, RulesRect10)
      
      RULEST11 = FONT53.render('moved or removed from the board. ', True, BLACK)
      RulesRect11 = RULEST11.get_rect()
      RulesRect11.center = (365, 715)
      screen.blit(RULEST11, RulesRect11)
    
      RULEST12 = FONT100.render('Return', True, BLACK)
      RulesRect12 = RULEST12.get_rect()
      RulesRect12.center = (1320, 850)
      screen.blit(RULEST12, RulesRect12)
      pygame.display.flip()
      
      X_LIST = [1200, 1440]
      Y_LIST = [800, 900]
      BUTTON_LIST = [temp]
      Identifier = 'RULES'
      if temp == 'GAME':
         Redraw = True
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Redraw

  def P1_Name():
      pygame.draw.rect(screen, (SCREEN_COLOUR),(380, 235, 680, 540), 0)
      pygame.draw.rect(screen, WHITE, (380, 235, 680, 430), 4)
     
      TextInputGroup.add(TextInput(x=605, y=440, width = 230))
      pygame.display.flip()
     
      for i in range (3):
          pygame.draw.rect(screen, WHITE, (NAMES_GET_RECT[i]), 4)
          pygame.display.flip()
         
      NAMEST0 = FONT68.render('Please enter Player names:', True, BLACK)
      NAMESRect0 = NAMEST0.get_rect()
      NAMESRect0.center = (720, 290)
      screen.blit(NAMEST0, NAMESRect0)
      
      NAMEST1 = FONT68.render('Player 1 name:', True, BLACK)
      NAMESRect1 = NAMEST1.get_rect()
      NAMESRect1.center = (720, 395)
      screen.blit(NAMEST1, NAMESRect1)
      
      NAMEST2 = FONT55.render('(Player names must differ)', True, BLACK)
      NAMESRect2 = NAMEST2.get_rect()
      NAMESRect2.center = (720, 567)
      screen.blit(NAMEST2, NAMESRect2)
      pygame.display.flip()
      
      #no buttons, only inputs - requires change of enter key code
      Identifier = 'NAMES'
      X_LIST = []
      Y_LIST = []
      BUTTON_LIST = []
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def P2_Name():
      for current in TextInputGroup:
          TextInputGroup.remove(current)
     
      pygame.draw.rect(screen, (SCREEN_COLOUR),(540, 360, 360, 70), 0)
      pygame.draw.rect(screen, WHITE, (540, 360, 360, 70), 4)
     
      TextInputGroup.add(TextInput(x=605, y=440, width = 230))
      pygame.display.flip()
      
      NAMES2T0 = FONT68.render('Player 2 name:', True, BLACK)
      NAMES2Rect0 = NAMES2T0.get_rect()
      NAMES2Rect0.center = (720, 395)
      screen.blit(NAMES2T0, NAMES2Rect0)
      pygame.display.flip()
      
      Identifier = 'P2'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def Main_Program():
      for i in range (5):
          pygame.draw.rect(screen, WHITE, MAIN_PROG_RECT[i], 4)
          pygame.display.flip()

      MAINT0 = FONT50.render('Player 1s score: ' + str(P1SCORE), True, BLACK)
      MAINRect0 = MAINT0.get_rect()
      MAINRect0.center = (225, 390)
      screen.blit(MAINT0, MAINRect0)
      
      MAINT1 = FONT50.render('Player 2s score: ' + str(P2SCORE), True, BLACK)
      MAINRect1 = MAINT1.get_rect()
      MAINRect1.center = (225, 460)
      screen.blit(MAINT1, MAINRect1)
      
      MAINT2 = FONT100.render('Rules', True, BLACK)
      MAINRect2 = MAINT2.get_rect()
      MAINRect2.center = (250, 695)
      screen.blit(MAINT2, MAINRect2)
      pygame.display.flip()
      
      X_LIST = [140, 360]
      Y_LIST = [650, 740]
      BUTTON_LIST = ['Rules']
      Identifier = 'MAIN'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def Board_Size():
      X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Program()
      for current in TextInputGroup:
          TextInputGroup.remove(current)
     
      pygame.draw.rect(screen, SCREEN_COLOUR, (600, 400, 650, 340), 0)
      pygame.draw.rect(screen, WHITE, (600, 400, 650, 340), 4)
      
      for i in range (2):
        pygame.draw.rect(screen, WHITE, BOARD_SIZE_RECT[i], 4)
        pygame.display.flip()
      
      BOARDT0 = FONT50.render('Please select your desired', True, BLACK)
      BOARDRect0= BOARDT0.get_rect()
      BOARDRect0.center = (925, 460)
      screen.blit(BOARDT0, BOARDRect0)
      
      BOARDT1 = FONT50.render('board size:', True, BLACK)
      BOARDRect1= BOARDT1.get_rect()
      BOARDRect1.center = (925, 500)
      screen.blit(BOARDT1, BOARDRect1)
      
      BOARDT2 = FONT75.render('15x15', True, BLACK)
      BOARDRect2= BOARDT2.get_rect()
      BOARDRect2.center = (925, 570)
      screen.blit(BOARDT2, BOARDRect2)
      
      BOARDT3 = FONT75.render('19x19', True, BLACK)
      BOARDRect3= BOARDT2.get_rect()
      BOARDRect3.center = (925, 650)
      screen.blit(BOARDT3, BOARDRect3)
      pygame.display.flip()
      
      X_LIST = [140, 360, 835, 1015, 835, 1015]
      Y_LIST = [650, 740, 540, 600, 620, 680]
      BUTTON_LIST = ['Rules', '15', '19']
      Identifier = 'BOARD_SIZE'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def Clean():
     screen.fill(SCREEN_COLOUR)

  def Fail(error):
      pygame.draw.rect(screen, (SCREEN_COLOUR), (450, 530, 540, 80), 0)
      pygame.draw.rect(screen, (WHITE), (415, 530, 610, 80), 4)
      pygame.display.flip()
      
      if error == 'Name':
        FAILT0 = FONT55.render('ERROR: player name are same', True, BLACK)
        FAILRect0 = FAILT0.get_rect()
        FAILRect0.center = (720, 570)
        screen.blit(FAILT0, FAILRect0)
   
      elif error == 'Empty':
        FAILT1 = FONT55.render('ERROR: Invalid input', True, BLACK)
        FAILRect1 = FAILT1.get_rect()
        FAILRect1.center = (720, 570)
        screen.blit(FAILT1, FAILRect1)
      pygame.display.flip()
   
  def Game(Size):
    Size = int(Size)
    pygame.draw.rect(screen, SCREEN_COLOUR, (500, 260, 900, 600), 0)
    pygame.draw.rect(screen, WHITE, (500, 260, 900, 585), 4)
    
    if Size == 15:
        for i in range (14):
            for j in range (14):
                pygame.draw.rect(screen, WHITE, ((610+35*i), (313+35*j), 35, 35), 1)
                
        pygame.draw.rect(screen, WHITE, (1175, 510, 200, 100), 4)
        
        GAMET0 = FONT100.render('Undo', True, BLACK)
        GAMERect0= GAMET0.get_rect()
        GAMERect0.center = (1275, 560)
        screen.blit(GAMET0, GAMERect0)
        pygame.display.flip  
          
    elif Size == 19:
        for i in range (18):
            for j in range (18):
                pygame.draw.rect(screen, WHITE, ((580+30*i), (290+30*j), 30, 30), 1)
        
        pygame.draw.rect(screen, WHITE, (1175, 510, 200, 100), 4)
        
        GAMET1 = FONT75.render('Undo', True, BLACK)
        GAMERect1= GAMET1.get_rect()
        GAMERect1.center = (1275, 560)
        screen.blit(GAMET1, GAMERect1)
        pygame.display.flip
    
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
    
    BoardScore = Game.get_BoardScore(Size)

    X_LIST = [140, 360, 1175, 1275]
    Y_LIST = [650, 740, 510, 610]
    BUTTON_LIST = ['Rules', 'Undo']
    Identifier = 'GAME'
    return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size
  
  def Winner(Turn):
      pygame.draw.rect(screen, SCREEN_COLOUR, (600, 380, 510, 340), 0)
      pygame.draw.rect(screen, WHITE, (600, 380, 510, 340), 4)
      pygame.draw.rect(screen, WHITE, (770, 565, 180, 70), 4)
      
      WINNERT0 = FONT75.render('Player ' + str(Turn) + ' wins!', True, BLACK)
      WINNERRect0= WINNERT0.get_rect()
      WINNERRect0.center = (860, 450)
      screen.blit(WINNERT0, WINNERRect0)

      WINNERT1 = FONT65.render('Replay', True, BLACK)
      WINNERRect1 = WINNERT1.get_rect()
      WINNERRect1.center = (860, 600)
      screen.blit(WINNERT1, WINNERRect1)
      pygame.display.flip

      X_LIST = [770, 950]
      Y_LIST = [565, 635]
      BUTTON_LIST = ['Replay']
      Identifier = 'GAME_OVER'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

class Game():
    def __init__(self):
       pass

    def Draw_Next(Next, Size, Temp_Board, Board, Turn, Turn_count, CPU):  
      if Next == 'AI_opponent':
         Drawing.Clean()
         X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()

      elif Next == 'Player_name':
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.P1_Name()
        
      elif Next == '15' or Next == '19':
        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn)
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Next)
        
      elif Next == 'MENU':
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Menu()
    
      elif Next == 'Undo':
         X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn = Game.Undo_Move(Size, Board, Temp_Board, Turn_count, Turn)

      else:
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()
        
      return  X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size, Board, Turn, Turn_count, CPU
      
    def get_BoardScore(Size):
      if Size == 15:
        BoardScore = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
                    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'], 
                    ['1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '2', '1'], 
                    ['1', '2', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '5', '5', '5', '5', '5', '5', '5', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '5', '6', '6', '6', '6', '6', '5', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '5', '6', '7', '7', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '7', '6', '5', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '5', '6', '7', '7', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '6', '6', '6', '6', '5', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '5', '5', '5', '5', '5', '5', '5', '4', '3', '2', '1'], 
                    ['1', '2', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '3', '2', '1'], 
                    ['1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '2', '1'], 
                    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'], 
                    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]
        
      elif Size == 19:
        BoardScore= [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
                    ['1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '2', '1'],
                    ['1', '2', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '6', '6', '6', '6', '6', '6', '6', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '7', '7', '7', '7', '7', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '8', '8', '8', '8', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '9', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '8', '8', '8', '8', '8', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '7', '7', '7', '7', '7', '7', '7', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '6', '6', '6', '6', '6', '6', '6', '6', '6', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '4', '3', '2', '1'],
                    ['1', '2', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '3', '2', '1'],
                    ['1', '2', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '2', '1'],
                    ['1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1'],
                    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]
      return BoardScore

    def Undo_Move(Size, Board, Temp_Board, Turn_Count, Turn):
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Size)
        Board = []
        
        for Count1 in range (Size):
            BoardRow = []
            for Count2 in range (Size):
                if Temp_Board[Count1][Count2] == 'O':
                  BoardPosition = 'O'
                elif Temp_Board[Count1][Count2] == 'X':
                  BoardPosition = 'X'
                else:
                  BoardPosition = ' '
                BoardRow.append(BoardPosition)
            Board.append(BoardRow)
            
        Turn_Count, Turn = Game.Player_Turn (Turn_count, Turn)
        if Size == 15:
            for i in range (Size):
                for j in range (Size):
                    if Temp_Board[i][j] == 'X':
                      pygame.draw.circle(screen, P1COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                      pygame.display.flip()
                    elif Temp_Board[i][j] == 'O':
                      pygame.draw.circle(screen, P2COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                      pygame.display.flip()
        elif Size == 19:
            for i in range (Size):
                for j in range (Size):
                    if Temp_Board[i][j] == 'X':
                      pygame.draw.circle(screen, P1COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                      pygame.display.flip()
                    elif Temp_Board[i][j] == 'O':
                      pygame.draw.circle(screen, P2COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                      pygame.display.flip()
        return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn
      
    def Player_Turn (Turn_count, Turn):
      if Turn_count == 0 and not CPU:
        if random.randint(0,1) == 1:  
          Turn = 1
        else:
            Turn = 2
      elif Turn_count == 0 and CPU:
          Turn = 1
      else:
        if Turn == 1:
            Turn = 2
        elif Turn == 2:
            Turn = 1
      Turn_count += 1

      pygame.draw.rect(screen, SCREEN_COLOUR, (650, 115, 550, 90), 0)
      TURNT0 = FONT75.render('Player ' + str(Turn)  + 's turn: ', True, BLACK)
      TURNRect0 = TURNT0.get_rect()
      TURNRect0.center = (925, 155)
      screen.blit(TURNT0, TURNRect0)
      pygame.display.flip()

      return Turn_count, Turn

    def Update_Board(Turn, XIndex, YIndex):
      if Turn == 1:
        Colour = P1COLOUR
      else:
        Colour = P2COLOUR
        
      if Size == 15:
        pygame.draw.circle(screen, Colour, (XIndex*35 + 610, YIndex* 35 + 313), 15, 0)
      else:
        pygame.draw.circle(screen, Colour, (XIndex*30 + 580, YIndex* 30 + 290), 12, 0)
      pygame.display.flip()

    def Win_Check(Board, Size):
      for x in range (0, Size):
        for y in range (0, Size):
            try:
              if Board[x-2][y] == Board[x-1][y] == Board[x][y] == Board[x+1][y] == Board [x+2][y] != ' ':
                return True
            except:
               pass
            
            try:
              if Board[x][y-2] == Board[x][y-1] == Board[x][y] == Board[x][y+1] == Board [x][y+2] != ' ':
                return True
            except:
               pass
            
            try:
              if Board[x-2][y-2] == Board[x-1][y-1] == Board[x][y] == Board[x+1][y+1] == Board [x+2][y+2] != ' ':
                return True
            except:
               pass
            
            try:
              if Board[x-2][y+2] == Board[x-1][y+1] == Board[x][y] == Board[x+1][y-1] == Board [x+2][y-2] != ' ':
                return True
            except:
               pass
      return False
          
    def Check_Draw(Board, Size):
      for x in range (Size):
        for y in range (Size):
          if Board[x][y] == ' ':
             return False
      return True

TextInputGroup = CustomGroup()
TextInputList = []

Player_1 = humanPlayer()
Player_2 = humanPlayer()
Ai_player = computerPlayer()

X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Menu()

while True:
    mouse_pos = pygame.mouse.get_pos()
    if (AI_turn and Updated) == True:
              Updated = False
              Best_move, Max_score  = Ai_Move(Board, 4, float('-inf'), float('inf'), True)
              Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = Ai_player.move(Turn, Turn_count, Board, Best_move[0], Best_move[1], Temp_Board, CPU, HeatMap, HeatTruth)
              Board[Best_move[0]][Best_move[1]] = 'O'
              AI_turn = False

    for event in pygame.event.get():
        if event.type == pygame.quit:
            pygame.quit()
            sys.exit
           
        if event.type == pygame.MOUSEBUTTONDOWN:
            for textinput in TextInputGroup:
                if textinput.clicked(mouse_pos):
                    if TextInputGroup.current:
                        TextInputGroup.current.isSelected = False
                    textinput.isSelected = True
                    TextInputGroup.current = textinput
                    break
                  
            for i in range (int(len(X_LIST)/2)):
                if (X_LIST[2*i] <= mouse_pos[0] <= X_LIST[2*i+1]) and (Y_LIST[2*i] <= mouse_pos[1] <= Y_LIST[2*i+1]):
                     Next = BUTTON_LIST[i]
                     if Next == 'AI_opponent':
                        Ai_player = computerPlayer()
                        CPU = True
                        
                     if Next == 'Rules':
                        Drawing.Clean()
                        temp = Identifier
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Redraw = Drawing.Rules(temp)
                        if Redraw:
                           if Size == 15:
                            for i in range (Size):
                                for j in range (Size):
                                    if Temp_Board[i][j] == 'X':
                                      pygame.draw.circle(screen, P1COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                                      pygame.display.flip()
                                    elif Temp_Board[i][j] == 'O':
                                      pygame.draw.circle(screen, P2COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                                      pygame.display.flip()
                           elif Size == 19:
                            for i in range (Size):
                                for j in range (Size):
                                    if Temp_Board[i][j] == 'X':
                                      pygame.draw.circle(screen, P1COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                                      pygame.display.flip()
                                    elif Temp_Board[i][j] == 'O':
                                      pygame.draw.circle(screen, P2COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                                      pygame.display.flip()
                        break
                     elif Next == 'Replay':
                        if Turn == 1:
                            P1SCORE += 1
                        else:
                            P2SCORE += 1
                        Drawing.Clean()
                        Line_Check = False
                        Board = []
                        HeatMap = []
                        HeatTruth = []
                        Turn_count = 0
                        if CPU:
                           AI_turn = False
                           Updated = False
                        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn)
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Program()
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Size)
                        break
                     else:
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size, Board, Turn, Turn_count, CPU = Game.Draw_Next(Next, Size, Temp_Board, Board, Turn, Turn_count, CPU)
                        break

            if not Line_Check:
              Updated = False
              if Identifier == 'GAME' and CPU:
                 if Turn == 1:
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_1.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)

                    if not Line_Check: AI_turn = True

              elif Identifier == 'GAME' and not CPU:
                 if Turn == 1:
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_1.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)
                 elif Turn == 2:
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_2.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                TextInputGroup.current.update_text(TextInputGroup.current.text_value[:-1])
                
            if event.key == pygame.K_RETURN:
                if TextInputGroup.current:
                    TextInputList.append(TextInputGroup.current.text_value)

                    if TextInputGroup.current.text_value != '':
                        if Identifier == 'NAMES':
                            Player_1 = humanPlayer()
                            X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.P2_Name()

                        elif TextInputGroup.current.text_value != TextInputList[0]:
                            Player_2 = humanPlayer()
                            TextInputList.append(TextInputGroup.current.text_value)
                            Drawing.Clean()
                            X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()
                        else:
                            Drawing.Fail('Name')
                    else:
                       Drawing.Fail('Empty')

        if event.type == pygame.USEREVENT: 
          if Identifier == 'GAME':
            Seconds += 1
            if Seconds == 60:
              Minutes += 1
              Seconds = 0
          else:
            Seconds = 0
            Minutes = 0
                
        if event.type == pygame.TEXTINPUT:
            Current_text = TextInputGroup.current.update_text(TextInputGroup.current.text_value + event.text)
    for textinput in TextInputGroup:
        textinput.update(mouse_pos)
        textinput.render(screen)
    if TextInputGroup.current and TextInputGroup.current.bg.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(ibeam)
    else:
        pygame.mouse.set_cursor(pygame.cursors.Cursor())
        
    if Identifier == 'GAME':
      pygame.draw.rect(screen, SCREEN_COLOUR, (120, 150, 260, 50), 0)
      MAINT0 = FONT75.render('Timer: ' + str(Minutes) + ':' + str(Seconds), True, BLACK)
      MAINRect0 = MAINT0.get_rect()
      MAINRect0.center = (235, 175)
      screen.blit(MAINT0, MAINRect0)
      pygame.display.flip()
    pygame.display.update()