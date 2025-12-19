from random import randint

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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (148, 25, 248)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализация игрового объекта."""
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.body_color = body_color if body_color else (255, 255, 255)

    def draw(self):
        """Отрисовка объекта (абстрактный метод)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.positions = [((GRID_WIDTH // 2) * GRID_SIZE,
                           (GRID_HEIGHT // 2) * GRID_SIZE)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки на один шаг."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверка столкновения с собой
        if new_head in self.positions[1:]:
            self.reset()
            return False

        self.positions.insert(0, new_head)
        has_tail = len(self.positions) > self.length
        self.last = self.positions[-1] if has_tail else None

        # Удаление хвоста, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def grow(self):
        """Увеличение длины змейки."""
        self.length += 1

    def draw(self):
        """Отрисовка змейки."""
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки (немного темнее)
        if self.positions:
            head_color = tuple(max(0, c - 50) for c in self.body_color)
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, head_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
            # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка нажатий клавиш."""
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


def draw_score(score):
    """Отрисовка счета игры."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()
    score = 0

    # Проверка, чтобы яблоко не появилось на змейке
    while apple.position in snake.positions:
        apple.randomize_position()

    while True:
        clock.tick(SPEED)

        # Обработка ввода
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Перемещение змейки
        if not snake.move():
            # Если змейка столкнулась с собой, сброс счета
            score = 0

        # Проверка съедения яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            score += 1
            apple.randomize_position()
            # Проверка, чтобы яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка сетки (опционально, для визуализации)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20),
                             (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20),
                             (0, y), (SCREEN_WIDTH, y))

        apple.draw()
        snake.draw()
        draw_score(score)

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
