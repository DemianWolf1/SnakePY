import pygame
import random
import sys
from pygame.locals import *


pygame.init()
W, H = 480, 320
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SnakePY 1.0dev1")
CELL_SIZE = 32
COL_COUNT = W // CELL_SIZE
ROW_COUNT = H // CELL_SIZE
startimage = "data/images/snake/white.png"


class Snake: # Snake Object Class
    def __init__(self, img):
        self.image = pygame.image.load(img)
        self.body = [[COL_COUNT // 2, ROW_COUNT // 2],
                     [COL_COUNT // 2, ROW_COUNT // 2 + 1],
                     [COL_COUNT // 2, ROW_COUNT // 2 + 2]]
        self.direction = [0, -1]
        self.oldkey = K_UP
        self.score = 0

    def set_direction(self, key):
        opposite = {K_LEFT: K_RIGHT, K_RIGHT: K_LEFT, K_UP: K_DOWN, K_DOWN: K_UP}
        if opposite[self.oldkey] != key: 
            if key == pygame.K_LEFT:
                self.direction = [-1, 0]
                self.oldkey = K_LEFT
            elif key == pygame.K_RIGHT:
                self.direction = [1, 0]
                self.oldkey = K_RIGHT
            elif key == pygame.K_UP:
                self.direction = [0, -1]
                self.oldkey = K_UP
            elif key == pygame.K_DOWN:
                self.direction = [0, 1]
                self.oldkey = K_DOWN


    def move(self):
        self.body.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
        self.body.pop() # убираем хвост
        self.image = pygame.image.load("data/images/snake/" + random.choice(("white.png", "dblue.png", "green.png", "lblue.png", "orange.png", "red.png", "violet.png")))

    def eat(self):
        screen.fill((0, 0, 0))
        self.score += 1
        self.body.append([COL_COUNT // 2, ROW_COUNT // 2 + 2 + self.score])
        print(len(self.body))

    def draw(self):
        for elem in self.body:
            screen.blit(self.image, (elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Apple: # Apple Class Object

    def __init__(self, size=1):
        self.x = random.randrange(COL_COUNT) * CELL_SIZE
        self.y = random.randrange(ROW_COUNT) * CELL_SIZE
        self.size = size  # Зачем?

    def draw(self):
        pygame.draw.rect(screen, (250, 50, 50), (self.x, self.y, CELL_SIZE, CELL_SIZE))


snake = Snake(startimage)
apple = Apple()
pygame.mixer.music.load("data/sound/start.wav")
pygame.mixer.music.play()
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            snake.set_direction(event.key)
    snake.move()
    clock.tick(10)
    screen.fill((0, 0, 0))
    snake.draw()
    apple.draw()
    for elem in snake.body:
        if pygame.Rect(apple.x, apple.y, CELL_SIZE, CELL_SIZE).colliderect((elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)):
            snake.eat()
            apple = Apple()
            break
    screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render(f'{snake.score}', False, (255, 0, 0)), (W - 35, 0))
    pygame.display.flip()
