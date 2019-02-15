import pygame  # Импортируем Pygame
import random  # Импортируем Random
import sys  # Импортируем Sys (для sys.exit(0))
# Импортируем pygame.locals (чтобы не писать постоянно pygame.*)
from pygame.locals import *

W, H = 640, 480  # Устанавливаем разрешение экрана (640X480)
pygame.init()  # Инициализируем Pygame
# Скрываем курсор мыши во время игры (а зачем он?)
pygame.mouse.set_visible(False)
# Создаём экран с нужным размером и в полноэкранном режиме
screen = pygame.display.set_mode((W, H), FULLSCREEN)
pygame.display.set_caption("SnakePY 1.0dev3")  # Создаём заголовок окна
CELL_SIZE = 8  # Задаём размер одной клеточки для змейки
COL_COUNT = W // CELL_SIZE  # Высчитываем количество столбцов
ROW_COUNT = H // CELL_SIZE  # Высчитываем количество строк
startimage = "data/images/snake/white.png"  # Задаём начальное изображение клеточек змейки


def play_sound(fname):  # Функция для проигрывания звуков
    pygame.mixer.music.load(fname)  # Загружаем звук
    pygame.mixer.music.play()  # и... собственно, проигрываем)


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
        screen.fill((0, 0, 0))  # заполняем экран чёрным цветом
        self.score += 1  # добавляем очко
        self.body.append([COL_COUNT // 2, ROW_COUNT // 2 + 2 + self.score])  # Добавить кусок тела (змейка "растёт")
        play_sound("data/sound/ate.wav")  # проиграть звук съедания яблока

    def draw(self):  # Метод, отвечающий за отрисовку змейки
        for elem in self.body:  # Отрисовывать надо каждую клеточку змейки, поэтому перебираем их циклом for и
            screen.blit(self.image, (elem[0] * CELL_SIZE, elem[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # отрисовываем

    def quit_game(self):  # Завершить игру (пока появляется только при закрытии игры крестиком)
        records_out = open("results.ini", "a")  # Открываем файл для записями и
        records_out.write(" ".join((str(self.score),
                                    str(pygame.time.get_ticks()))) + "\n")  # и добавляем туда новый результат игры
        records_out.close()  # Обязательно закрываем файл
        pygame.quit()  # Завершаем работу pygame
        sys.exit(0)  # Завершаем работу всего кода (во избежание ошибки из-за неинициализированного pygame)


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
        pygame.draw.rect(screen, (250, 50, 50),
                         (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def set_coords(self):  # Метод для задания координат яблока
        self.x = random.randrange(COL_COUNT) * CELL_SIZE  # Задаём x и
        self.y = random.randrange(ROW_COUNT) * CELL_SIZE  # y


snake = Snake(startimage)  # Создаём змейку
apple = Apple()  # и яблоко
play_sound("data/sound/start.wav")  # играем звук гонга
clock = pygame.time.Clock()  # создаём объект часов
while True:  # Главный цикл игры
    for event in pygame.event.get():  # Перебираем все события циклом for
        if event.type == QUIT:  # Если событие на выход, то
            snake.quit_game()  # выйти
        elif event.type == KEYDOWN:  # Если событие на нажатие клавиши
            if event.key == K_ESCAPE or (event.mod in (KMOD_LALT, KMOD_RALT) and event.key == K_F4):  # для выхода, то
                snake.quit_game()  # выйти из игры
            elif event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):  # для движения, то
                # меняем направление или скорость движения в соответствии с нажатием кл.
                snake.set_direction(event.key)
    snake.move()  # двигаемся
    # сколько раз в секунду выполняется цикл зависит от скорости змейки
    clock.tick(snake.vel)
    screen.fill((0, 0, 0))  # заливаем экран чёрным цветом
    snake.draw()  # отрисовываем змейку
    apple.draw()  # и яблоко
    if pygame.Rect(apple.x, apple.y, CELL_SIZE, CELL_SIZE).colliderect((snake.body[0][0] * CELL_SIZE,
                                                                        snake.body[0][1] * CELL_SIZE,
                                                                        CELL_SIZE,
                                                                        CELL_SIZE)):  # если змейка съела яблоко
        snake.eat()  # съесть яблоко
        apple.set_coords()  # изменить координаты яблока на экране
    screen.blit(pygame.font.SysFont('Comic Sans MS', 30) .render(
        f'{snake.score}', False, (255, 0, 0)), (W - 35, 0))  # отображаем очки на экране
    pygame.display.flip()  # обновляем экран
