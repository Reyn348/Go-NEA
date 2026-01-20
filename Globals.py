import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.display.set_caption('Gomoku')
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

Time = pygame.time.get_ticks()

#allow for different cursors
ibeam = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM)

#screen globals
SIZE = (1440, 900)
SCREEN_COLOUR = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#create screen
screen = pygame.display.set_mode(SIZE)
screen.fill(SCREEN_COLOUR)

#game globals
Time = pygame.time.get_ticks()
Size = 0
Board = []
Temp_Board = []
HeatMap = []
HeatTruth = []
BoardScore = []
Turn_count = 0
Difficulty = ''
Turn = 0
Seconds = 0
Minutes = 0
Depth = 0
Line_Check = False
AI_turn = False
Updated = False

#player gloabls
P1SCORE = 0
P2SCORE = 0
P1COLOUR = (66, 58, 214) #blue
P2COLOUR = (66, 143, 78) #green
CPU = False

#allow for different cursors
ibeam = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM)

#create screen
screen = pygame.display.set_mode(SIZE)
screen.fill(SCREEN_COLOUR)

#lists for drawing GUI
MAIN_MENU_RECT = [pygame.Rect(0, 0, 400, 100),
                  pygame.Rect(520, 100, 400, 100),
                  pygame.Rect(395, 270, 650, 100),
                  pygame.Rect(445, 420, 550, 100),
                  pygame.Rect(590, 600, 260, 100)
                  ]
                  
RULES_RECT = [pygame.Rect(0, 0, 360, 100),
              pygame.Rect(35, 150, 670, 650),
              pygame.Rect(770, 150, 620, 300),
              pygame.Rect(770, 500, 620, 300),
              pygame.Rect(1200, 800,240, 100)
              ]
              
CPU_DIFF_RECT = [pygame.Rect(420, 250, 600, 80),
                 pygame.Rect(545, 370, 350, 90),
                 pygame.Rect(545, 500, 350, 90),
                 pygame.Rect(545, 630, 350, 90)
                 ]
                 
NAMES_GET_RECT = [pygame.Rect(395, 250, 650, 90),
                  pygame.Rect(540, 360, 360, 70),
                  pygame.Rect(450, 530, 540, 80)
                  ]
                  
BOARD_SIZE_RECT = [pygame.Rect(835, 540, 180, 60),
                   pygame.Rect(835, 620, 180, 60)
                   ]
                   
MAIN_PROG_RECT = [pygame.Rect(100, 130, 300, 90),
                  pygame.Rect(50, 350, 400, 150),
                  pygame.Rect(140, 650, 220, 90),
                  pygame.Rect(625, 100, 600, 110),
                  pygame.Rect(600, 400, 650, 340)
                  ]
                  

#all font sizes
FONT100 = pygame.font.SysFont('freesanbold.ttf', 100)
FONT75 = pygame.font.SysFont('freesanbold.ttf', 75)
FONT68 = pygame.font.SysFont('freesanbold.ttf', 68)
FONT65 = pygame.font.SysFont('freesanbold.ttf', 65)
FONT55 = pygame.font.SysFont('freesanbold.ttf', 55)
FONT53 = pygame.font.SysFont('freesanbold.ttf', 53)
FONT50 = pygame.font.SysFont('freesanbold.ttf', 50)
FONT40 = pygame.font.SysFont('freesanbold.ttf', 40)