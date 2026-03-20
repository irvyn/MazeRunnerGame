import os
import pygame  # Import pygame to create the game

pygame.init()  # Initialize pygame

# -------------------------
# Window configuration
# -------------------------
WIN_WIDTH = 700
WIN_HEIGHT = 500
BACKGROUND_COLOR = (119, 210, 223)  # RGB color for the window background

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Create window
pygame.display.set_caption("Maze Runner Game")             # Window title

# -------------------------
# Image paths configuration
# -------------------------
BASE_DIR = os.path.dirname(__file__)            # Folder where this file is located
IMAGES_PATH = os.path.join(BASE_DIR, "Images")  # Images folder

# -------------------------
# Base class for all sprites
# -------------------------
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__()  # Initialize Sprite class

        # Load image from the given path
        self.image = pygame.image.load(os.path.join(IMAGES_PATH, image_path))

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (width, height))

        # Get the rectangle (position and size)
        self.rect = self.image.get_rect()
        self.rect.x = x  # X position
        self.rect.y = y  # Y position

    def draw(self):
        # Draw the sprite on the window
        window.blit(self.image, (self.rect.x, self.rect.y))


# -------------------------
# Player class (can move)
# -------------------------
class Player(GameSprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

        self.x_speed = 0  # Movement speed on X axis
        self.y_speed = 0  # Movement speed on Y axis

    def update(self):
        # Update position based on speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


# -------------------------
# Create game objects
# -------------------------

# Two wall/platform sprites
w1 = GameSprite(
    "platform.png",
    WIN_WIDTH / 2 - WIN_WIDTH / 3, WIN_HEIGHT / 2,
    300, 50
)

w2 = GameSprite(
    "platform_v.png",
    370, 100,
    50, 400
)

# Create Pac-Man player
pacman = Player(
    "1-2.png",
    5, WIN_HEIGHT - 80,
    80, 80
)

# -------------------------
# Main game loop
# -------------------------
run = True
while run:
    pygame.time.delay(50)          # Small delay to control game speed
    window.fill(BACKGROUND_COLOR)  # Fill the background

    # Check events (keyboard, closing window, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # Exit the game

        # When a key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.x_speed = -5
            if event.key == pygame.K_RIGHT:
                pacman.x_speed = 5
            if event.key == pygame.K_UP:
                pacman.y_speed = -5
            if event.key == pygame.K_DOWN:
                pacman.y_speed = 5

        # When a key is released
        elif event.type == pygame.KEYUP:
            # Stop horizontal movement
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                pacman.x_speed = 0

            # Stop vertical movement
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                pacman.y_speed = 0

    # Update and draw sprites
    # w1.draw()
    # w2.draw()
    pacman.update()
    pacman.draw()

    pygame.display.update()  # Refresh the screen
