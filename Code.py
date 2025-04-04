import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 40)

# Load bird image or use a placeholder
bird_img = pygame.Surface((34, 24))
bird_img.fill((255, 255, 0))  # Yellow

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, 34, 24)

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y)

    def jump(self):
        self.vel = JUMP_STRENGTH

    def draw(self, screen):
        screen.blit(bird_img, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

    def update(self):
        self.x -= 4
        self.top_rect.x = self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

def draw_text(text, x, y):
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (x, y))

def main():
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()

        # Update pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

        # Add new pipes
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe(WIDTH))

        # Remove off-screen pipes
        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        # Collision detection
        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                return main()

        # Ground and ceiling collision
        if bird.y > HEIGHT or bird.y < 0:
            return main()

        bird.draw(screen)
        draw_text(f"Score: {score}", 10, 10)
        pygame.display.update()

if __name__ == "__main__":
    main()
