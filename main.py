import os
import pygame  # Import pygame to create the game

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
        window.blit(self.image, (self.rect.x, self.rect.y) )

# -------------------------
# Player class (can move)
# -------------------------
class Player(GameSprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

        self.x_speed = 0  # Movement speed on X axis
        self.y_speed = 0  # Movement speed on Y axis

    def move_horizontal(self):
        # Move horizontally only if the next position stays within the allowed boundaries
        if 0 <= self.rect.x + self.x_speed <= 620:
            self.rect.x += self.x_speed

        # Check for collisions with any platform (barriers)
        for p in pygame.sprite.spritecollide(self, barriers, False):
            if self.x_speed > 0:
                # Moving right → align player's right side with the platform's left side
                self.rect.right = p.rect.left
            elif self.x_speed < 0:
                # Moving left → align player's left side with the platform's right side
                self.rect.left = p.rect.right

    def move_vertical(self):
        # Move vertically only if the next position stays within the allowed boundaries
        if 0 <= self.rect.y + self.y_speed <= 420:
            self.rect.y += self.y_speed

        # Check for vertical collisions with platforms
        for p in pygame.sprite.spritecollide(self, barriers, False):
            if self.y_speed > 0:
                # Moving down → align player's bottom with the platform's top
                self.rect.bottom = p.rect.top
            elif self.y_speed < 0:
                # Moving up → align player's top with the platform's bottom
                self.rect.top = p.rect.bottom

    def update(self):
        # Update movement separately for each axis
        # This avoids "sticking" and handles collisions properly
        self.move_horizontal()
        self.move_vertical()

pygame.init()  # Initialize pygame

# -------------------------
# Window configuration
# -------------------------
WIN_WIDTH  = 700
WIN_HEIGHT = 500
BACKGROUND_COLOR = (119, 210, 223)  # RGB color for the window background

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Create window
pygame.display.set_caption("Maze Runner Game")             # Window title

# -------------------------
# Image paths configuration
# -------------------------
BASE_DIR    = os.path.dirname(__file__)         # Folder where this file is located
IMAGES_PATH = os.path.join(BASE_DIR, "Images")  # Images folder

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

#creando un grupo de paredes
barriers = pygame.sprite.Group()                # NEW
# añadiendo paredes al grupo
barriers.add(w1)                                # NEW
barriers.add(w2)                                # NEW

# Create Pac-Man player
pacman = Player(
    "1-2.png",
    5, WIN_HEIGHT - 80,
    80, 80
)
monster = GameSprite('cyborg.png', WIN_WIDTH - 80, 180, 80, 80)
final_sprite = GameSprite('pac-1.png', WIN_WIDTH - 85, WIN_HEIGHT - 100, 80, 80)

# -------------------------
# Win and lose images
# -------------------------

# --- Load end-game images once ---
game_over_img = pygame.image.load(os.path.join(IMAGES_PATH, "game-over-3.jpg"))
thumb_img = pygame.image.load(os.path.join(IMAGES_PATH, "thumb_1.jpg"))

# Pre-scale images to avoid doing it during gameplay
game_over_ratio = game_over_img.get_width() // game_over_img.get_height()
game_over_scaled = pygame.transform.scale(game_over_img, (WIN_HEIGHT * game_over_ratio, WIN_HEIGHT))

thumb_scaled = pygame.transform.scale(thumb_img, (WIN_WIDTH, WIN_HEIGHT))

def show_end_screen(image, position=(0, 0)):
    """Draws an end screen image."""
    window.fill((255, 255, 255))
    window.blit(image, position)


# -------------------------
# Main game loop
# -------------------------
finish = False # End the game        NEW
run = True
while run:
    pygame.time.delay(50)          # Small delay to control game speed

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

    if not finish:
        window.fill(BACKGROUND_COLOR)

        # Draw game objects
        w1.draw()
        w2.draw()
        barriers.draw(window)
        monster.draw()
        final_sprite.draw()
        pacman.draw()

        # Activate movement
        pacman.update()

        # Collision with monster → Game Over
        if pygame.sprite.collide_rect(pacman, monster):
            finish = True
            show_end_screen(game_over_scaled, (90, 0))

        # Collision with final flag → Victory
        elif pygame.sprite.collide_rect(pacman, final_sprite):
            finish = True
            show_end_screen(thumb_scaled)

    pygame.display.update()  # Refresh the screen
