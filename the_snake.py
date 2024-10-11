import pygame
from random import randint

pygame.init()

SCR_WIDTH, SCR_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCR_WIDTH // GRID_SIZE
GRID_HEIGHT = SCR_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)

INITIAL_SPEED = 10
SPEED_INCREMENT = 5
MIN_SPEED = 10
MAX_SPEED = 25

scr = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
screen = pygame.Surface((150, 150))


class GameObject():
    """
    Fake
    comment
    """

    position = (0, 0)
    body_color = (0, 0, 0)

    def __int__(self):
        """
        Fake
        comment
        """
        return 0

    def draw():
        """
        Fake
        comment
        """
        return 0


class Snake(GameObject):
    """
    Публичный класс Snake
    Класс для взаимодействия со змейкой
    """

    position = (0, 0)
    body_color = (0, 0, 0)
    positions = [(0, 0), (0, 0), (0, 0)]
    direction = 'UP'

    def __init__(self):
        """
        Инициализирует экземпляр змейки.
        Устанавливает начальные позиции, направление, флаг роста и счет.
        """
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
            (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)
        ]
        self.direction = RIGHT
        self.grow = False
        self.score = 0

    def get_head_position():
        """
        Fake
        comment
        """
        return 0

    def reset():
        """
        Fake
        comment
        """
        return 0

    def move(self):
        """
        Перемещает змейку в нужном направлении. Проверяет столкновение с собой.
        Если столкновение произошло, возвращает False, иначе True.
        """
        current_head = self.positions[0]
        x, y = self.direction
        a = (current_head[0] + x) % GRID_WIDTH
        b = (current_head[1] + y) % GRID_HEIGHT
        new_head = (a, b)

        if new_head in self.positions:
            return False
        else:
            self.positions.insert(0, new_head)
            if not self.grow:
                self.positions.pop()
            self.grow = False
            return True

    def update_direction(self, direction):
        """
        Изменяет направление движения змейки.
        Параметры: direction - направление в виде кортежа (dx, dy)
        """
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self):
        """
        Данная функция предназначена для
        отрисовки змейки на экране.
        """
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(scr, SNAKE_COLOR, rect)
            pygame.draw.rect(scr, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Публичный класс Apple
    Определяет поведение яблока в игре.
    """

    position = (0, 0)
    body_color = (0, 0, 0)

    def __init__(self):
        """
        Инициализирует экземпляр яблока. Устанавливает начальную позицию
        яблока случайным образом в пределах игрового поля.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)

    def draw(self):
        """
        Данная функция предназначена для
        отрисовки яблока на экране.
        """
        a = self.position[0] * GRID_SIZE
        b = self.position[1] * GRID_SIZE
        rect = pygame.Rect(a, b, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(scr, APPLE_COLOR, rect)
        pygame.draw.rect(scr, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """
        Сбрасывает позицию яблока на новую случайную координату.
        Устанавливает новую случайную позицию яблока в пределах игрового поля.
        """
        a = randint(0, GRID_WIDTH - 1)
        b = randint(0, GRID_HEIGHT - 1)
        self.position = (a, b)


def handle_keys(snake):
    """
    Данная функция предназначена для
    определения управление в игре.
    """
    global speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key in (
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT
            ):
                direction_map = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT
                }
                snake.update_direction((direction_map[event.key]))
            elif event.key == pygame.K_q:
                speed = max(MIN_SPEED, speed - SPEED_INCREMENT)
            elif event.key == pygame.K_w:
                speed = min(MAX_SPEED, speed + SPEED_INCREMENT)


def game_over_scr(score, high_score):
    """
    Данная функция предназначена для
    определения работы экрана после смерти
    """
    while True:
        scr.fill(BOARD_BACKGROUND_COLOR)

        game_over_text = font.render('Вы проиграли!', True, WHITE)
        score_text = font.render(f'Ваш результат: {score}', True, WHITE)
        high_score_text = font.render(f'Рекорд: {high_score}', True, WHITE)
        exit_text = font.render('ESC - выйти', True, WHITE)
        continue_text = font.render('SPACE - продолжить', True, WHITE)

        scr.blit(game_over_text, (SCR_WIDTH // 2 - 50, SCR_HEIGHT // 2 - 50))
        scr.blit(score_text, (SCR_WIDTH // 2 - 70, SCR_HEIGHT // 2 - 28))
        scr.blit(high_score_text, (SCR_WIDTH // 2 - 35, SCR_HEIGHT // 2))
        scr.blit(exit_text, (SCR_WIDTH // 2 - 50, SCR_HEIGHT // 2 + 28))
        scr.blit(continue_text, (SCR_WIDTH // 2 - 90, SCR_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    return


def main():
    """
    Общий класс игры
    Взаимодействует с остальными классами
    """
    global speed
    speed = INITIAL_SPEED
    snake = Snake()
    apple = Apple()
    high_score = 0

    while True:
        handle_keys(snake)

        if not snake.move():
            if snake.score > high_score:
                high_score = snake.score
            game_over_scr(snake.score, high_score)
            snake = Snake()
            apple.randomize_position()

        if snake.positions[0] == apple.position:
            snake.grow = True
            snake.score += 1
            apple.randomize_position()

        scr.fill(BOARD_BACKGROUND_COLOR)

        pygame.draw.rect(scr, BORDER_COLOR, (0, 0, SCR_WIDTH, SCR_HEIGHT), 2)

        snake.draw()
        apple.draw()

        score_text = font.render(f'Счет: {snake.score}', True, WHITE)
        scr.blit(score_text, (10, 10))
        speed_text = font.render(f'Скорость: {speed}', True, WHITE)
        scr.blit(speed_text, (10, 30))

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
