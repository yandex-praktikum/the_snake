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


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """
        Инициализация игрового объекта.
        
        Args:
            position (tuple): Координаты объекта (x, y)
            body_color (tuple): Цвет объекта в формате RGB
        """
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализация змейки в начальной позиции."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки.
        
        Returns:
            tuple: Кортеж (x, y) с координатами головы
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на один шаг в текущем направлении.
        
        Returns:
            bool: True если произошло столкновение с собой, иначе False
        """
        # Сохраняем последнюю позицию для очистки
        if len(self.positions) > 0:
            self.last = self.positions[-1]

        # Получаем текущую позицию головы
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head in self.positions:
            self.reset()
            return True

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()

        return False

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовка тела змейки (кроме головы)
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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


def handle_keys(game_object):
    """Обработка нажатий клавиш пользователем.
    
    Args:
        game_object: Объект змейки, которым управляет игрок
    """
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
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        # Обработка действий пользователя
        handle_keys(snake)
        
        # Обновление направления змейки
        snake.update_direction()
        
        # Движение змейки
        snake_collided = snake.move()
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убеждаемся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        
        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
