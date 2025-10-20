from random import randint
import pygame

# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# --- Инициализация pygame и обязательные объекты ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


# --- Классы ---
class GameObject:
    """Базовый игровой объект (позиция и цвет)."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Args:
            position: координаты верхнего левого угла клетки).
            body_color: RGB-цвет объекта (по умолчанию белый).
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Базовый метод отрисовки (заглушка)."""
        pass


class Apple(GameObject):
    """Яблоко — появляется в случайной клетке."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайно выбирает позицию на поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        super().__init__((center_x, center_y), SNAKE_COLOR)

        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        """Применяет следующее направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow=False):
        """Перемещает змейку на 1 клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if not grow:
            self.last = self.positions.pop()
        else:
            self.last = None
            self.length += 1

    def draw(self, surface):
        """Отрисовка змейки."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сброс в начальное состояние."""
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.position = (center_x, center_y)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


# --- Обработка клавиш ---
def handle_keys(game_object):
    """Обрабатывает события pygame и меняет направление змейки."""
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


# --- Основная функция ---
def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        # Проверка, съела ли змейка яблоко
        dx, dy = snake.direction
        head_x, head_y = snake.get_head_position()
        next_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                     (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        ate_apple = next_head == apple.position
        snake.move(grow=ate_apple)

        if ate_apple:
            apple.randomize_position()

        # Проверка самопересечения
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
