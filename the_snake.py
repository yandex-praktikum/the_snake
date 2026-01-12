# Импортируем функцию randint из модуля random для генерации случайных чисел
from random import randint

# Импортируем библиотеку pygame для создания игры
import pygame

# Константы для размеров поля и сетки:
# Размеры игрового окна в пикселях
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
# Размер одной клетки сетки в пикселях
GRID_SIZE = 20
# Ширина и высота в клетках (не в пикселях!)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # 640 ÷ 20 = 32 клетки по ширине
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 480 ÷ 20 = 24 клетки по высоте

# Направления движения змейки:
# Каждое направление - это пара чисел (x, y)
UP = (0, -1)    # x не меняется, y уменьшается (движение вверх)
DOWN = (0, 1)   # x не меняется, y увеличивается (движение вниз)
LEFT = (-1, 0)  # x уменьшается, y не меняется (движение влево)
RIGHT = (1, 0)  # x увеличивается, y не меняется (движение вправо)

# Цвета в формате RGB (Red, Green, Blue):
BOARD_BACKGROUND_COLOR = (0, 0, 0)      # Черный цвет фона
BORDER_COLOR = (93, 216, 228)           # Голубой цвет границы
APPLE_COLOR = (255, 0, 0)               # Красный цвет яблока
SNAKE_COLOR = (0, 255, 0)               # Зеленый цвет змейки

# Скорость движения змейки (кадров в секунду):
SPEED = 1  # Чем больше число, тем быстрее змейка

# Настройка игрового окна:
# Создаем окно размером 640x480 пикселей
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
# Создаем объект для контроля частоты кадров
clock = pygame.time.Clock()


class GameObject:
    

    def __init__(self, body_color=None):
        """Инициализирует игровой объект с начальными значениями."""
        # Начальная позиция объекта - в центре экрана
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Цвет объекта
        self.body_color = body_color

    def draw(self):
        
        pass


class Apple(GameObject):
    

    def __init__(self):
        
        # Вызываем конструктор родительского класса с красным цветом
        super().__init__(APPLE_COLOR)
        # Устанавливаем случайное положение яблока
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на сетке."""
        # Генерируем случайные координаты в пределах сетки
        # randint(0, GRID_WIDTH - 1) дает число от 0 до 31
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE  # Умножаем на GRID_SIZE для перевода в пиксели
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        # Создаем прямоугольник (Rect) с координатами яблока и размерами клетки
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        # Рисуем залитый прямоугольник (яблоко)
        pygame.draw.rect(screen, self.body_color, rect)
        # Рисуем рамку вокруг яблока (толщина линии = 1)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    

    def __init__(self):
        
        # Вызываем конструктор родительского класса с зеленым цветом
        super().__init__(SNAKE_COLOR)
        # Сбрасываем змейку в начальное состояние
        self.reset()

    def reset(self):
       
        # Длина змейки (начинаем с 1 - только голова)
        self.length = 1
        # Список позиций всех сегментов змейки (от головы к хвосту)
        self.positions = [self.position]
        # Текущее направление движения
        self.direction = RIGHT  # Начинаем движение вправо
        # Следующее направление (изменяется при нажатии клавиш)
        self.next_direction = None
        # Последняя позиция (для очистки хвоста при движении)
        self.last = None

    def update_direction(self):
        
        # Если было задано новое направление
        if self.next_direction:
            # Меняем текущее направление
            self.direction = self.next_direction
            # Сбрасываем следующее направление
            self.next_direction = None

    def get_head_position(self):
       
        return self.positions[0]

    def move(self):
        
        # Получаем текущие координаты головы
        head_x, head_y = self.get_head_position()
        # Получаем направление движения
        dir_x, dir_y = self.direction
        
        # Вычисляем новые координаты головы
        # % SCREEN_WIDTH обеспечивает телепортацию через границы экрана
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Сохраняем последнюю позицию (хвост) для очистки экрана
        self.last = self.positions[-1] if self.positions else None

        # Добавляем новую позицию головы в начало списка
        self.positions.insert(0, new_position)

        # Если змейка стала длиннее, чем должна быть, удаляем последний элемент (хвост)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        
        # Отрисовка тела змейки (все сегменты кроме головы)
        for position in self.positions[:-1]:  # [:-1] означает "все кроме последнего"
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки (последний сегмент в списке)
        if self.positions:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Очищаем старую позицию хвоста (чтобы не оставался след)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш.
    """
    
    # Получаем все события (нажатия клавиш, закрытие окна и т.д.)
    for event in pygame.event.get():
        # Если пользователь закрыл окно
        if event.type == pygame.QUIT:
            # Закрываем pygame
            pygame.quit()
            # Выходим из программы
            raise SystemExit
        # Если была нажата клавиша
        elif event.type == pygame.KEYDOWN:
            # Вверх: проверяем, что змейка не движется вниз (чтобы не развернуться на 180°)
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            # Вниз: проверяем, что змейка не движется вверх
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            # Влево: проверяем, что змейка не движется вправо
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            # Вправо: проверяем, что змейка не движется влево
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры - игровой цикл."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()  # Создаем змейку
    apple = Apple()  # Создаем яблоко

    # Игровой цикл - выполняется бесконечно, пока игра не закончится
    while True:
        # Контролируем скорость игры (кадров в секунду)
        clock.tick(SPEED)

        # 1. Обработка действий пользователя
        handle_keys(snake)

        # 2. Обновление направления движения змейки
        snake.update_direction()

        # 3. Движение змейки
        snake.move()

        # 4. Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            # Увеличиваем длину змейки
            snake.length += 1
            # Перемещаем яблоко в случайное место
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            # Пока яблоко на змейке - генерируем новую позицию
            while apple.position in snake.positions:
                apple.randomize_position()

        # 5. Проверка столкновения змейки с собой
        # Проверяем, не находится ли голова в теле змейки
        if snake.get_head_position() in snake.positions[1:]:  # [1:] означает "все кроме головы"
            # Если столкнулась - сбрасываем игру
            snake.reset()

        # 6. Отрисовка объектов
        # Заливаем экран черным цветом (очищаем)
        screen.fill(BOARD_BACKGROUND_COLOR)
        # Рисуем змейку
        snake.draw()
        # Рисуем яблоко
        apple.draw()

        # 7. Обновление экрана (показываем нарисованное)
        pygame.display.update()


if __name__ == '__main__':
    # Запускаем игру, только если файл запущен напрямую
    main()
