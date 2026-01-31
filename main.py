import pygame, os
import random
import sys

# ==================== INITIALIZATION ====================
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
SKY_BLUE = (135, 206, 235)

GRAVITY = 0.4
FLAP_STRENGTH = -9
PIPE_SPEED = 3
PIPE_GAP = 170
PIPE_WIDTH = 80
PIPE_INTERVAL = 1500  # milliseconds between new pipes

# Window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird – Pygame")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 40, bold=True)
small_font = pygame.font.SysFont("arial", 24)

# ==================== CLASSES ====================

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 18

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        # Simple yellow bird with eye and beak
        pygame.draw.circle(screen, (255, 220, 0), (int(self.x), int(self.y)), self.radius)
        # eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 6)), 5)
        # beak
        pygame.draw.polygon(screen, (255, 180, 0), [
            (self.x + 14, self.y),
            (self.x + 26, self.y - 4),
            (self.x + 26, self.y + 4)
        ])

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(140, 380)  # top pipe bottom edge
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        bottom_y = self.height + PIPE_GAP
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, PIPE_WIDTH, HEIGHT - bottom_y))

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, bird_rect):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)


# ==================== GAME FUNCTIONS ====================

def draw_background():
    screen.fill(SKY_BLUE)
    # Simple ground
    pygame.draw.rect(screen, (240, 220, 140), (0, HEIGHT - 60, WIDTH, 60))
    # grass line
    pygame.draw.line(screen, (100, 180, 60), (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 6)


def show_text(text, font_obj, color, x, y, center=True):
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)


def game_over_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return True  # restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

        draw_background()
        show_text("GAME OVER", font, BLACK, WIDTH//2, 180)
        show_text(f"Score: {score}", font, BLACK, WIDTH//2, 260)
        show_text("Press SPACE or click to play again", small_font, BLACK, WIDTH//2, 340)

        pygame.display.flip()
        clock.tick(30)


# ==================== MAIN GAME LOOP ====================

def main():
    while True:  # allow restart
        bird = Bird()
        pipes = []
        score = 0
        last_pipe_time = pygame.time.get_ticks()
        game_active = True

        while game_active:
            dt = clock.tick(FPS)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if game_active:
                            bird.flap()
                        else:
                            game_active = True  # fallback

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_active:
                        bird.flap()

            if game_active:
                # Update
                bird.update()

                # Spawn pipes
                now = pygame.time.get_ticks()
                if now - last_pipe_time > PIPE_INTERVAL:
                    pipes.append(Pipe(WIDTH + 50))
                    last_pipe_time = now

                # Update pipes & scoring
                for pipe in pipes[:]:
                    pipe.update()
                    if pipe.off_screen():
                        pipes.remove(pipe)
                    if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                        pipe.passed = True
                        score += 1

                # Collision check
                bird_rect = bird.get_rect()
                if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT - 60:
                    game_active = False

                for pipe in pipes:
                    if pipe.collides_with(bird_rect):
                        game_active = False
                        break

            # Drawing
            draw_background()

            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Score display
            show_text(str(score), font, WHITE, WIDTH//2, 80)
            # semi-transparent black outline effect
            show_text(str(score), font, BLACK, WIDTH//2 + 2, 82)

            pygame.display.flip()

        # Game over → show screen and wait for restart
        if not game_over_screen(score):
            break  # user closed window during game over

    pygame.quit()


if __name__ == "__main__":
    main()
