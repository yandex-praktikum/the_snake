import pygame
import random
from typing import Tuple, Set
import os

# Константы игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (255, 255, 255)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Клавиши управления
KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

# Все возможные позиции на поле
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

# Инициализация pygame для глобальных переменных
pygame.init()

# Глобальные переменные для тестов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def init(self, position: Tuple[int, int] = None):
        """
        Инициализирует игровой объект.

        Args:
            position: Начальная позиция объекта.
                     Если None, используется центр экрана.
        """
        if position is None:
            position = CENTER_POSITION
        self.position = position
        self.body_color = None

    def draw_cell(self, surface: pygame.Surface,
                  position: Tuple[int, int],
                  color: Tuple[int, int, int]):
        """
        Отрисовывает одну ячейку на поверхности.

        Args:
            surface: Поверхность для отрисовки
            position: Позиция ячейки
            color: Цвет ячейки
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self, surface: pygame.Surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def init(self):
        """Инициализирует яблоко со случайной позицией."""
        super().init()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self,
                           occupied_positions: Set[Tuple[int, int]] = None):
        """
        Устанавливает случайную позицию для яблока.

        Args:
            occupied_positions: Множество занятых позиций
        """
        if occupied_positions is None:
            occupied_positions = set()

        # Выбираем из свободных ячеек
        free_cells = ALL_CELLS - occupied_positions
        if free_cells:
            self.position = random.choice(tuple(free_cells))
        else:
            # Если все ячейки заняты, используем центр
            self.position = CENTER_POSITION

    def draw(self, surface: pygame.Surface):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def init(self):
        """Инициализирует змейку в начальном состоянии."""
        super().init()
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last_position = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем движение в противоположном направлении
            opposite_directions = {
                UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT
            }
            if self.next_direction != opposite_directions[self.direction]:
                self.direction = self.next_direction
            self.next_direction = None
def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def get_occupied_positions(self) -> Set[Tuple[int, int]]:
        """Возвращает множество занятых змейкой позиций."""
        return set(self.positions)

    def move(self):
        """Перемещает змейку на одну ячейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Вычисляем новую позицию головы
        new_x = (head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверяем столкновение с собой (только для змейки длиной > 3)
        if len(self.positions) > 3 and new_head in self.positions[3:]:
            # При самоукусе отбрасываем хвост, оставляя только голову
            self.positions = [new_head]
            self.length = 1
            return

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Сохраняем позицию последнего сегмента для стирания
        if len(self.positions) > self.length:
            self.last_position = self.positions.pop()
        else:
            self.last_position = None

    def draw(self, surface: pygame.Surface):
        """Отрисовывает змейку на игровой поверхности."""
        # Отрисовываем только голову
        self.draw_cell(surface, self.positions[0], self.body_color)

        # Стираем последний сегмент если нужно
        if self.last_position:
            rect = pygame.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


def handle_keys(snake: Snake) -> bool:
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    Returns:
        True если игра должна продолжиться, False если нужно выйти
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key in KEY_DIRECTIONS:
                snake.next_direction = KEY_DIRECTIONS[event.key]
    return True


def load_high_score() -> int:
    """Загружает рекордный счёт из файла."""
    try:
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
    except (IOError, ValueError):
        pass
    return 0


def save_high_score(score: int):
    """Сохраняет рекордный счёт в файл."""
    try:
        with open('high_score.txt', 'w') as f:
            f.write(str(score))
    except IOError:
        pass


def main():
    """Основная функция игры."""
    # Загрузка рекорда
    high_score = load_high_score()

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Игровой цикл
    game_speed = 10
    running = True

    while running:
        # Обработка событий
        running = handle_keys(snake)
        if not running:
            break

        # Обновление состояния игры
        snake.update_direction()
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Обновляем рекорд
            if snake.length > high_score:
                high_score = snake.length
                save_high_score(high_score)

            # Перемещаем яблоко на свободную позицию
            apple.randomize_position(snake.get_occupied_positions())

        # Обновление заголовка окна
        caption = f'Изгиб Питона - Длина: {snake.length} Рекорд: {high_score}'
        pygame.display.set_caption(caption)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        # Ограничение FPS
        clock.tick(game_speed)

    pygame.quit()


if name == "main":
    main()
