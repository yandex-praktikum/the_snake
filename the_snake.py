import pygame
import random
from typing import List, Tuple

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройки игры
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 20

class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position: Tuple[int, int] = None):
        """
        Инициализирует игровой объект.
        
        Args:
            position: Начальная позиция объекта (x, y) в пикселях
        """
        if position is None:
            position = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.position = position
        self.body_color = None
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Абстрактный метод для отрисовки объекта.
        
        Args:
            surface: Поверхность для отрисовки
        """
        pass

class Apple(GameObject):
    """Класс яблока, которое змейка должна съесть."""
    
    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = RED
        self.randomize_position()
    
    def randomize_position(self) -> None:
        """Устанавливает случайную позицию яблока в пределах игрового поля."""
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает яблоко на поверхности.
        
        Args:
            surface: Поверхность для отрисовки
        """
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)

class Snake(GameObject):
    """Класс змейки, управляемой игроком."""
    
    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__()
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)  # Начальное направление: вправо
        self.next_direction = None
    
    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем движение в противоположном направлении
            opposite_x = -self.direction[0]
            opposite_y = -self.direction[1]
            if self.next_direction[0] != opposite_x or self.next_direction[1] != opposite_y:
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self) -> None:
        """
        Перемещает змейку на одну клетку в текущем направлении.
        """
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        
        # Вычисляем новую позицию головы с учетом прохождения через стены
        new_x = (head_x + dir_x) % WINDOW_WIDTH
        new_y = (head_y + dir_y) % WINDOW_HEIGHT
        new_head = (new_x, new_y)
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def get_head_position(self) -> Tuple[int, int]:
        """
        Возвращает позицию головы змейки.
        
        Returns:
            Координаты головы (x, y)
        """
        return self.positions[0]
    
    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None
    
    def grow(self) -> None:
        """Увеличивает длину змейки на 1."""
        self.length += 1
    
    def check_self_collision(self) -> bool:
        """
        Проверяет столкновение змейки с самой собой.
        
        Returns:
            True если произошло столкновение, иначе False
        """
        head = self.get_head_position()
        return head in self.positions[1:]
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает змейку на поверхности.
        
        Args:
            surface: Поверхность для отрисовки
        """
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

def handle_keys(snake: Snake) -> None:
    """
    Обрабатывает нажатия клавиш для управления змейкой.
    
    Args:
        snake: Объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (CELL_SIZE, 0)

def main() -> None:
    """Основная функция игры."""
    # Инициализация окна
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()
    
    # Создание объектов
    snake = Snake()
    apple = Apple()
    
    # Основной игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)
        
        # Обновление направления змейки
        snake.update_direction()
        
        # Перемещение змейки
        snake.move()
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Проверка столкновения с собой
        if snake.check_self_collision():
            snake.reset()
        
        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        
        # Контроль FPS
        clock.tick(FPS)

if __name__ == "__main__":
    main()
