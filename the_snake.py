"""Игра Змейка"""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Общий класс объектов игры"""

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self):
        """Шаблон метода отрисовки"""


class Apple(GameObject):
    """Класс объекта яблоко"""

    def __init__(self):
        """Инициализатор объекта яблока"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None

    def randomize_position(self, snake_positions):
        """Метод задания рандомной позиции яблока"""
        if snake_positions:
            while True:
                x_coordinate = randint(0, GRID_WIDTH - 1) * 20
                y_coordinate = randint(0, GRID_HEIGHT - 1) * 20
                if (x_coordinate, y_coordinate) not in snake_positions:
                    self.position = (x_coordinate, y_coordinate)
                    break

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка"""

    def __init__(self):
        """Инициализатор объекта змейки"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [SCREEN_CENTER]
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод, обновляющий направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод задания движения змейке"""
        head = self.get_head_position()
        if self.direction == UP:
            new_head = (
                head[0] % SCREEN_WIDTH,
                (head[1] - GRID_SIZE) % SCREEN_HEIGHT
            )
        elif self.direction == DOWN:
            new_head = (
                head[0] % SCREEN_WIDTH,
                (head[1] + GRID_SIZE) % SCREEN_HEIGHT
            )
        elif self.direction == RIGHT:
            new_head = (
                (head[0] + GRID_SIZE) % SCREEN_WIDTH,
                head[1] % SCREEN_HEIGHT
            )
        elif self.direction == LEFT:
            new_head = (
                (head[0] - GRID_SIZE) % SCREEN_WIDTH,
                head[1] % SCREEN_HEIGHT
            )

        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if self.length != len(self.positions):
                self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения координат головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод обнуления змейки"""
        self.length = 1
        self.positions.clear()
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.move()
            apple.randomize_position(snake.positions)
            snake.length += 1
        else:
            snake.move()
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()

