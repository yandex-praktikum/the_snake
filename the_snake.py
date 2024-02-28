from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
HEAD_SNAKE_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс, содержащий обязательные методы и атрибуты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color
        self.position = (
            randint(0, SCREEN_WIDTH) // GRID_SIZE * GRID_SIZE,
            randint(0, SCREEN_HEIGHT) // GRID_SIZE * GRID_SIZE
        )

    def draw(self, screen):
        """Обязательный метод наследников класса."""
        pass

    def eat(self, position):
        """Обязательный метод наследников класса."""
        raise NotImplementedError


class Apple(GameObject):
    """
    Класс, описывающий яблоко в игре.
    Атрибуты:
    - body_color: tuple. Цвет яблока.
    - position: tuple. Текущая позиция яблока на экране.
    Методы:
    - __init__: Инициализация объекта яблока.
    Задает начальное положение и цвет.
    - draw: Отрисовка яблока на игровом экране.
    - eat: Обработка события поедания яблока змейкой и перемещение яблока.
    """

    position = (0, 0)
    body_color = APPLE_COLOR

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)

    def draw(self, screen):
        """Метод отрисовывает яблоко в игровом окне."""
        rect = pygame.Rect(
            (self.position),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, position):
        """
        Метод меняет координаты яблока
        при совпадении координат змейки и яблока.
        """
        if self.position == position:
            self.position = (
                randint(0, SCREEN_WIDTH) // GRID_SIZE * GRID_SIZE,
                randint(0, SCREEN_HEIGHT) // GRID_SIZE * GRID_SIZE
            )


class Snake(GameObject):
    """
    Класс, описывающий поведение змеи в игре.

    Атрибуты:
    - position: tuple. Начальная позиция головы змеи на экране.
    - positions: list. Список координат сегментов змеи.
    - last: tuple. Координаты последнего сегмента змеи перед движением.
    - body_color: tuple. Цвет тела змеи.
    - direction: tuple. Направление движения змеи (UP, DOWN, LEFT, RIGHT).
    - next_direction: str. Следующее направление движения змеи.

    Методы:
    - draw: Отрисовка змеи на игровом экране.
    - randomize_position: Обработка события поеданияяблока и увеличение
    длины змеи.
    - reset: Сброс состояния змеи до начального состояния.
    """

    position: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),

    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    def __init__(self, body_color=SNAKE_COLOR, direction=(0, 0)):
        self.last = None
        self.body_color = SNAKE_COLOR
        self.direction = direction
        self.next_direction = None
        self.length = 1
        super().__init__(body_color)

    # # Метод draw класса Snake
    def draw(self, screen):
        """
        Метод отрисовывает каждый сегмент змейки,
        голова змеи будет окрашена другим цветом,
        последний сегмент змеи окрашивается цветом фона доски.
        """
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, HEAD_SNAKE_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def eat(self, position):
        """
        Метод увеличивает длину змейки на один сегмент
        при совпадении координат змейки и яблока.
        """
        if position == self.positions[0]:
            self.positions.append(snake.last)
            self.length = len(self.positions)

    def reset(self):
        """
        Метод создает новую змею длиной в 1 сегмент,
        сегменты старой змеи закрашивает цветом фона.
        """
        for position in self.positions:
            rect = pygame.Rect(
                (position),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        self.direction = UP
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = len(self.positions)

# Функция обработки действий пользователя
    def get_head_position(self):
        """Метод возвращающий координаты первого звена змейки."""
        return self.positions[0]

# Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод изменяющий направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод создает новое звено змейки в направлении ее движения и
        удаляет посленее звено.
        """
        new_pos = (snake.positions[0][0] + GRID_SIZE * snake.direction[0],
                   snake.positions[0][1] + GRID_SIZE * snake.direction[1])
        if new_pos[0] < 0:
            new_pos = (SCREEN_WIDTH - GRID_SIZE, new_pos[1])
        if new_pos[0] > SCREEN_WIDTH - GRID_SIZE:
            new_pos = (0, new_pos[1])
        if new_pos[1] < 0:
            new_pos = (new_pos[0], SCREEN_HEIGHT - GRID_SIZE)
        if new_pos[1] > SCREEN_HEIGHT - GRID_SIZE:
            new_pos = (new_pos[0], 0)
        snake.positions.insert(0, new_pos)
        snake.last = snake.positions.pop()


def handle_keys():
    """
    Метод изменяет направление движения змеи при нажатии на стрелки и
    возвращает возвращает позицию головы змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


direction = UP
apple = Apple(APPLE_COLOR)
snake = Snake(SNAKE_COLOR, direction)


def main():
    """
    Основная функция игры. Эта функция обрабатывает основную логику игры,
    включая обновление экрана, проверку нажатий клавиш, движение змейки и
    яблока, проверку столкновений и т.д.
    """
    while True:
        # Тут описывается основная логика игры.
        clock.tick(SPEED)
        apple.draw(screen)
        snake.update_direction()
        snake.eat(apple.position)
        if snake.get_head_position() in snake.positions[3:]:
            snake.reset()
        handle_keys()
        apple.randomize_position(snake.positions[0])
        snake.move()
        snake.draw(screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()