import pygame  # Импортируем Pygame
import random  # Импортируем Random
import sys  # Импортируем Sys (для sys.exit(0))
# Импортируем pygame.locals (чтобы не писать постоянно pygame.*)
from pygame.locals import *
import webbrowser

from bounds import Bounds

W, H = 640, 480  # Устанавливаем разрешение экрана (640X480)
pygame.init()  # Инициализируем Pygame
# Скрываем курсор мыши во время игры (а зачем он?)
pygame.mouse.set_visible(False)
# Создаём экран с нужным размером и в полноэкранном режиме
screen = pygame.display.set_mode((W, H), FULLSCREEN)
pygame.display.set_caption("SnakePY 1.00dev4")  # Создаём заголовок окна
CELL_SIZE = 8  # Задаём размер одной клеточки для змейки
COL_COUNT = W // CELL_SIZE  # Высчитываем количество столбцов
ROW_COUNT = H // CELL_SIZE  # Высчитываем количество строк
startimage = "data/images/snake/white.png"  # Задаём начальное изображение клеточек змейки

INTRO = 1
GAME = 2
BEST_RESULTS = 3
HELP = 4
ABOUT = 5
GOVER = 6
game_mode = INTRO

INTRO_BUTTONS = ("play", "best_results", "help", "about", "exit")
ABOUT_BUTTONS = ("ok", "contact_me", "more_projects")
ABOUT_BUTTONS_POS = (100, 175, 345)
GOVER_BUTTONS = ("ok", "retry")
GOVER_BUTTONS_POS = (230, 300)

def play_sound(fname):  # Функция для проигрывания звуков
    pygame.mixer.music.load(fname)  # Загружаем звук
    pygame.mixer.music.play()  # и... собственно, проигрываем)

def quit_app():
    pygame.quit()  # Завершаем работу pygame
    sys.exit(0)  # Завершаем работу всего кода (во избежание ошибки из-за неинициализированного pygame)

class Snake:   # Класс змейки
    def __init__(self, img):
        self.image = pygame.image.load(img)  # Атрибут, с изображением клеточек змейки
        self.body = [[COL_COUNT // 2, ROW_COUNT // 2], [COL_COUNT // 2, ROW_COUNT // 2 + 1],
                     [COL_COUNT // 2, ROW_COUNT // 2 + 2]]  # Тело змейки (список клеточек)
        self.direction = [0, -1]  # Направление змейки
        self.oldkey = K_UP  # Атрибут со значением последний раз нажатой клавиши - змейка сначала идёт вверх
        self.vel = 10  # Скорость перемещений змейки
        self.score = 0  # Очки змейки (количество съеденных яблочек)

    def set_direction(self, key):  # Метод, устанавливающий направление змейки
        opposite = {K_LEFT: K_RIGHT, K_RIGHT: K_LEFT, K_UP: K_DOWN, K_DOWN: K_UP}  # Словарь противоположных клавиш
        if self.oldkey == key:
            self.vel += 5  # Если дважды нажата одна и та же клавиша, увеличиваем скороть
        # Если нажата клавиша, противоположная прошлой, уменьшаем скорость,
        elif opposite[self.oldkey] == key:
            if self.vel > 5:
                self.vel -= 5  # однако не даём ей опуститься до 0
        else:  # В противном случае
            if key == K_LEFT:
                # Если нажата клавиша влево, идём влево
                self.direction = [-1, 0]
            elif key == K_RIGHT:
                # Если нажата клавиша вправо, идём вправо
                self.direction = [1, 0]
            elif key == K_UP:
                # Если нажата клавиша вверх, идём вверх
                self.direction = [0, -1]
            elif key == K_DOWN:
                self.direction = [0, 1]  # Если нажата клавиша вниз, идём вниз
            self.oldkey = key  # Запоминаем клавишу, как последнюю нажатую

    def move(self):  # Метод, отвечающий за движение змейки
        self.body.insert(0, [self.body[0][0] + self.direction[0],
                             self.body[0][1] + self.direction[1]])  # Вставляем в начало тела змейки один кусок и
        self.body.pop()  # убираем хвост с конца
        self.image = pygame.image.load("data/images/snake/" + random.choice(("white.png", "dblue.png", "green.png",
                                                                             "lblue.png", "orange.png", "red.png",
                                                                             "violet.png")))  # меняем цвета

    def eat(self):  # Метод, отвечающий за съедание яблока
        self.score += 1  # добавляем очко
        self.body.append([COL_COUNT // 2, ROW_COUNT // 2 + 2 + self.score])  # Добавить кусок тела (змейка "растёт")
        if self.score % 10:
            play_sound("data/sound/ate.wav")  # проиграть звук съедания яблока
        else:
            play_sound("data/sound/ten.mp3")
        
    def draw(self):  # Метод, отвечающий за отрисовку змейки
        for elem in self.body:  # Отрисовывать надо каждую клеточку змейки, поэтому перебираем их циклом for и
            screen.blit(self.image, (elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # отрисовываем

    def end_game(self):  # Завершить игру (пока появляется только при закрытии игры крестиком)
        records_out = open("results.ini", "a")  # Открываем файл для дозаписи и
        records_out.write(" ".join((str(self.score),
                                    str(pygame.time.get_ticks()))) + "\n")  # и добавляем туда новый результат игры
        records_out.close()  # Обязательно закрываем файл


class Apple:  # Класс яблока
    def __init__(self):
        # Создаём атрибут x-координаты (все атрибуты, по правилам Python,
        # должны быть указаны в __init__)
        self.x = 0
        # Создаём атрибут y-координаты (все атрибуты, по правилам Python,
        # должны быть указаны в __init__)
        self.y = 0
        self.set_coords()  # Задаём начальные координаты яблока

    def draw(self):  # Метод, для отрисовки яблока на экран
        # Отрисовываем Rect-яблоко
        screen.blit(pygame.image.load("data/images/snake/apple.png"), (self.x, self.y))

    def set_coords(self):  # Метод для задания координат яблока
        self.x = random.randrange(1, COL_COUNT - 1) * CELL_SIZE  # Задаём x и
        self.y = random.randrange(1, ROW_COUNT - 1) * CELL_SIZE  # y



background = pygame.image.load("data/images/bg.png")
intro_selected_button, about_selected_button, gover_selected_button = 0, 0, 0
while True:  # Главный цикл игры
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # Перебираем все события циклом for
        if event.type == QUIT:  # Если событие на выход, то
            quit_app()  # выйти
        elif event.type == KEYDOWN:  # Если событие на нажатие клавиши
            if event.mod in (KMOD_LALT, KMOD_RALT) and event.key == K_F4:
                quit_app()
            if event.key == K_ESCAPE:  # для выхода, то
                if game_mode != INTRO:
                    game_mode = INTRO  # выйти из игры
                else:
                    quit_app()
            elif event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN, K_RETURN):  # для движения, то
                if game_mode == GAME:
                    # меняем направление или скорость движения в соответствии с нажатием кл.
                    if event.key != K_RETURN:
                        snake.set_direction(event.key)
                elif game_mode == INTRO:
                    if event.key == K_DOWN:
                        if intro_selected_button < 4:
                            intro_selected_button += 1
                        else:
                            intro_selected_button = 0
                    elif event.key == K_UP:
                        if intro_selected_button > 0:
                            intro_selected_button -= 1
                        else:
                            intro_selected_button = 4
                    elif event.key == K_RETURN:
                        if intro_selected_button == 0:
                            game_mode = GAME # игра начинается
                            snake = Snake(startimage)  # Создаём змейку
                            apple = Apple()  # и яблоко
                            clock = pygame.time.Clock()  # создаём объект часов
                            play_sound("data/sound/start.wav")  # играем звук гонга
                            
                        elif intro_selected_button == 1:
                            game_mode = BEST_RESULTS
                        elif intro_selected_button == 2:
                            game_mode = HELP
                        elif intro_selected_button == 3:
                            game_mode = ABOUT
                        elif intro_selected_button == 4:
                            quit_app()
                elif game_mode == ABOUT:
                    if event.key == K_RIGHT:
                        if about_selected_button < 2:
                            about_selected_button += 1
                        else:
                            about_selected_button = 0
                    elif event.key == K_LEFT:
                        if about_selected_button > 0:
                            about_selected_button -= 1
                        else:
                            about_selected_button = 2
                    elif event.key == K_RETURN:
                        if about_selected_button == 0:
                            game_mode = INTRO
                        elif about_selected_button == 1:
                            webbrowser.open("mailto:demianwolfssd@gmail.com")
                        elif about_selected_button == 2:
                            webbrowser.open("https://github.com/DemianWolf1/")
                elif game_mode == GOVER:
                    if event.key == K_RIGHT:
                        if gover_selected_button < 1:
                            gover_selected_button += 1
                        else:
                            gover_selected_button = 0
                    elif event.key == K_LEFT:
                        if gover_selected_button > 0:
                            gover_selected_button -= 1
                        else:
                            gover_selected_button = 1
                    elif event.key == K_RETURN:
                        if gover_selected_button == 0:
                            game_mode = INTRO
                        elif gover_selected_button == 1:
                            game_mode = GAME
                            snake = Snake(startimage)  # Создаём змейку
                            apple = Apple()  # и яблоко
                            clock = pygame.time.Clock()  # создаём объект часов
                            play_sound("data/sound/start.wav")  # играем звук гонга
                elif game_mode == HELP and event.key == K_RETURN:
                    game_mode = INTRO

    if game_mode == INTRO:
        screen.blit(pygame.image.load("data/images/intro/caption.png"), (8, 0))
        for button_id in range(5):
            if button_id != intro_selected_button:
                screen.blit(pygame.image.load("".join(("data/images/intro/buttons/", INTRO_BUTTONS[button_id], ".png"))), (150, 90 + button_id * 75))
            else:
                screen.blit(pygame.image.load("".join(("data/images/intro/buttons/", INTRO_BUTTONS[button_id], "_selected.png"))), (136, 90 + button_id * 75))   
    elif game_mode == GAME:
        snake.move()  # двигаемся
        # сколько раз в секунду выполняется цикл зависит от скорости змейки
        clock.tick(snake.vel)
        snake.draw()  # отрисовываем змейку
        apple.draw()  # и яблоко
        for bound in Bounds().createlist(width=W, height=H, size=CELL_SIZE):
            pygame.draw.rect(screen, (100, 100, 255), bound)
        if snake.body[0] in snake.body[1:]:
            game_mode = GOVER
            play_sound("data/sound/gameover.mp3")
        for bound in Bounds().createlist(width=W, height=H, size=CELL_SIZE):
            if bound.colliderect((snake.body[0][0] * CELL_SIZE,
                                  snake.body[0][1] * CELL_SIZE,
                                  CELL_SIZE,
                                  CELL_SIZE)):
                game_mode = GOVER
                play_sound("data/sound/gameover.mp3")
        if pygame.Rect(apple.x, apple.y, CELL_SIZE, CELL_SIZE).colliderect((snake.body[0][0] * CELL_SIZE,
                                                                            snake.body[0][1] * CELL_SIZE,
                                                                            CELL_SIZE,
                                                                            CELL_SIZE)):  # если змейка съела яблоко
            snake.eat()  # съесть яблоко
            apple.set_coords()  # изменить координаты яблока на экране
        screen.blit(pygame.font.SysFont('Arial', 30).render(
            str(snake.score), False, (255, 0, 0)), (W - 35, 0))  # отображаем очки на экране
    elif game_mode == BEST_RESULTS:
        pass
    elif game_mode == HELP:
        screen.blit(pygame.image.load("data/images/help/dialogue.png"), (61.5, 100))
        screen.blit(pygame.image.load("data/images/about/buttons/ok_selected.png"), (280, 310))
    elif game_mode == ABOUT:
        screen.blit(pygame.image.load("data/images/about/dialogue.png"), (24, 100))
        for button_id in range(3):
            if button_id != about_selected_button:
                screen.blit(pygame.image.load("".join(("data/images/about/buttons/", ABOUT_BUTTONS[button_id], ".png"))), (ABOUT_BUTTONS_POS[button_id], 350))
            else:
                screen.blit(pygame.image.load("".join(("data/images/about/buttons/", ABOUT_BUTTONS[button_id], "_selected.png"))), (ABOUT_BUTTONS_POS[button_id], 350))

    elif game_mode == GOVER:
        screen.blit(pygame.image.load("data/images/gover/dialogue.png"), (61.5, 180))
        for button_id in range(2):
            if button_id != gover_selected_button:
                screen.blit(pygame.image.load("".join(("data/images/gover/buttons/", GOVER_BUTTONS[button_id], ".png"))), (GOVER_BUTTONS_POS[button_id], 310))
            else:
                screen.blit(pygame.image.load("".join(("data/images/gover/buttons/", GOVER_BUTTONS[button_id], "_selected.png"))), (GOVER_BUTTONS_POS[button_id], 310))
    pygame.display.flip()  # обновляем экран
