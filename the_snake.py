from random import randint
import pygame


# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость игры
SPEED = 20

# Настройка окна и таймера
pygame.display.set_caption("Змейка")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=(255, 255, 255),
    ):
        """
        Инициализация базовых атрибутов.

        :param position: начальная позиция объекта
        :param body_color: цвет объекта (RGB)
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле."""

    def __init__(self):
        """Создаёт яблоко и задаёт случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """
        Размещает яблоко в случайной клетке игрового поля,
        исключая клетки, занятые змеёй.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """рисует яблоко на игровом поле."""
        rect = pygame.Rect(self.position,
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen,
                         self.body_color, rect)
        pygame.draw.rect(screen,
                         BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Создаёт змейку в центре экрана."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки (если нажата клавиша)."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвигает змейку на одну клетку в текущем направлении."""
        cur_x, cur_y = self.get_head_position()
        dx, dy = self.direction
        new_position = (
            (cur_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (cur_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if (len(self.positions) > 2 and new_position in self.positions[2:]):
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Отрисовывает тело и голову змейки. Затирает след."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """обработка нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif (event.key == pygame.K_UP and snake.direction != DOWN):
                snake.next_direction = UP
            elif (event.key == pygame.K_DOWN and snake.direction != UP):
                snake.next_direction = DOWN
            elif (event.key == pygame.K_LEFT and snake.direction != RIGHT):
                snake.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT and snake.direction != LEFT):
                snake.next_direction = RIGHT


def main():
    """Основная функция запуска игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
