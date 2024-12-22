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


class GameObject():
    """Базовый класс для игровых объектов."""

    def __init__(self):
        self.position = (0, 0)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Отрисовка объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока, которое ест змейка."""

    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        """Случайное размещение яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """Сброс состояния змейки."""
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Отрисовка змейки на экране."""
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

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Получение текущей позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки."""
        new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                    self.positions[0][1] + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()  # Удаляем последний сегмент


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
            elif event.key == pygame.K_ESCAPE:  # Выход из игры
                pygame.quit()
                raise SystemExit


def main():
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        snake.move()

        # Проверка выхода за границы экрана и перенос
        head_pos = snake.get_head_position()
        if head_pos[0] < 0:
            head_pos = (SCREEN_WIDTH - GRID_SIZE, head_pos[1])
        elif head_pos[0] >= SCREEN_WIDTH:
            head_pos = (0, head_pos[1])
        elif head_pos[1] < 0:
            head_pos = (head_pos[0], SCREEN_HEIGHT - GRID_SIZE)
        elif head_pos[1] >= SCREEN_HEIGHT:
            head_pos = (head_pos[0], 0)

        # Проверка на столкновение с самой собой
        if head_pos in snake.positions[1:]:
            snake.reset()  # Сброс змейки, если она столкнулась с собой
            apple = Apple()  # Создание нового яблока
            continue  # Перезапуск цикла

        snake.positions[0] = head_pos  # Обновляем позицию головы

        # Проверка на съедание яблока
        if head_pos == apple.position:
            snake.positions.append(snake.last)  # Увеличиваем длину змейки
            apple.randomize_position()  # Создаем новое яблоко

        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
