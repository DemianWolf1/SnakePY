import pygame
from pygame.locals import * 
pygame.init()
W, H = 480, 320
screen = pygame.display.set_mode((W, H))
CELL_SIZE = 10
COL_COUNT = W // CELL_SIZE
ROW_COUNT = H // CELL_SIZE
image = 'images/part.png'
class Snake:
    def __init__(self, img):
        self.image = pygame.image.load(img)
        self.body = [[COL_COUNT // 2,ROW_COUNT // 2],\
                    [COL_COUNT // 2 + 1,ROW_COUNT // 2 + 1],\
                     [COL_COUNT // 2 + 2,ROW_COUNT // 2 + 2]]
        pass
    def move(self):
        pass
    def eat(self):
        pass
    def draw(self):
        pass
class Apple:
    def __init__(self):
        pass
    def draw(self):
        pass
#hero = Snake(image)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            pass
        
