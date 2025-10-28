import random
from typing import List, Optional, Tuple

import pygame

# Константы игрового поля и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Возможные направления (в виде смещений в пикселях)
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Цвета (R, G, B)
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # чёрный
SNAKE_COLOR = (0, 255, 0)  # зелёный
APPLE_COLOR = (255, 0, 0)  # красный
ERASE_COLOR = BOARD_BACKGROUND_COLOR

# Частота обновления (кадров в секунду)
FPS = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты
    --------
    position: Tuple[int, int]
        Координаты верхнего левого угла ячейки объекта (в пикселях).
    body_color: Tuple[int, int, int]
        Цвет заполнения объекта (RGB).
    """

    def __init__(self, position: Optional[Tuple[int, int]] = None):
        """Инициализирует базовые атрибуты объекта."""
        if position is None:
            # Центральная точка экрана, выровненная по сетке
            center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
            center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
            position = (center_x, center_y)
        self.position: Tuple[int, int] = position
        self.body_color: Tuple[int, int, int] = (255, 255, 255)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовать объект на указанной поверхности.

        Подклассы должны переопределять этот метод.
        """
        pass


class Apple(GameObject):
    """
    Класс яблока — появляется в случайной клетке и хранит свою позицию.

    Методы
    ------
    randomize_position(occupied=None)
        Устанавливает случайную позицию яблока; опционально избегает занятых
        клеток.
    draw(surface)
        Рисует яблоко как заполненный квадрат размера GRID_SIZE.
    """

    def __init__(self, occupied: Optional[List[Tuple[int, int]]] = None):
        """Инициализирует яблоко и задаёт ему случайную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied)

    def randomize_position(
        self, occupied: Optional[List[Tuple[int, int]]] = None
    ) -> None:
        """
        Задать случайную позицию яблока на игровом поле.

        Параметры
        ---------
        occupied: Optional[List[Tuple[int, int]]]
            Список позиций (в пикселях), которые нужно избегать
            (например, сегменты змейки).
        """
        occupied_set = set(occupied) if occupied is not None else set()
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in occupied_set:
                self.position = (x, y)
                break

    def draw(self, surface: pygame.Surface) -> None:
        """Нарисовать яблоко как заполненный квадрат."""
        rect = pygame.Rect(self.position[0], self.position[1],
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """
    Класс змейки: хранит список сегментов и логику движения, роста и сброса.

    Атрибуты
    --------
    length: int
        Текущая длина змейки (количество сегментов).
    positions: List[Tuple[int, int]]
        Список позиций сегментов, начиная с головы.
    direction: Tuple[int, int]
        Текущее направление движения (dx, dy) в единицах клеток.
    next_direction: Optional[Tuple[int, int]]
        Направление, которое будет применено в следующем обновлении.
    body_color: Tuple[int, int, int]
        Цвет змейки.
    last: Optional[Tuple[int, int]]
        Позиция последнего сегмента перед его удалением (для "стирання"
        хвоста).
    """

    def __init__(self):
        """Инициализирует змейку в центральной точке."""
        super().__init__()
        self.length: int = 1
        center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions: List[Tuple[int, int]] = [(center_x, center_y)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.body_color = SNAKE_COLOR
        self.last: Optional[Tuple[int, int]] = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки (первый элемент списка)."""
        return self.positions[0]

    @staticmethod
    def _is_opposite(d1: Tuple[int, int], d2: Tuple[int, int]) -> bool:
        """Проверяет являются ли направления противоположными."""
        return d1[0] == -d2[0] and d1[1] == -d2[1]

    def update_direction(self) -> None:
        """
        Применяет next_direction, если оно задано и не является обратным
        по отношению к текущему направлению.
        """
        if self.next_direction and not self._is_opposite(
            self.direction, self.next_direction
        ):
            self.direction = self.next_direction
        self.next_direction = None

    def move(self) -> None:
        """
        Передвинуть змейку на одну клетку в текущем направлении.
        Добавляет новый сегмент головы и удаляет последний сегмент,
        если длина positions превышает self.length.
        Производит проверку выхода за пределы и обёртку по торцам.
        Также проверяет самопересечение и в этом случае вызывает reset().
        """
        current_head = self.get_head_position()
        dx, dy = self.direction
        new_x = (current_head[0] + dx) % SCREEN_WIDTH
        new_y = (current_head[1] + dy) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверка столкновения с собой (исключаем позицию neck)
        if new_head in self.positions[2:]:
            self.reset()
            return

        # Вставляем новую голову
        self.positions.insert(0, new_head)

        # Если слишком много сегментов (т.е. надо укоротить), то удалить хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            # Когда змейка выросла (после съедания яблока) — хвост не удаляем
            self.last = None

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовать змейку и стереть след предыдущего хвоста (если он есть).
        Стирание выполняется заливкой фонового цвета по координатам last.
        """
        # Стереть старый хвостный сегмент (если есть)
        if self.last is not None:
            rect = pygame.Rect(self.last[0], self.last[1],
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, ERASE_COLOR, rect)

        # Нарисовать все сегменты змейки
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def reset(self) -> None:
        """
        Сбросить змейку в начальное состояние (длина 1, в центре),
        задать случайное начальное направление.
        """
        self.length = 1
        center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(events: List[pygame.event.Event], snake: Snake) -> None:
    """
    Обработать события клавиатуры и задать next_direction для змейки.

    Управление:
        Стрелки и WASD.
    """
    for event in events:
        if event.type != pygame.KEYDOWN:
            continue
        if event.key in (pygame.K_UP, pygame.K_w):
            snake.next_direction = UP
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            snake.next_direction = DOWN
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            snake.next_direction = LEFT
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            snake.next_direction = RIGHT


def main() -> None:
    """Основная функция: инициализация Pygame и игровой цикл."""
    pygame.init()
    pygame.display.set_caption("Изгиб Питона")

    # Инициализация объектов
    snake = Snake()
    apple = Apple(occupied=snake.positions)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Обработка нажатий -> задать next_direction
        handle_keys(events, snake)

        # Применить направление и передвинуть змейку
        snake.update_direction()
        snake.move()

        # Если змейка съела яблоко — увеличить длину и переместить яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # После увеличения длины мы не удаляем хвост в move()
            apple.randomize_position(occupied=snake.positions)

        # Очистить экран (удаляем артефакты)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовать объекты
        apple.draw(screen)
        snake.draw(screen)

        # Обновить экран
        pygame.display.update()

        # Ограничить скорость игры
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
