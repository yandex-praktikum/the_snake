import pygame
import random
import sys


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле (x, y)
        body_color (tuple): Цвет объекта в формате RGB
    """

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """
        Инициализирует игровой объект.

        Args:
            position (tuple): Начальная позиция объекта (по умолчанию (0, 0))
            body_color (tuple): Цвет объекта (по умолчанию черный)
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        pass


class Apple(GameObject):
    """
    Класс для яблока в игре.

    Атрибуты:
        body_color (tuple): Цвет яблока (красный)
        position (tuple): Позиция яблока на игровом поле
    """

    def __init__(self, position=(0, 0)):
        """
        Инициализирует яблоко.

        Args:
            position (tuple): Начальная позиция яблока
        """
        super().__init__(position, (255, 0, 0))  # Красный цвет
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайное положение яблока на игровом поле.

        Координаты выбираются так, чтобы яблоко оказалось в пределах
        игрового поля и было выровнено по сетке 20x20 пикселей.
        """
        x = random.randint(0, 31) * 20  # 32 ячейки по горизонтали (0-31)
        y = random.randint(0, 23) * 20  # 24 ячейки по вертикали (0-23)
        self.position = (x, y)

    def draw(self, surface):
        """
        Отрисовывает яблоко на игровой поверхности.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(self.position, (20, 20))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)  # Черная рамка


class Snake(GameObject):
    """
    Класс для змейки в игре.

    Атрибуты:
        length (int): Длина змейки
        positions (list): Список позиций всех сегментов тела
        direction (tuple): Текущее направление движения
        next_direction (tuple): Следующее направление движения
        body_color (tuple): Цвет змейки (зеленый)
        last_position (tuple): Последняя позиция хвоста (для затирания следа)
    """

    def __init__(self, position=(320, 240)):
        """
        Инициализирует змейку.

        Args:
            position (tuple): Начальная позиция змейки (по умолчанию центр)
        """
        super().__init__(position, (0, 255, 0))  # Зеленый цвет
        self.length = 1
        self.positions = [position]
        self.direction = (1, 0)  # Движение вправо
        self.next_direction = None
        self.last_position = None

    def update_direction(self):
        """
        Обновляет направление движения змейки.

        Если было задано следующее направление, применяет его.
        """
        if self.next_direction:
            # Проверяем, чтобы змейка не могла двигаться
            # в противоположном направлении
            opposite_x = self.direction[0] * -1
            opposite_y = self.direction[1] * -1

            if (self.next_direction[0] != opposite_x or
                    self.next_direction[1] != opposite_y):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки, добавляя новую голову и удаляя хвост.

        Сохраняет последнюю позицию хвоста для затирания следа.
        """
        # Сохраняем позицию хвоста для затирания
        self.last_position = self.positions[-1] if self.positions else None

        # Получаем текущую позицию головы
        head_x, head_y = self.positions[0]

        # Вычисляем новую позицию головы
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * 20) % 640  # Прохождение через стены
        new_y = (head_y + dir_y * 20) % 480

        new_head = (new_x, new_y)

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """
        Отрисовывает змейку на экране и затирает след.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        # Затираем след (последнюю позицию хвоста)
        if self.last_position:
            rect = pygame.Rect(self.last_position, (20, 20))
            pygame.draw.rect(surface, (0, 0, 0), rect)  # Черный цвет фона

        # Отрисовываем все сегменты змейки
        for position in self.positions:
            rect = pygame.Rect(position, (20, 20))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)  # Черная рамка

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Returns:
            tuple: Координаты головы змейки (x, y)
        """
        return self.positions[0] if self.positions else (0, 0)

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)  # Движение вправо
        self.next_direction = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.

    Args:
        snake (Snake): Объект змейки, направление которой нужно изменить
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (1, 0)


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    # Инициализация Pygame
    pygame.init()
    window_size = (640, 480)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Изгиб Питона')

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Настройка часов для контроля FPS
    clock = pygame.time.Clock()

    # Главный игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление направления движения змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            # Проверяем, чтобы яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения змейки с собой
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill((0, 0, 0))  # Черный фон
        apple.draw(screen)
        snake.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Контроль FPS
        clock.tick(10)  # 10 кадров в секунду для комфортной игры


if __name__ == "__main__":
    main()
