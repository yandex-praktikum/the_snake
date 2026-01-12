"""Мини-игра 'Змейка' на pygame.

Файл: the_snake.py
Требования: pygame
Запуск: python the_snake.py
"""

import random
import sys
from typing import List, Optional, Tuple

import pygame

# Параметры игрового поля
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Цвета RGB
COLOR_BG = (0, 0, 0)
COLOR_SNAKE = (0, 255, 0)
COLOR_APPLE = (255, 0, 0)

FPS = 20

# Направления (dx, dy)
UP: Tuple[int, int] = (0, -CELL_SIZE)
DOWN: Tuple[int, int] = (0, CELL_SIZE)
LEFT: Tuple[int, int] = (-CELL_SIZE, 0)
RIGHT: Tuple[int, int] = (CELL_SIZE, 0)

# Алиасы для тестов
GRID_SIZE = CELL_SIZE
BOARD_BACKGROUND_COLOR = COLOR_BG

# Инициализация pygame (объекты на уровне модуля)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position: Optional[Tuple[int, int]] = None) -> None:
        """Инициализирует объект с позицией."""
        if position is None:
            position = (0, 0)
        self.position = position
        self.body_color = None

    def draw(self, surface: pygame.Surface) -> None:
        """Метод отрисовки (переопределяется в наследниках)."""
        raise NotImplementedError


class Apple(GameObject):
    """Яблоко, появляется в случайной свободной ячейке."""

    def __init__(
        self, forbidden_positions: Optional[List[Tuple[int, int]]] = None
    ) -> None:
        """Инициализирует яблоко и задаёт начальную позицию."""
        center_x = (GRID_WIDTH // 2) * CELL_SIZE
        center_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((center_x, center_y))
        self.body_color = COLOR_APPLE
        self.randomize_position(forbidden_positions or [])

    def randomize_position(
        self, forbidden_positions: List[Tuple[int, int]]
    ) -> None:
        """Устанавливает случайную позицию, избегая forbidden_positions."""
        attempts = 0
        while True:
            x = random.randrange(0, GRID_WIDTH) * CELL_SIZE
            y = random.randrange(0, GRID_HEIGHT) * CELL_SIZE
            if (x, y) not in forbidden_positions:
                self.position = (x, y)
                return
            attempts += 1
            if attempts > 1000:
                for gx in range(GRID_WIDTH):
                    for gy in range(GRID_HEIGHT):
                        maybe = (gx * CELL_SIZE, gy * CELL_SIZE)
                        if maybe not in forbidden_positions:
                            self.position = maybe
                            return

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать яблоко."""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки, хранит сегменты и реализует движение."""

    def __init__(self) -> None:
        """Инициализирует змейку в центре поля."""
        center_x = (GRID_WIDTH // 2) * CELL_SIZE
        center_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((center_x, center_y))
        self.body_color = COLOR_SNAKE
        self.positions: List[Tuple[int, int]] = [(center_x, center_y)]
        self.length: int = 1
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает координаты головы."""
        return self.positions[0]

    @staticmethod
    def _opposite(dir1: Tuple[int, int], dir2: Tuple[int, int]) -> bool:
        """Проверяет, противоположны ли направления."""
        return dir1[0] == -dir2[0] and dir1[1] == -dir2[1]

    def update_direction(self) -> None:
        """Применяет следующую команду направления (если задана)."""
        if self.next_direction is None:
            return
        if not self._opposite(self.next_direction, self.direction):
            self.direction = self.next_direction
        self.next_direction = None

    def move(self) -> Optional[Tuple[int, int]]:
        """Сдвигает змейку на одну ячейку; возвращает удалённый хвост."""
        head = self.get_head_position()
        new_x = head[0] + self.direction[0]
        new_y = head[1] + self.direction[1]

        if new_x < 0:
            new_x = (GRID_WIDTH - 1) * CELL_SIZE
        elif new_x >= SCREEN_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = (GRID_HEIGHT - 1) * CELL_SIZE
        elif new_y >= SCREEN_HEIGHT:
            new_y = 0

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        removed_tail: Optional[Tuple[int, int]] = None
        if len(self.positions) > self.length:
            removed_tail = self.positions.pop()
        return removed_tail

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает сегменты змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        center_x = (GRID_WIDTH // 2) * CELL_SIZE
        center_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_key_event(event: pygame.event.Event, snake: Snake) -> None:
    """Обработка нажатий клавиш: стрелки или WASD."""
    if event.type != pygame.KEYDOWN:
        return
    key = event.key
    if key == pygame.K_UP or key == pygame.K_w:
        snake.next_direction = UP
    elif key == pygame.K_DOWN or key == pygame.K_s:
        snake.next_direction = DOWN
    elif key == pygame.K_LEFT or key == pygame.K_a:
        snake.next_direction = LEFT
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        snake.next_direction = RIGHT


# Алиас для совместимости
handle_keys = handle_key_event


def main() -> None:
    """Главный игровой цикл."""
    pygame.display.set_caption('Изгиб Питона — Змейка')

    snake = Snake()
    apple = Apple(forbidden_positions=snake.positions)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            handle_key_event(event, snake)

        if not running:
            break

        snake.update_direction()
        removed_tail = snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            if removed_tail is not None:
                snake.positions.append(removed_tail)
                removed_tail = None
            apple.randomize_position(snake.positions)

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(COLOR_BG)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
