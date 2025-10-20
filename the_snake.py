import pygame
import random
import sys


class GameObject:
    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=(255, 0, 0))
        self.randomize_position()
    
    def randomize_position(self):
        x = random.randint(0, 31) * 20
        y = random.randint(0, 23) * 20
        self.position = (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect(self.position, (20, 20))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    def __init__(self):
        super().__init__(body_color=(0, 255, 0))
        self.positions = [(320, 240)]
        self.direction = (1, 0)
        self.next_direction = None
        self.last_position = None
    
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        self.last_position = self.positions[-1]
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * 20) % 640
        new_y = (head_y + dir_y * 20) % 480
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        self.positions.pop()
    
    def draw(self, surface):
        if self.last_position:
            rect = pygame.Rect(self.last_position, (20, 20))
            pygame.draw.rect(surface, (0, 0, 0), rect)
        for position in self.positions:
            rect = pygame.Rect(position, (20, 20))
            pygame.draw.rect(surface, self.body_color, rect)
    
    def get_head_position(self):
        return self.positions[0]
    
    def reset(self):
        self.positions = [(320, 240)]
        self.direction = (1, 0)
        self.next_direction = None


def handle_keys(snake):
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
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Snake Game')
    
    snake = Snake()
    apple = Apple()
    clock = pygame.time.Clock()
    
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last_position)
            apple.randomize_position()
        
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        
        screen.fill((0, 0, 0))
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()
