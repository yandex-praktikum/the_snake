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
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Это докстриг"""

    def __init__(self, body_color: tuple = (255, 0, 0),
                 position: tuple = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
                 ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Это докстриг"""
        pass


class Apple(GameObject):
    """Это докстриг"""

    def __init__(self, body_color=(255, 0, 0),
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        super().__init__(body_color=(255, 0, 0),
                         position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
        self.body_color = (255, 0, 0)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Это докстриг"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        position = (x, y)

        self.position = position

        return position

    # Метод draw класса Apple
    def draw(self):
        """Это докстриг"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Это докстриг"""

    def __init__(self, position=(0, 0), length: int = 1,
                 positions: list[tuple] = [(0, 0)],
                 direction: tuple = RIGHT, next_direction: tuple = None,
                 body_color=(0, 255, 0)):
        super().__init__(body_color, position)
        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = self.positions[-1]

    def update_direction(self):
        """Это докстриг"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Это докстриг"""
        head = self.get_head_position()

        dx, dy = self.direction

        new_head = (
            (head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self):
        """Это докстриг"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
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
        """Это докстриг"""
        return self.positions[0]

    def reset(self):
        """Это докстриг"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Это докстриг"""
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
    """Это докстриг"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        snake.draw()
        apple.draw()

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
            print(apple.position)

        pygame.display.update()


if __name__ == '__main__':
    main()
