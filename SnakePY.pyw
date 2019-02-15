import pygame
import random
import sys
from pygame.locals import *


pygame.init()
W, H = 480, 320
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption("SnakePY 1.0dev2")
CELL_SIZE = 8
COL_COUNT = W // CELL_SIZE
ROW_COUNT = H // CELL_SIZE
startimage = "data/images/snake/white.png"

def play_sound(fname):
    pygame.mixer.music.load(fname)
    pygame.mixer.music.play()

class Snake: # Snake Object Class
    def __init__(self, img):
        self.image = pygame.image.load(img)
        self.body = [[COL_COUNT // 2, ROW_COUNT // 2],
                     [COL_COUNT // 2, ROW_COUNT // 2 + 1],
                     [COL_COUNT // 2, ROW_COUNT // 2 + 2]]
        self.direction = [0, -1]
        self.oldkey = K_UP
        self.vel = 10
        self.score = 0

    def set_direction(self, key):
        opposite = {K_LEFT: K_RIGHT, K_RIGHT: K_LEFT, K_UP: K_DOWN, K_DOWN: K_UP}
        if self.oldkey == key: self.vel += 5
        elif opposite[self.oldkey] == key:
            if self.vel > 5: self.vel -= 5
        else:
            if key == K_LEFT: self.direction = [-1, 0]
            elif key == K_RIGHT: self.direction = [1, 0]
            elif key == K_UP: self.direction = [0, -1]
            elif key == K_DOWN: self.direction = [0, 1]
            self.oldkey = key

    def move(self):
        self.body.insert(0, [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]])
        self.body.pop() # убираем хвост
        self.image = pygame.image.load("data/images/snake/" + random.choice(("white.png", "dblue.png", "green.png", "lblue.png", "orange.png", "red.png", "violet.png")))

    def eat(self):
        screen.fill((0, 0, 0))
        self.score += 1
        self.body.append([COL_COUNT // 2, ROW_COUNT // 2 + 2 + self.score])
        play_sound("data/sound/ate.wav")

    def draw(self):
        for elem in self.body:
            screen.blit(self.image, (elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def quit_game(self):
        records_out = open("records.ini", "w")
        records_out.write(str(self.score))
        records_out.close()
        pygame.quit()
        sys.exit(0)

class Apple: # Apple Class Object

    def __init__(self, size=1):
        self.set_coords()
        self.size = size  # Зачем?

    def draw(self):
        pygame.draw.rect(screen, (250, 50, 50), (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def set_coords(self):
        self.x = random.randrange(COL_COUNT) * CELL_SIZE
        self.y = random.randrange(ROW_COUNT) * CELL_SIZE


snake = Snake(startimage)
apple = Apple()
play_sound("data/sound/start.wav")
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            snake.quit_game()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                snake.quit_game()
            else:
                snake.set_direction(event.key)
    snake.move()
    clock.tick(snake.vel)
    screen.fill((0, 0, 0))
    snake.draw()
    apple.draw()
    for elem in snake.body:
        if pygame.Rect(apple.x, apple.y, CELL_SIZE, CELL_SIZE).colliderect((elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)):
            snake.eat()
            apple.set_coords()
            break
    screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render(f'{snake.score}', False, (255, 0, 0)), (W - 35, 0))
    pygame.display.flip()
