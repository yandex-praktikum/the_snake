"""
Модуль игры "Змейка" на PyGame.

Содержит классы для игровых объектов и основную логику игры.
"""

from random import choice, randint
from itertools import product

import pygame

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
BOARD_BACKGROUND_COLOR = (40, 40, 40)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
SNAKE_BORDER_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Множество всех полей доски
board_field = set(product(list(range(GRID_WIDTH)), list(range(GRID_HEIGHT))))
# Счётчик съеденных яблок
counter = 0

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

screen.fill(BOARD_BACKGROUND_COLOR)

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, pos, color):
        """Инициализирует игровой объект с позицией и цветом."""
        self.pos = pos
        self.color = color

    def draw(self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.pos, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(self):
        """Инициализирует змейку в центре экрана."""
        x_pos = SCREEN_WIDTH / 2
        y_pos = SCREEN_HEIGHT / 2
        super().__init__((x_pos, y_pos), SNAKE_COLOR)
        self.positions = [self.pos]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1]

        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)
        self.positions.pop()
        self.pos = new_head

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, SNAKE_BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, head_rect)
        pygame.draw.rect(screen, SNAKE_BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Класс яблока - цели для змейки."""

    def __init__(self):
        """Инициализирует яблоко в случайной позиции."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        super().__init__((x, y), APPLE_COLOR)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.pos, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize(self, snake):
        """Перемещает яблоко в случайную свободную позицию."""
        snake_positions_set = set(
            (x // GRID_SIZE, y // GRID_SIZE) for x, y in snake.positions
        )
        available_positions = list(board_field - snake_positions_set)

        if available_positions:
            pos = choice(available_positions)
            self.pos = (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE)


def handle_keys(game_object, game_over):
    """Обрабатывает нажатия клавиш пользователем."""
    global counter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_s and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_a and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_d and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_r and game_over:
                return True
    return False


def show_message(message):
    """Отображает сообщение на экране."""
    font_1 = pygame.font.Font(None, 36)
    text_1 = font_1.render(message, True, (255, 255, 255))
    font_2 = pygame.font.SysFont("arial", 18, italic=True)
    text_2 = font_2.render(f"СЧЁТ: {counter}", True, (255, 255, 255))
    text_rect_1 = text_1.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 15)
    )
    text_rect_2 = text_2.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 15)
    )

    # Создаем полупрозрачный фон для текста
    s = pygame.Surface((SCREEN_WIDTH, 100))
    s.fill((0, 0, 0))
    s.set_alpha(40)
    screen.blit(s, (0, SCREEN_HEIGHT // 2 - 50))

    screen.blit(text_1, text_rect_1)
    screen.blit(text_2, text_rect_2)
    pygame.display.update()


def main():
<<<<<<< HEAD
    """Основная функция игры, содержащая главный игровой цикл."""
    global counter
=======
    # Инициализация PyGame:
>>>>>>> fb2f06cd0e032d0064921cd364789a6d8c1d0558
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    game_over = False

    snake.draw()
    running = True

    pygame.display.update()

    while running:
        # Обработка ввода пользователя
        if handle_keys(snake, game_over):
            game_over = False
            counter = 0
            snake = Snake()
            apple = Apple()

        if not game_over:
            snake.update_direction()
            snake.move()

            # Проверка столкновения с хвостом
            if len(snake.positions) >= 2:
                for i in range(2, len(snake.positions)):
                    if snake.positions[0] == snake.positions[i]:
                        game_over = True

            # Проверка столкновения с яблоком
            if snake.positions[0] == apple.pos:
                counter += 1
                apple = Apple()
                apple.randomize(snake)
                snake.positions.append(snake.last)

            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw()
            snake.draw()
            pygame.display.update()
            clock.tick(SPEED)
        else:
            show_message("GAME OVER")


if __name__ == '__main__':
    main()
