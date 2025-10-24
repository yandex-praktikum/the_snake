import pygame
import random
import sys


# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """
        Инициализирует игровой объект.

        Args:
            position: Начальная позиция объекта
            body_color: Цвет объекта
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока в игре."""

    def __init__(self, position=(0, 0)):
        """Инициализирует яблоко."""
        super().__init__(position, (255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс для змейки в игре."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        """Инициализирует змейку."""
        super().__init__(position, (0, 255, 0))
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            current_x, current_y = self.direction
            next_x, next_y = self.next_direction

            # Не позволяем двигаться в противоположном направлении
            if (current_x + next_x != 0) or (current_y + next_y != 0):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_x = head_x + dir_x * GRID_SIZE
        new_y = head_y + dir_y * GRID_SIZE
        new_head = (new_x, new_y)
        new_head = self._handle_wall_collision(new_head)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def _handle_wall_collision(self, position):
        """Обрабатывает столкновение со стенами."""
        x, y = position
        if x >= SCREEN_WIDTH:
            x = 0
        elif x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        if y >= SCREEN_HEIGHT:
            y = 0
        elif y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        return (x, y)

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0], position[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.last[0], self.last[1], GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


# Инициализация Pygame и создание глобальных переменных
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убеждаемся, что яблоко не появляется на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения с собой
        head_position = snake.get_head_position()
        if head_position in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
