import pygame
import random
import os
from pygame.locals import * 
pygame.init()
W, H = 480, 320
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SnakePY 1.0dev0")
CELL_SIZE = 32
COL_COUNT = W // CELL_SIZE
ROW_COUNT = H // CELL_SIZE
startimage = "data/images/snake/orange.png"
class Snake:
    def __init__(self, img):
        self.image = pygame.image.load(img)
        self.body = [[COL_COUNT // 2, ROW_COUNT // 2],\
                    [COL_COUNT // 2, ROW_COUNT // 2 + 1],\
                     [COL_COUNT // 2, ROW_COUNT // 2 + 2]]
        self.direction = [0, -1]
        self.velocity = 5
    def set_direction(self, key):
        if key == pygame.K_LEFT:
            self.direction = [-1, 0]
        elif key == pygame.K_RIGHT:
            self.direction = [1, 0]
        elif key == pygame.K_UP:
            self.direction = [0, -1]
        elif key == pygame.K_DOWN:
            self.direction = [0, 1]
    def move(self):
        self.body.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
        self.body.pop() # убираем хвост
        self.image = pygame.image.load("data/images/snake/" + random.choice(("black.png", "dblue.png", "green.png", "lblue.png", "orange.png", "red.png", "violet.png")))
    def eat(self):
        pass
    def draw(self):
        for elem in self.body:
            screen.blit(self.image, (elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

class Apple:
    def __init__(self):
        pass
    def draw(self):
        pass


snake = Snake(startimage)
pygame.time.set_timer(31, 100) # задаём таймер на движение (ID=31, ms=100)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            snake.set_direction(event.key)
        elif event.type == 31: # обрабатываем таймер на движение
            snake.move()
    screen.fill((0, 0, 0))
    snake.draw()
    pygame.time.wait(100)
    pygame.display.flip()
