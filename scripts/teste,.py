import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class CircularHUD:
    def __init__(self, screen):
        self.screen = screen
        self.radius = 200
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.options = ["Weapon 1", "Weapon 2", "Armor", "Health Pack", "Grenade"]
        self.num_options = len(self.options)
        self.selected_option = 0

        # Load any necessary images for the HUD (not included in this example)
        # e.g., load an image for the circular background, icons, etc.

    def draw(self):
        self.screen.fill(BLACK)

        # Draw the circular background (not included in this example)
        # e.g., you can use an image for the circular background

        # Draw the options as text on the circle
        for i, option in enumerate(self.options):
            angle = math.radians(360 / self.num_options * i - 90)
            x = int(self.center[0] + self.radius * math.cos(angle))
            y = int(self.center[1] + self.radius * math.sin(angle))
            text_color = WHITE if i == self.selected_option else BLACK
            font = pygame.font.Font(None, 36)
            text = font.render(option, True, text_color)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

        # Draw an arc for the selected option
        angle_start = 360 / self.num_options * self.selected_option - 90
        angle_end = 360 / self.num_options * (self.selected_option + 1) - 90
        pygame.draw.arc(self.screen, RED, (self.center[0] - self.radius, self.center[1] - self.radius, self.radius * 2, self.radius * 2), angle_start, angle_end, 5)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 1) % self.num_options
            elif event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 1) % self.num_options

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Circular HUD Example")

    hud = CircularHUD(screen)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            hud.handle_input(event)

        hud.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
