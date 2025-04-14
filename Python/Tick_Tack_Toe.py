import pygame
from pygame.locals import *
import sys
import random


# model
class Game:
    def __init__(self):
        self.a = [3 * [0] for _ in range(3)]   # 3 x 3 array: 0 = empty, 1 = X, 2 = O
        self.turn = 1    # whose turn it is to play
        self.winner = 0  # player who has won, or 0 = nobody has won yet, or 3 = draw
        self.winning_squares = []
        self.index = 0

    def clean (self):
      self.winner = 0
      self.winning_squares = []
      self.turn = 1

    def _check_win(self, x, y, dx, dy):
        
        a = self.a
        if a[x][y] > 0 and a[x][y] == a[x + dx][y + dy] == a[x + 2 * dx][y + 2 * dy]:
            self.winner = a[x][y]
            self.winning_squares = [(x + i * dx, y + i * dy) for i in range(3)]
            return True
        return False

    def check_win(self):
        for i in range(3):
            if (self._check_win(0, i, 1, 0) or self._check_win(i, 0, 0, 1)):
              return True 
        return (self._check_win(0, 0, 1, 1) or self._check_win(2, 0, -1, 1))

    def playAI(self):
      for x in range(3):    #checks if can win
        for y in range(3):
          if (self.a[x][y] == 0):
            self.a[x][y] = 2
            if (self.check_win()):
              self.index = 0
              return
            else:
              self.a[x][y] = 0              
      for x in range(3):    #checks if can block
        for y in range(3):
          if (self.a[x][y] == 0):
            self.a[x][y] = 1
            if (self.check_win()):
              self.clean()
              self.a[x][y] = 2
              return
            else:
              self.a[x][y] = 0

      while True:       #chooses random position
        xNew = random.randint(0,2)
        yNew = random.randint(0,2)
        if (self.a[xNew][yNew] == 0):
          break
      self.a[xNew][yNew] = 2
      self.turn = 1
      if (self.check_win()):
        return
      else:
        self.turn = 1
      
    def play(self, x, y):
      if (self.turn == 1):
        if self.a[x][y] == 0:
          self.a[x][y] = 1
          self.index += 1   #counts how many times player 1 played
          if (self.index == 5): #player 1 can play maximum 5 times 
            self.index = 0
            self.winner = 3  #draw
            return
          if (self.check_win()):
            self.index = 0  
            return
          else:
            self.turn = 2
    
   
# view

Black = (0, 0, 0)
Green = (0, 255, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255) 
Yellow = ((255,255,0))

Margin = 50     # margin size in pixels
Square = 100    # square size in pixels
BoardSize = 3 * Square + 2 * Margin


pygame.init()
screen = pygame.display.set_mode((640, 240))
font1 = pygame.font.SysFont('You WON!', 72)
img1 = font1.render('You WON!', True, Blue)
font2 = pygame.font.SysFont('You Lost!', 72)
img2 = font2.render('You Lost!', True, Red)
font3 = pygame.font.SysFont('Draw', 72)
img3 = font3.render('Draw', True, Yellow)

def draw(game, surface):
    surface.fill(White)
    for x in range(Margin, Margin + 4 * Square, Square):
        pygame.draw.line(surface, Black, (x, Margin), (x, BoardSize - Margin))  # vertical line
        pygame.draw.line(surface, Black, (Margin, x), (BoardSize - Margin, x))  # horizontal line

    if (game.winner == 1): #won the game
      
      screen.blit(img1, (20, 7))
      pygame.display.update()

    if (game.winner == 2): #lost the game
      
      screen.blit(img2, (20, 7))
      pygame.display.update()
    
    if (game.winner == 3): #draw
      screen.blit(img3, (20, 7))
      pygame.display.update()
      game.turn = 1

    for x, y in game.winning_squares:
      pygame.draw.rect(surface, Green,
                         (Margin + x * Square + 2, Margin + y * Square + 2, Square - 4, Square - 4))
  
    for x in range(0, 3):
        for y in range(0, 3):
            pos_x, pos_y = Margin + x * Square, Margin + y * Square
            if game.a[x][y] == 1:    # draw an X
                pygame.draw.line(surface, Blue,
                                 (pos_x + 10, pos_y + 10),
                                 (pos_x + Square - 10, pos_y + Square - 10), 4)
                pygame.draw.line(surface, Blue,
                                 (pos_x + Square - 10, pos_y + 10),
                                 (pos_x + 10, pos_y + Square - 10), 4)
            elif game.a[x][y] == 2:   # draw an O
                pygame.draw.circle(surface, Red,
                                   (pos_x + Square // 2, pos_y + Square // 2),   # center
                                   (Square - 20) // 2,   # radius
                                   3)    # width

game = Game()

pygame.init()
surface = pygame.display.set_mode((BoardSize, BoardSize))
pygame.display.set_caption('tic tac toe')
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
    if game.winner == 0:
      pos_x, pos_y = event.pos
      play_x, play_y = int((pos_x - Margin) / Square), int((pos_y - Margin) / Square)
      if 0 <= play_x < 3 and 0 <= play_y < 3:     # valid square
        game.play(play_x, play_y)
        redraw = True
    else:  
      game = Game()       # start a new game
      redraw = True

  if game.turn == 2 and game.winner == 0:
    game.playAI()
    redraw = True
