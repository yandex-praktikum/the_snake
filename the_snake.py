from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.
class GameObject:

    # Набор позиций тела питона
    positions = [[300, 220]]
    # Цвет тела питона
    body_color_snake = (0, 200, 0)
    # Позиция для затирания
    last = [0, 0]
    # Признак удлинения тела Snake
    flag = False
    # Текущая позиция и цвет яблока
    position = [randint(0, 31) * 20, randint(0, 23) * 20]
    body_color_apple = (200, 0, 200)
    # Атрибуты направления движения
    direction = RIGHT
    next_direction = None

class Snake(GameObject):

    # Метод draw класса Snake
    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color_snake, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color_snake, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
               (self.last[0], self.last[1]),
               (GRID_SIZE, GRID_SIZE)
            )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    # Метод обработки действий пользователя
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод изменения набора позиций тела Snake
    def move_snake(self):
        if self.direction == DOWN:
            self.positions.insert(
                0, list(map(sum, zip(self.positions[0], [0, 20])))
            )
            if self.flag is False:
                self.last = self.positions[-1]
                self.positions.pop(-1)
            else:
                self.flag = False
        if self.direction == UP:
            self.positions.insert(
                0, list(map(sum, zip(self.positions[0], [0, -20])))
            )
            if self.flag is False:
                self.last = self.positions[-1]
                self.positions.pop(-1)
            else:
                self.flag = False
        if self.direction == RIGHT:
            self.positions.insert(
                0, list(map(sum, zip(self.positions[0], [20, 0])))
            )
            if self.flag is False:
                self.last = self.positions[-1]
                self.positions.pop(-1)
            else:
                self.flag = False
        if self.direction == LEFT:
            self.positions.insert(
                0, list(map(sum, zip(self.positions[0], [-20, 0])))
            )
            if self.flag is False:
                self.last = self.positions[-1]
                self.positions.pop(-1)
            else:
                self.flag = False

class Apple(GameObject):

    # Метод draw класса Apple
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color_apple, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def new_position_apple(self, position_snake_head):
        self.position = [randint(0, 31) * 20, randint(0, 23) * 20]

def main():
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        # Прорисовка Snake и Apple
        snake.draw(screen)
        apple.draw(screen)

        # Установка скорости движения Snake
        clock.tick(SPEED)

        # Опрос клавиатуры на определение команды изменения направления
        snake.handle_keys()

        # Изменение направление при наличии команды
        snake.update_direction()

        # Изменение набора позиций тела Snake
        # в зависимости от текущего направления движения
        snake.move_snake()

        # Проверка совпадения головы Snake и apple
        # В случае совпадения, генерация нового яблока
        if snake.positions[0] == apple.position:
            apple.new_position_apple(snake.position)
            snake.flag = True

        # Проверка ввыхода за пределы поля
        if (
            snake.positions[0][0] < 0 or snake.positions[0][0] > 620 or
            snake.positions[0][1] < 0 or snake.positions[0][1] > 460
        ):
            print('Игра окончена. Вы столкнулись со стеной')
            break

        pygame.display.update()

if __name__ == '__main__':
    main()
