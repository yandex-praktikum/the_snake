import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 20

# Направления
UP = (0, -CELL_SIZE)
DOWN = (0, CELL_SIZE)
LEFT = (-CELL_SIZE, 0)
RIGHT = (CELL_SIZE, 0)

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None):
        """Инициализация объекта с заданной позицией."""
        self.position = position if position else (0, 0)

    def draw(self, surface):
        """Метод для рисования объекта на поверхности."""
        er = "Метод draw() должен быть переопределён в дочерних классах."
        raise NotImplementedError(er)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = RED

    def randomize_position(self):
        """Случайная позиция для яблока."""
        return (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )

    def draw(self, surface):
        """Рисует яблоко на поверхности."""
        pygame.draw.rect(surface, self.body_color,
                         (*self.position, CELL_SIZE, CELL_SIZE))


class BadFood(GameObject):
    """Класс для вредной еды."""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = BLUE

    def randomize_position(self):
        """Случайная позиция для вредной еды."""
        return (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )

    def draw(self, surface):
        """Рисует вредную еду на поверхности."""
        pygame.draw.rect(surface, self.body_color,
                         (*self.position, CELL_SIZE, CELL_SIZE))


class Obstacle(GameObject):
    """Класс для препятствий."""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = GRAY

    def randomize_position(self):
        """Случайная позиция для препятствия."""
        return (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )

    def draw(self, surface):
        """Рисует препятствие на поверхности."""
        pygame.draw.rect(surface, self.body_color,
                         (*self.position, CELL_SIZE, CELL_SIZE))


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки."""
        initial_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(initial_position)
        self.length = 1
        self.positions = [initial_position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = GREEN

    def update_direction(self, new_direction):
        """Обновление направления движения."""
        opposite_direction = (-self.direction[0], -self.direction[1])

        if new_direction != opposite_direction:
            self.next_direction = new_direction

    def move(self):
        """Обновление позиций сегментов змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (
            (self.positions[0][0] + self.direction[0]) % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1]) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Рисует змейку на поверхности."""
        for segment in self.positions:
            pygame.draw.rect(surface, self.body_color,
                             (*segment, CELL_SIZE, CELL_SIZE))

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.__init__()


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        snake.update_direction(UP)

    elif keys[pygame.K_DOWN]:
        snake.update_direction(DOWN)

    elif keys[pygame.K_LEFT]:
        snake.update_direction(LEFT)

    elif keys[pygame.K_RIGHT]:
        snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    bad_food = None
    obstacles = []

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обработка клавиш
        handle_keys(snake)

        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

            # Появление вредной еды после увеличения змейки
            if snake.length == 5 and bad_food is None:
                bad_food = BadFood()

            # Появление препятствий после увеличения змейки
            if snake.length >= 10:
                obstacles.append(Obstacle())

        # Проверка столкновения с вредной едой
        if bad_food and snake.get_head_position() == bad_food.position:
            if snake.length > 1:
                snake.length -= 1
                snake.positions = snake.positions[:snake.length]

            bad_food.position = bad_food.randomize_position()

        # Проверка столкновения с камнем
        for i in range(len(obstacles)):
            if snake.get_head_position() == obstacles[i].position:
                snake.length = 1
                snake.positions = [snake.get_head_position()]
                del obstacles[i]
                bad_food = None
                break

        # Проверка столкновения змейки с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.length = 1
            snake.positions = [snake.get_head_position()]
            bad_food = None

        screen.fill(BLACK)
        apple.draw(screen)

        if bad_food:
            bad_food.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        snake.draw(screen)

        pygame.display.update()

        clock.tick(FPS)

    # Завершение работы Pygame после выхода из цикла.
    pygame.quit()


if __name__ == "__main__":
    main()
