import pygame
import random


class GameObject:
    def __init__(self, position=None, body_color=(0, 0, 0)):
        """Базовые атрибуты объекта
        position: Позиция объекта
        body_color: Цвет объекта
        """
        self.position = position or (320, 240)
        self.body_color = body_color

    def draw(self, surface, size=20):
        """Объект на экране
        surface: Поверхность
        size: Размер объекта"""
        raise NotImplementedError("Метод draw должен быть переопределен в дочерних классах")


class Apple(GameObject):
    """Класс для яблока"""
    def __init__(self, position=None, body_color=(255, 0, 0)):
        """Инициализация яблока с цветом и случайной позицией
        position: Позиция яблока
        body_color: Цвет яблока"""
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Случайную позицию яблока на поле"""
        max_x = (640 // 20)
        max_y = (480 // 20) - 1
        self.position = (random.randint(0, max_x) * 20, random.randint(0, max_y) * 20)

    def draw(self, surface, size=20):
        """Яблоко как красный квадрат"""
        pygame.draw.rect(surface, self.body_color, pygame.Rect(self.position[0], self.position[1], size, size))


class Snake(GameObject):
    """Класс для змейки"""
    def __init__(self, position=None, body_color=(0, 255, 0), length=1):
        super().__init__(position, body_color)
        self.length = length
        self.positions = [self.position]
        self.direction = (20, 0)
        self.next_direction = (20, 0)

    def update_direction(self):
        """Обновляет направление движения змейки на основе следующего направления"""
        if self.next_direction != (-self.direction[0], -self.direction[1]):
            self.direction = self.next_direction

    def move(self, screen_width, screen_height):
        """Двигает змейку, добавляя новую голову и удаляя последний сегмент, если длина не увеличилась.
        Если змейка пересекает границы поля, она появляется с противоположной стороны
        creen_width: Ширина экрана
        screen_height: Высота экрана"""
        new_head = (
            (self.positions[0][0] + self.direction[0]) % screen_width,
            (self.positions[0][1] + self.direction[1]) % screen_height
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = (20, 0)

    def draw(self, screen):
        for segment in self.positions:
            pygame.draw.rect(screen, self.body_color, pygame.Rect(segment[0], segment[1], 20, 20))


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.next_direction = (0, -20)
    elif keys[pygame.K_DOWN]:
        snake.next_direction = (0, 20)
    elif keys[pygame.K_LEFT]:
        snake.next_direction = (-20, 0)
    elif keys[pygame.K_RIGHT]:
        snake.next_direction = (20, 0)


def main():
    pygame.init()

    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    game_over = False

    while not game_over:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        handle_keys(snake)
        snake.update_direction()
        snake.move(screen_width, screen_height)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            game_over = True
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    main()
