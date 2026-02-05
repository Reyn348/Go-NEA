from Globals import *
import sys
import random
import math
import numpy
from abc import ABC

class TextInput(pygame.sprite.Sprite):
    def __init__(self, x, y, Width=100, Height=50, Colour= BLACK, bgcolour=WHITE, SelectedColour=(190,195,198)):
        super().__init__()
        self.Text_value = ''
        self.Selected = False
        self.Colour = Colour
        self.bgcolour = bgcolour
        self.SelectedColor = SelectedColour
        self.Font = FONT40
        self.Text = self.Font.render(self.Text_value, True, self.Colour)
        self.bg = pygame.Rect(x, y, Width, Height)
       
    def clicked(self, mousePos): #determine if textbox has been selected
        if self.bg.collidepoint(mousePos):
            self.Selected = not(self.Selected)
            return True
        return False
       
    def update_text(self, new_text): #change text as it is entered
        temp = self.Font.render(new_text, True, self.Colour)
        if temp.get_rect().width >= (self.bg.width - 20):
            return
        self.Text_value = new_text
        self.Text = temp
        return self.Text_value
       
    def render(self, display): #output text onto sreen
        self.pos = self.Text.get_rect(center = (self.bg.x + self.bg.width/2, self.bg.y + self.bg.height/2))
        if self.Selected:
            pygame.draw.rect(display, self.SelectedColor, self.bg)
        else:
            pygame.draw.rect(display, self.bgcolour, self.bg)
        display.blit(self.Text, self.pos)
       
class CustomGroup(pygame.sprite.Group): #allow for textboxes to be made with ease
    def __init__(self):
        super().__init__()
        self.current = None
       
    def current(self):
        return self.current
  
class basePlayer(ABC):
   def __init__(self):
      pass
   
   def move(self, Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth): #allows for player moves to be made
      Temp_Board = numpy.copy(Board) #just for the undo function
      Updated = False

      if not (CPU and Turn == 2):
        if Size == 15: #calculate what position in the board is being selected for player moves
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
            YIndex = math.ceil(y/38)

      else: #CPU directly enters coordinates, so skip calculation
         XIndex = x
         YIndex = y

      if Board[XIndex][YIndex] == ' ':
        if Turn == 1: #standardise which player is which piece, simply differentiates between the two
            Board[XIndex][YIndex] = 'X'
        else:
            Board[XIndex][YIndex] = 'O'  

        Game.Update_Board(Turn, XIndex, YIndex) #update screen wtith move
        HeatMap = Minimax.Update_HeatMap(HeatMap, [XIndex, YIndex], HeatTruth) #ensure the heatmap is accurate
        Line_Check = Game.Win_Check(Board, Size) #check is someone has won
        Updated = True #screen has been updated, used to determine if Ai should make a move

        if Line_Check:
          X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Winner(Turn) #output winner
          return Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier
        
        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn) #if no winner, switch to next turn
      return Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, [140, 360, 1175, 1275], [650, 740, 510, 610], ['Rules', 'Undo'], 'GAME' #return specific values here to avoid them being updated needlessly
   
   def Move_calc(self, Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth):
        Updated = False #no valid move has been entered yet

        if Size == 15:
            x = (mouse_pos[0]-610) #take mouse position and calculate if it is in the Board (based on the size of the board itself)
            y = (mouse_pos[1]-313)
            if(x % 35 <= 10 or x % 35 >= 25) and (y % 35 <= 10 or y % 35 >= 25) and (-10 <= x <= 500 and -10 <= y <= 500): #if close enough to the position, make move
                Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = self.move(Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth)
                Line_Check = Game.Win_Check(Board, Size) #recheck here to return
                return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
            
            else: #otherwise, do nothing
               return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
          
        elif Size == 19: #exact same with slightly different calculations
            x = (mouse_pos[0]-580)
            y = (mouse_pos[1]-290)
            if (x % 30 <= 10 or x % 30 >= 20) and (y % 30 <= 10 or y % 30 >= 20) and (-10 <= x <= 600 and -10<= y <+ 600):
                Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = self.move(Turn, Turn_count, Board, x, y, Temp_Board, CPU, HeatMap, HeatTruth)
                Line_Check = Game.Win_Check(Board, Size)
                return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap
            
            else:
               return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap

#classes are mainly used as a convenience for grouping functions and differentiating objects, the following classes and functions in them rely on global variables
#as such using a self list in these classes would be more inconvenient than not, which is why the inits are empty
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
   
  def Main_Menu(self): #draw main menu
      for i in range (5): #iteration here is easier + saves extra lines in main program
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
      X_LIST = [395, 1045, 445, 995, 590, 850] #button lists line up with coordinate lists
      Y_LIST = [270, 370, 420, 520, 600, 700] #e.g. 'Rules' button has x values 590, 850 here
      BUTTON_LIST = ['AI_opponent','Player_name', 'Rules']
      Identifier = 'MENU' #current screen
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def Rules(self, temp): #draw rules screen
      Prev = '' #prev used to determine if game state needs to be redrawn
      for i in range (3):
        pygame.draw.rect(screen, WHITE, (RULES_RECT[i]), 4)
        pygame.display.flip()

      RULEST0 = FONT100.render('The Rules', True, BLACK)
      RulesRect0 = RULEST0.get_rect()
      RulesRect0.center = (180, 50)
      screen.blit(RULEST0, RulesRect0)
      
      RULEST1 = FONT55.render('•   Gomoku is played on either a 15 x 15 or 19 x 19 square board', True, BLACK)
      RulesRect1 = RULEST1.get_rect()
      RulesRect1.center = (720, 220)
      screen.blit(RULEST1, RulesRect1)
      
      RULEST2 = FONT55.render('•   The first player is random, and players alternate in placing a', True, BLACK)
      RulesRect2 = RULEST2.get_rect()
      RulesRect2.center = (720, 325)
      screen.blit(RULEST2, RulesRect2)
      
      RULEST3 = FONT55.render('stone of their colour on an empty intersection. ', True, BLACK)
      RulesRect3 = RULEST3.get_rect()
      RulesRect3.center = (720, 365)
      screen.blit(RULEST3, RulesRect3)
      
      RULEST4 = FONT55.render('•   The winner is the first player to form an unbroken chain of', True, BLACK)
      RulesRect4 = RULEST4.get_rect()
      RulesRect4.center = (720, 470)
      screen.blit(RULEST4, RulesRect4)
      
      RULEST5 = FONT55.render('five stones horizontally, vertically, or diagonally. ', True, BLACK)
      RulesRect5 = RULEST5.get_rect()
      RulesRect5.center = (720, 510)
      screen.blit(RULEST5, RulesRect5)

      RULEST6 = FONT55.render('•   Once placed, stones cannot be moved or removed from the', True, BLACK)
      RulesRect6 = RULEST6.get_rect()
      RulesRect6.center = (720, 615)
      screen.blit(RULEST6, RulesRect6)
      
      RULEST6 = FONT55.render('board, however moves can be undone once per turn', True, BLACK)
      RulesRect6 = RULEST6.get_rect()
      RulesRect6.center = (720, 655)
      screen.blit(RULEST6, RulesRect6)
    
      RULEST7 = FONT55.render('within this program' , True, BLACK)
      RulesRect7 = RULEST7.get_rect()
      RulesRect7.center = (720, 695)
      screen.blit(RULEST7, RulesRect7)

      RULEST8 = FONT100.render('Return', True, BLACK)
      RulesRect8 = RULEST8.get_rect()
      RulesRect8.center = (1310, 850)
      screen.blit(RULEST8, RulesRect8)
      pygame.display.flip()
      
      X_LIST = [1200, 1440]
      Y_LIST = [800, 900]
      BUTTON_LIST = [temp]
      Identifier = 'RULES'
      if temp == 'GAME': #if page to return to is the game, update prev to redraw board
         Prev = 'Rules'
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Prev

  def P1_Name(self): #draw screen to get player one name
      pygame.draw.rect(screen, (SCREEN_COLOUR),(380, 235, 680, 540), 0)
      pygame.draw.rect(screen, WHITE, (380, 235, 680, 430), 4)
     
      TextInputGroup.add(TextInput(x=605, y=440, width = 230)) #create textbox to enter name into
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
      
      #no buttons, only inputs, hence lists empty (can't be ignored as that would result in lists from other screens carrying over)
      Identifier = 'NAMES'
      X_LIST = []
      Y_LIST = []
      BUTTON_LIST = []
      return X_LIST, Y_LIST, BUTTON_LIST, Identifier

  def P2_Name(self): #draw screen for player 2 name
      for current in TextInputGroup:
          TextInputGroup.remove(current) #get rid of old textbox
     
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

  def Main_Program(self): #draw bulk of the main game screen
      for i in range (5):
          pygame.draw.rect(screen, WHITE, MAIN_PROG_RECT[i], 4)
          pygame.display.flip()

      MAINT0 = FONT50.render('Player 1s score: ' + str(P1SCORE), True, BLACK) #update player scores
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

  def Board_Size(self): #draw screen to get baord size
      X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Program()
      for current in TextInputGroup:
          TextInputGroup.remove(current) #ensure no textboxes carry over from player names
     
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

  def Clean(self):
     screen.fill(SCREEN_COLOUR) #covers screen in background colour to reset it

  def Fail(self, error): #only used in player name get
      pygame.draw.rect(screen, (SCREEN_COLOUR), (450, 530, 540, 80), 0)
      pygame.draw.rect(screen, (WHITE), (415, 530, 610, 80), 4)
      pygame.display.flip()
      
      if error == 'Name': #error if names are the same
        FAILT0 = FONT55.render('ERROR: player names are same', True, BLACK)
        FAILRect0 = FAILT0.get_rect()
        FAILRect0.center = (720, 570)
        screen.blit(FAILT0, FAILRect0)
   
      elif error == 'Empty': #error if nothing is entered as a name
        FAILT1 = FONT55.render('ERROR: Invalid input', True, BLACK)
        FAILRect1 = FAILT1.get_rect()
        FAILRect1.center = (720, 570)
        screen.blit(FAILT1, FAILRect1)
      pygame.display.flip()
   
  def Game(self, Size): #draw main game (mostly board)
    Size = int(Size) #update size to be an int for future use
    pygame.draw.rect(screen, SCREEN_COLOUR, (500, 260, 900, 600), 0)
    pygame.draw.rect(screen, WHITE, (500, 260, 900, 585), 4)
    
    if Size == 15: #exact dimensions of board change with size to fit in better
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
    
    for Count1 in range (Size): #create 2D array for Board
        BoardRow = []
        for Count2 in range (Size):
            BoardPosition = ' '
            BoardRow.append(BoardPosition)
        Board.append(BoardRow)

    for Count1 in range (Size): #ceate 2D array for heatmap
        HeatRow = []
        for Count2 in range (Size):
            HeatValue = 0
            HeatRow.append(HeatValue)
        HeatMap.append(HeatRow)
 
    for Count1 in range (Size): #create 2D array to check if heat value has been updated already
        TruthRow = []
        for Count2 in range (Size):
            HeatBool = False
            TruthRow.append(HeatBool)
        HeatTruth.append(TruthRow)

    X_LIST = [140, 360, 1175, 1275]
    Y_LIST = [650, 740, 510, 610]
    BUTTON_LIST = ['Rules', 'Undo']
    Identifier = 'GAME'
    return X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size
  
  def Winner(self, Turn): #if someone wins, output who it was
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

    def Draw_Next(self, Next, Size, Temp_Board, Board, Turn, Turn_count, CPU, Prev): #send players down pre-determined set of screens based on choices  
      if Next == 'AI_opponent': #if player chooses 'Play vs Computer' on main screen
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()

      elif Next == 'Player_name': #if player chooses 'Play vs Human' on main screen
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.P1_Name()
        
      elif Next == '15' or Next == '19': #any time where board size has been chosen
        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn)
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Next)
        
      #elif Next == 'MENU':
       # Drawing.Clean()
       # X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Menu()
    
      elif Next == 'Undo': #if player chooses to undo a move
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn = Game.Undo_Move(Size, Board, Temp_Board, Turn_count, Turn)
      
      elif Next == 'Rules': #if player chooses to view rules on any screen
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Prev = Drawing.Rules(temp)

      elif Prev == 'Rules' and Next == 'GAME': #if returning from rules to running game
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Size)

        if Size == 15:
            for i in range (Size):
                for j in range (Size): #redraw current Board state, exact positions differ with board size
                    if Board[i][j] == 'X':
                        pygame.draw.circle(screen, P1COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                        pygame.display.flip()
                    elif Board[i][j] == 'O':
                        pygame.draw.circle(screen, P2COLOUR, (i*35 + 610, j* 35 + 313), 15, 0)
                        pygame.display.flip()

        elif Size == 19:
            for i in range (Size):
                for j in range (Size):
                    if Board[i][j] == 'X':
                        pygame.draw.circle(screen, P1COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                        pygame.display.flip()
                    elif Board[i][j] == 'O':
                        pygame.draw.circle(screen, P2COLOUR, (i*30 + 580, j* 30 + 290), 12, 0)
                        pygame.display.flip()

        Prev = '' #reset Prev to allow for rules to be re-visited
      else: #if no other check works, next screen must be finding board size
        Drawing.Clean()
        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size()
        
      return  X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size, Board, Turn, Turn_count, CPU, Prev #return all relevant potentially updated values

    def Undo_Move(self, Size, Board, Temp_Board, Turn_Count, Turn):
        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Size)
        Board = []
        
        for Count1 in range (Size): #updated board to previous position via Temp_Board
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
            
        Turn = Game.Player_Turn (Turn_count, Turn)[1] #set Turn back to previous value
        if Size == 15: #redraw Board based on previous Board state
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
      
    def Player_Turn (self, Turn_count, Turn):
      if Turn_count == 0 and not CPU:
        if random.randint(0,1) == 1:  #random starting player
          Turn = 1
        else:
            Turn = 2

      elif Turn_count == 0 and CPU: #if CPU player, human always goes first
          Turn = 1

      else:
        if Turn == 1: #alternate turns
            Turn = 2
        elif Turn == 2:
            Turn = 1

      Turn_count += 1

      pygame.draw.rect(screen, SCREEN_COLOUR, (650, 115, 550, 90), 0) #updated text box displaying current turn
      TURNT0 = FONT75.render('Player ' + str(Turn)  + 's turn: ', True, BLACK)
      TURNRect0 = TURNT0.get_rect()
      TURNRect0.center = (925, 155)
      screen.blit(TURNT0, TURNRect0)
      pygame.display.flip()

      return Turn_count, Turn

    def Update_Board(self, Turn, XIndex, YIndex):
      if Turn == 1: #determine which player is moving, and what colour piece to place
        Colour = P1COLOUR
      else:
        Colour = P2COLOUR
        
      if Size == 15: #place piece in chosen position, dimensions etc change with Board Size
        pygame.draw.circle(screen, Colour, (XIndex*35 + 610, YIndex* 35 + 313), 15, 0)

      else:
        pygame.draw.circle(screen, Colour, (XIndex*30 + 580, YIndex* 30 + 290), 12, 0)
      pygame.display.flip()

    def Win_Check(self, Board, Size):
      for x in range (0, Size):
        for y in range (0, Size):
            try: #iterate through full board, if 5 in a row found, return True and end game
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
    
    def Check_Draw(self, Board, Size):
      for x in range (Size): #if no possible moves left (no empty spaces in Board) draw is True
        for y in range (Size):
          if Board[x][y] == ' ':
             return False
      return True

class Minimax():
   def __init__(self):
       pass
   
    #Minimax algorithm with Alpha beta Pruning for finding the best move on the game board.
   def Ai_Move(self, Board, depth, alpha, beta, maximisingPlayer):
        valid_locations = Minimax.GetAvailableMoves(Size)
        if Game.Win_Check(Board, Size) or Game.Check_Draw(Board, Size): 
            is_terminal = True
        else: is_terminal = False

        #if depth is 0 or game ends, return score
        if depth == 0 or is_terminal:
            if is_terminal:
                if Game.Win_Check(Board, Size):
                    return (None, (1000000000 + depth) * (1 if maximisingPlayer else -1))
                else: #game tied, no moves left
                    return (None, 0)
            else: #depth is zero
                return (None, Minimax.Score_calc(Board, True) - Minimax.Score_calc(Board, False))
        
        Player_symbol = 'O' if maximisingPlayer else 'X'
        #maximizing player
        if maximisingPlayer:
            value = float('-inf')
            Best_move = [-1, -1]
            for move in valid_locations:
                Board[move[0]][move[1]] = Player_symbol
                if Game.Win_Check(Board, Size):
                    new_score = Minimax.Ai_Move(Board, depth, alpha, beta, True)[1]
                else:
                    new_score = Minimax.Ai_Move(Board, depth-1, alpha, beta, False)[1]
                Board[move[0]][move[1]] = ' '
    
                #update move and alpha
                if new_score > value:
                    value = new_score
                    Best_move = move
                alpha = max((alpha, value))
    
                #prune search
                if alpha >= beta:
                    break
            return Best_move, value
    
        else: #minimizing player
            value = float('inf')
            Best_move = [-1, -1]
            for move in valid_locations:
                Board[move[0]][move[1]] = Player_symbol
                if Game.Win_Check(Board, Size):
                    new_score = Minimax.Ai_Move(Board, depth, alpha, beta, False)[1]
                else:
                    new_score = Minimax.Ai_Move(Board, depth-1, alpha, beta, True)[1]
                Board[move[0]][move[1]] = ' '
    
                #update move and alpha
                if new_score < value:
                    value = new_score
                    Best_move = move
                beta = min((beta, value))
    
                #prune search
                if alpha >= beta:
                    break
            return Best_move, value
    
   def Open_row_search(self, Piece):
        best = 0
        #horizontal count
        for x in range (1, Size-4):
            for y in range (Size):
                    if Board[x][y] == Board[x+1][y] == Board[x+2][y] == Piece:
                        if Board[x-1][y] == Board[x+3][y] == ' ':
                            best += 10 #three in a row (unblocked)
                        elif Board[x+3][y] == Piece:
                            best += 1000 #four in a row
                            if Board[x-1][y] == Board[x+4][y] == ' ':
                                best += 10000 #four in a row unblocked (guarantees win)

        #vertical count
        for x in range (Size):
            for y in range (1, Size-4):
                    if Board[x][y] == Board[x][y+1] == Board[x][y+2] == Piece:
                        if Board[x][y-1] == Board[x][y+3] == ' ':
                            best += 10 #three in a row (unblocked)
                        elif Board[x][y+3] == Piece:
                            best += 1000 #four in a row
                            if Board[x][y-1] == Board[x][y+4] == ' ':
                                best += 10000 #four in a row unblocked (guarantees win)

        #left diagonal count
        for x in range (1, Size-4):
            for y in range (1, Size-4):
                    if Board[x][y] == Board[x+1][y+1] == Board[x+2][y+2] == Piece:
                        if Board[x-1][y-1] == Board[x+3][y+3] == ' ':
                            best += 10 #three in a row (unblocked)
                        elif Board[x+3][y+3] == Piece:
                            best += 1000 #four in a row
                            if Board[x-1][y-1] == Board[x+4][y+4] == ' ':
                                best += 10000 #four in a row unblocked (guarantees win)

        #right diagonal count
        for x in range (4, Size-1):
            for y in range (1, Size-4):
                    if Board[x][y] == Board[x-1][y+1] == Board[x-2][y+2] == Piece:
                        if Board[x+1][y-1] == Board[x-3][y+3] == ' ':
                            best += 10 #three in a row (unblocked)
                        elif Board[x-3][y+3] == Piece:
                            best += 1000 #four in a row
                            if Board[x+1][y-1] == Board[x-4][y+4] == ' ':
                                best += 10000 #four in a row unblocked (guarantees win)
        return best

   def Score_calc(self, Board, Max_turn): 
        Piece = 'O' if Max_turn else 'X' #determine which player's score is being counted
        Opponent = 'X' if Max_turn else 'O'
        best = 0
        best += Minimax.Open_row_search(Piece) #check for high priority lines
        #horizontal count
        for x in range (1, Size-3):
            for y in range (Size):
                if Board[x][y] == Board[x+1][y] == Piece or Board[x][y] == Board[x+1][y] == Opponent:
                    if Board[x+2][y] != Board[x][y]:
                        if Board[x][y] == Piece:
                            best += 1 #two in a row
                            if Board[x-1][y] or Board[x+2][y] == Opponent:
                                best -=1 #blocked
                        else:
                            best -= 1
                            if Board[x-1][y] or Board[x+2][y] == Piece:
                                best += 3 #hgih score prioritises blocking moves
                    else:
                        if Board[x][y] == Piece:
                            best += 2 #three in a row
                            if Board[x-1][y] or Board[x+3][y] == Opponent:
                                best -=1
                        else:
                            best -= 2 #blocked
                            if Board[x-1][y] or Board[x+3][y] == Piece:
                                best += 5 #prioritise stopping opponents strong moves
        #vertical count
        for x in range (Size):
            for y in range (1, Size-3):
                if Board[x][y] == Board[x][y+1] == Piece or Board[x][y] == Opponent:
                    if Board[x][y+2] != Board[x][y]:
                        if Board[x][y] == Piece:
                            best += 1
                            if Board[x][y-1] or Board[x][y+2] == Opponent:
                                best -=1
                        else:
                            best -= 1
                            if Board[x][y-1] or Board[x][y+2] == Piece:
                                best += 3
                    else:
                        if Board[x][y] == Piece:
                            best += 2
                            if Board[x][y-1] or Board[x][y+3] == Opponent:
                                best -=1
                        else:
                            best -= 2
                            if Board[x][y-1] or Board[x][y+3] == Piece:
                                best += 5
                #left diagonal count -x +y to +x -y
        for x in range (1, Size-3):
            for y in range (3, Size-1):
                if Board[x][y] == Board[x+1][y-1] == Piece or Board[x][y] == Board[x+1][y-1] == Opponent:
                    if Board[x+2][y-2] != Board[x][y]:
                        if Board[x][y] == Piece:
                            best += 1
                            if Board[x-1][y+1] or Board[x+2][y-2] == Opponent:
                                best -=1
                        else:
                            best -= 1
                            if Board[x-1][y+1] or Board[x+2][y-2] == Piece:
                                best += 3
                    else:
                        if Board[x][y] == Piece:
                            best += 2
                            if Board[x-1][y+1] or Board[x+3][y-3] == Opponent:
                                best -=1
                        else:
                            best -= 2
                            if Board[x-1][y+1] or Board[x+3][y-3] == Piece:
                                best += 5
                #right diagonal -x -y to +x +y
        for x in range (1, Size-3):
            for y in range (1, Size-3):
                if Board[x][y] == Board[x+1][y] == Piece or Board[x][y] == Board[x+1][y] == Opponent:
                    if Board[x+2][y+2] != Board[x][y]:
                        if Board[x][y] == Piece:
                            best += 1
                            if Board[x-1][y-1] or Board[x+2][y+2] == Opponent:
                                best -=1
                        else:
                            best -= 1
                            if Board[x-1][y-1] or Board[x+2][y+2] == Piece:
                                best += 3
                    else:
                        if Board[x][y] == Piece:
                            best += 2
                            if Board[x-1][y-1] or Board[x+3][y+3] == Opponent:
                                best -=1
                        else:
                            best -= 2
                            if Board[x-1][y-1] or Board[x+3][y+3] == Piece:
                                best += 5
        return best

   def GetAvailableMoves(self, Size):
        AvailableMoves = []
        for i in range (Size):
            for j in range (Size):
                if Board[i][j] == ' ': #is move taken
                    if HeatMap[i][j] > 0: #is move relevant to current gamestate
                        AvailableMoves.append([i, j, HeatMap[i][j]])
        AvailableMoves.sort(reverse=True, key = Minimax.get_Heat) #order moves on importance
        return AvailableMoves

   def Update_HeatMap(self, HeatMap, Move, HeatTruth):
        Move_X = Move[0]
        Move_Y = Move[1]
        HeatMap[Move_X][Move_Y] = -1 #ignore taken spaces

        for k in range (2): #create range around moves to update
            X_pos = min((14, Move_X + k))
            X_neg = max((0, Move_X - k))
            Y_pos = min((14, Move_Y + k))
            Y_neg = max((0, Move_Y - k))

            #if space not taken, and heat value not updated already, increase heat
            if HeatMap[X_pos][Y_pos] > -1 and not HeatTruth[X_pos][Y_pos]: HeatMap[X_pos][Y_pos] += 1; HeatTruth[X_pos][Y_pos] = True
            if HeatMap[X_pos][Y_neg] > -1 and not HeatTruth[X_pos][Y_neg]: HeatMap[X_pos][Y_neg] += 1; HeatTruth[X_pos][Y_neg] = True
            if HeatMap[X_neg][Y_pos] > -1 and not HeatTruth[X_neg][Y_pos]: HeatMap[X_neg][Y_pos] += 1; HeatTruth[X_neg][Y_pos] = True
            if HeatMap[X_neg][Y_neg] > -1 and not HeatTruth[X_neg][Y_neg]: HeatMap[X_neg][Y_neg] += 1; HeatTruth[X_neg][Y_neg] = True

        HeatTruth = Minimax.Reset_HeatTruth(HeatTruth) #reset to allow for updates later
        return HeatMap
 
   def Reset_HeatTruth(self, HeatTruth):
        for i in range (Size):
            for j in range (Size):
                HeatTruth[i][j] = False
        return HeatTruth #allows for updating heat again later on
 
   def Reset_HeatMap(self, HeatMap):
        for i in range (len(HeatMap)):
            for j in range (len(HeatMap)):
                HeatMap[i][j] = 0 #set heatmap to 0 for replays
        return HeatMap
 
   def get_Heat(self, list):
        return list[2] #returns heat value only

TextInputGroup = CustomGroup() #pre-define textboxes for later use
TextInputList = []

X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Menu() #start program before gameplay loop

while True: #main game loop
    mouse_pos = pygame.mouse.get_pos()
    if (AI_turn and Updated) == True: #run Ai calculation on every frame where it is the AI's turn, and the previous player move updated the board (two checks used for safety)
              Updated = False #reset updated to allow human turn
              Best_move, Max_score  = Minimax.Ai_Move(Board, 3, float('-inf'), float('inf'), True) #run minimax algorithm
              Board, Turn, Turn_count, Temp_Board, Updated, HeatMap, X_LIST, Y_LIST, BUTTON_LIST, Identifier = Ai_player.move(Turn, Turn_count, Board, Best_move[0], Best_move[1], Temp_Board, CPU, HeatMap, HeatTruth) #output calculated move
              Board[Best_move[0]][Best_move[1]] = 'O' #update board with move
              AI_turn = False #reset Ai_turn to allow human turn

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit pygame
            pygame.display.quit()
            pygame.quit()
            sys.exit()
           
        if event.type == pygame.MOUSEBUTTONDOWN:
            for textinput in TextInputGroup: #if clicking on a textbox, allow for text input
                if textinput.clicked(mouse_pos):
                    if TextInputGroup.current:
                        TextInputGroup.current.Selected = False
                    textinput.Selected = True
                    TextInputGroup.current = textinput
                    break
                  
            for i in range (0, len(BUTTON_LIST)): #iterate through possible buttons on a screen
                if (X_LIST[2*i] <= mouse_pos[0] <= X_LIST[2*i+1]) and (Y_LIST[2*i] <= mouse_pos[1] <= Y_LIST[2*i+1]): #if mouse position is within the bounds of a button
                     Next = BUTTON_LIST[i] #find button pressed
                     if Next == 'AI_opponent':
                        Player_1 = humanPlayer() #create one human player
                        Ai_player = computerPlayer() #create ai player
                        CPU = True #set to true to allow AI moves to be made properly
                        
                     if Next == 'Rules': #rules runs separately due to need to hold previous screen to return to
                        Drawing.Clean()
                        temp = Identifier
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Prev = Drawing.Rules(temp)
                        break
                     
                     elif Next == 'Replay': #if replaying game, extra changes are needed hence made separately
                        if Turn == 1: #update score based on who won
                            P1SCORE += 1
                        else:
                            P2SCORE += 1
                        Drawing.Clean() #reset screen

                        Line_Check = False #reset variables that have been changed and will need to be emptied/ returned to default
                        Board = []
                        HeatMap = []
                        HeatTruth = []
                        Turn_count = 0

                        if CPU:
                           AI_turn = False #ensure Ai cannot move first if playing aganst it
                           Updated = False

                        Turn_count, Turn = Game.Player_Turn(Turn_count, Turn) #create starting player
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Main_Program() #redraw all key parts of game screen
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size = Drawing.Game(Size)
                        break
                     
                     else: #otherwise go through pre-determined steps through menus
                        X_LIST, Y_LIST, BUTTON_LIST, Identifier, Size, Board, Turn, Turn_count, CPU, Prev = Game.Draw_Next(Next, Size, Temp_Board, Board, Turn, Turn_count, CPU, Prev)
                        break

            if not Line_Check: #if game still going
              Updated = False
              if Identifier == 'GAME' and CPU: #if ai player, make human move
                 if Turn == 1:
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_1.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)

                    if not Line_Check: AI_turn = True

              elif Identifier == 'GAME' and not CPU: #if no ai player
                 if Turn == 1: #make player move for the correct player
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_1.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)
                 elif Turn == 2:
                    X_LIST, Y_LIST, BUTTON_LIST, Identifier, Board, Turn, Turn_count, Temp_Board, Line_Check, Updated, HeatMap = Player_2.Move_calc(Board, Turn, Turn_count, Temp_Board, Line_Check, X_LIST, Y_LIST, BUTTON_LIST, Identifier, HeatMap, HeatTruth)
                
        if event.type == pygame.KEYDOWN: #if entering text
            if event.key == pygame.K_BACKSPACE: #delete text
                TextInputGroup.current.update_text(TextInputGroup.current.text_value[:-1])
                
            if event.key == pygame.K_RETURN: #take text as an input
                if TextInputGroup.current:
                    TextInputList.append(TextInputGroup.current.text_value)

                    if TextInputGroup.current.text_value != '': #if text entered
                        if Identifier == 'NAMES': #if player one name was just gotten
                            Player_1 = humanPlayer() #create player
                            X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.P2_Name() #get player two name

                        elif TextInputGroup.current.text_value != TextInputList[0]: #fi player two name entered and not the same as P1
                            Player_2 = humanPlayer() #create player
                            TextInputList.append(TextInputGroup.current.text_value)
                            Drawing.Clean()
                            X_LIST, Y_LIST, BUTTON_LIST, Identifier = Drawing.Board_Size() #move to getting board size
                        else:
                            Drawing.Fail('Name') #if name are same, output error
                    else:
                       Drawing.Fail('Empty') #if no name entered, output error

        if event.type == pygame.USEREVENT:  #constantly updated timer
          if Identifier == 'GAME':
            Seconds += 1

            if Seconds == 60: #if minute passes, update timer as such
              Minutes += 1
              Seconds = 0

          elif Identifier == 'RULES':
              pass #if in rules, pause timer
          else: #if not in a game actively, reset timer
            Seconds = 0
            Minutes = 0
                
        if event.type == pygame.TEXTINPUT: #update text if needed
            Current_text = TextInputGroup.current.update_text(TextInputGroup.current.text_value + event.text)
    for textinput in TextInputGroup:
        textinput.update(mouse_pos)
        textinput.render(screen)

    if TextInputGroup.current and TextInputGroup.current.bg.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(ibeam) #if typing, change cursor type
    else:
        pygame.mouse.set_cursor(pygame.cursors.Cursor()) #otherwise use default
        
    if Identifier == 'GAME': #constantly update output timer
      pygame.draw.rect(screen, SCREEN_COLOUR, (95, 150, 290, 50), 0)
      MAINT0 = FONT75.render('Timer: ' + str(Minutes) + ':' + str(Seconds), True, BLACK)
      MAINRect0 = MAINT0.get_rect()
      MAINRect0.center = (235, 175)
      screen.blit(MAINT0, MAINRect0)
      pygame.display.flip()
      
    pygame.display.update()