import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_BLOCK = 10
SNAKE_SPEED = 10  # Slower speed

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(100, 50), (90, 50), (80, 50)]
        self.direction = (SNAKE_BLOCK, 0)  # Moving right

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)  # Add new head
        self.body.pop()  # Remove last segment

    def grow(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)  # Add new head

    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def get_positions(self):
        return self.body

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (
            random.randint(1, (SCREEN_WIDTH // SNAKE_BLOCK) - 1) * SNAKE_BLOCK,
            random.randint(1, (SCREEN_HEIGHT // SNAKE_BLOCK) - 1) * SNAKE_BLOCK,
        )

    def get_position(self):
        return self.position

# Game loop
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -SNAKE_BLOCK))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, SNAKE_BLOCK))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-SNAKE_BLOCK, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((SNAKE_BLOCK, 0))
                elif event.key == pygame.K_m:  # Press 'M' to maximize the window
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.NOFRAME)
                    pygame.display.set_caption("Snake Game (Maximized)")

        snake.move()

        # Check for collision with food
        if snake.get_positions()[0] == food.get_position():
            snake.grow()
            food.spawn()
            score += 1

        # Check for collision with walls or self
        head_x, head_y = snake.get_positions()[0]
        if (head_x < 0 or head_x >= SCREEN_WIDTH or 
            head_y < 0 or head_y >= SCREEN_HEIGHT or 
            len(snake.get_positions()) != len(set(snake.get_positions()))):
            print(f"Game Over! Your score: {score}")
            pygame.quit()
            sys.exit()

        # Drawing
        screen.fill(BLACK)
        for segment in snake.get_positions():
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK))
        pygame.draw.rect(screen, RED, pygame.Rect(food.get_position()[0], food.get_position()[1], SNAKE_BLOCK, SNAKE_BLOCK))

        # Draw the score
        font = pygame.font.SysFont("Arial", 25)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(SNAKE_SPEED)  # Control the speed of the game

if __name__ == "__main__":
    main()
