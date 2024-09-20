from random import choice, randrange

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Цвет отравы
POISON_COLOR = (102, 51, 0)

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
    """Базовый класс."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране (переопределение в дочер. классах)."""
        pass


class Apple(GameObject):
    """Класс яблока (еда для змеи)."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Определяет случайное местоположение яблока на экране."""
        return (randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE))

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Poison(GameObject):
    """Класс отравы (неправильной еды)."""

    def __init__(self):
        super().__init__()
        self.body_color = POISON_COLOR
        self.position = Apple.randomize_position(self)

    def draw(self):
        """Отрисовывает неправильную еду на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def update_direction(self):
        """Меняет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        self.last = self.positions[-1]
        coordX, coordY = self.positions[0]
        new_coord = (coordX + self.direction[0] * GRID_SIZE,
                     coordY + self.direction[1] * GRID_SIZE)
        self.positions = [new_coord] + self.positions[:-1]

        """Проверки на выход за пределы игрового поля."""
        if self.get_head_position()[0] < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                 self.get_head_position()[1])
        elif self.get_head_position()[0] > SCREEN_WIDTH - GRID_SIZE:
            self.positions[0] = (0, self.get_head_position()[1])
        elif self.get_head_position()[1] < 0:
            self.positions[0] = (self.get_head_position()[0], SCREEN_HEIGHT)
        elif self.get_head_position()[1] > SCREEN_HEIGHT - GRID_SIZE:
            self.positions[0] = (self.get_head_position()[0], 0)

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def grow(self):
        """Увеличивает длину змеи."""
        self.positions.append(self.positions[-1])

    def decrease(self):
        """Уменьшает длину змеи."""
        last = self.positions[-1]
        last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.positions.pop(-1)

    def reset(self):
        """Обнуление игры в случае неудачи."""
        self.__init__()
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
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
    """Основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    poison = Poison()

    while True:
        clock.tick(SPEED)
        apple.draw()
        poison.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            snake.grow()
            snake.length += 1
        if snake.get_head_position() in snake.positions[1:-1]:
            snake.reset()
        if snake.get_head_position() == poison.position:
            poison.position = apple.randomize_position()
            if snake.length > 1:
                snake.decrease()
                snake.length -= 1
            else:
                snake.reset()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
