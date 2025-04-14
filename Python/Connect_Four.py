import pygame
from pygame.locals import *
import sys

# model

class Game:
    def __init__(self):
        self.a = [8 * [0] for _ in range(7)]   # 7 x 6 array: 0 = empty, 1 = X, 2 = O
        self.turn = 1    # whose turn it is to play
        self.winner = 0  # player who has won, or 0 = nobody has won yet
        self.winning_squares = []

    def All(self, x, y, dx, dy):
        a = self.a
        if a[x][y] > 0 and a[x][y] == a[x + dx][y + dy] == a[x + 2 * dx][y + 2 * dy] == a[x + 3 * dx][y + 3 * dy]:
            self.winner = a[x][y]
            self.winning_squares = [(x + i * dx, y + i * dy) for i in range(4)]

    def check_win(self):
      for i in range(0,4,1): 
        for j in range(0,6,1):
          if (self.All(i,j,1,0) == True):
            return True
      for i in range (0,8,1):
        for j in range(0,7,1):
          if (self.All(j,i,0,1) == True):
            return True
      for j in range (0,4,1):
        for i in range (0,3,1):
          if (self.All(j,i,1,1) == True):
            return True
      for i in range (0,4,1):
        for j in range(3,6,1):
          if (self.All(i,j,1,-1) == True):
            return True
      return False
   
    def play(self, x, y):
        if self.a[x][y] == 0:   # square is available
            self.a[x][y] = self.turn   # place red or yellow
            self.turn = 3 - self.turn  # switch players
            self.check_win()

# view

Black = (0, 0, 0)
Green = (0, 255, 0)
White = (255, 255, 255)
Blue = (0, 0, 128)
Red = (255,   0,   0)
Yellow = (255, 255,   0)

Square = 70    # square size in pixels
Margin = Square//4     # margin size in pixels
BoardSize = 7 * Square + 6 * Margin
def draw(game, surface):
    surface.fill(White)
    pygame.draw.rect(surface, Blue, (Margin ,Margin, 7*Square,6*Square))
    for x in range(Margin + Square//2, Margin + 7*Square, Square):
      for y in range(Margin+Square//2, Margin + 6*Square, Square):
        pygame.draw.circle(surface, White, (x, y), (Square-20)//2 , 0)
   
    for x, y in game.winning_squares:
        pygame.draw.rect(surface, Green,
                         (Margin + x * Square + 2, Margin + y * Square + 2, Square - 4, Square - 4))
    for x in range(0, 7):
        for y in range(0, 6):
            pos_x, pos_y = Margin + x * Square, Margin + y * Square
            if game.a[x][y] == 1:    # draw red
                pygame.draw.circle(surface, Red,(pos_x + Square // 2, pos_y + Square // 2), (Square -20)//2, 0)
            elif game.a[x][y] == 2:   # draw  yellow
                  pygame.draw.circle(surface, Yellow,(pos_x + Square // 2, pos_y + Square // 2), (Square -20)//2,0)  

game = Game()

pygame.init()
surface = pygame.display.set_mode((BoardSize, BoardSize))
pygame.display.set_caption('Connect Four')
redraw = True

while True:
    if redraw:
        draw(game, surface)
        pygame.display.update()
        redraw = False
   
    event = pygame.event.wait()
    if event.type == QUIT:
        sys.exit()
    if event.type == MOUSEBUTTONDOWN:
        if game.winner > 0:
            game = Game()       # start a new game
            redraw = True
        else:
            pos_x, pos_y = event.pos
            play_x = int((pos_x - Margin) / Square)
            if (game.a[play_x][0] == 0):
              for y in range (0,6,1):
                if (game.a[play_x][y] != 0):
                  game.play(play_x,y-1)
                  redraw = True
            game.play(play_x,5)
            redraw = True
