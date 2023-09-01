import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRASS_COLOR = (34, 139, 34)  # Grass green color
PLAYER_SIZE = 150
PLAYER_HITBOX_SIZE = 100
PLAYER_SPEED = 5
ENEMY_SIZE = 40
ENEMY_SPEED = 3
SCORE_FONT = pygame.font.Font(None, 36)
BLUE_COLOR = (0, 0, 255)  # Blue color for "Woof!"
SCORE_COLOR = (255, 255, 255)

# Messages
CUTE_DOG_MESSAGES = ["Bark!", "Woof!", "Ruff!", "Arf!"]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Birthday Bruce")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")  # Load a cool pixel guy image
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Wrap around the screen edges
        if self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect()
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.x = 0
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif side == "right":
            self.rect.x = WIDTH - ENEMY_SIZE
            self.rect.y = random.randint(0, HEIGHT - ENEMY_SIZE)
        elif side == "top":
            self.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            self.rect.y = 0
        elif side == "bottom":
            self.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            self.rect.y = HEIGHT - ENEMY_SIZE
        self.speed_x = random.randint(-ENEMY_SPEED, ENEMY_SPEED)
        self.speed_y = random.randint(-ENEMY_SPEED, ENEMY_SPEED)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.level = 1
        self.image = SCORE_FONT.render(f"Level {self.level} - Score: {self.value}", True, SCORE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 30)  # Center the text at the top of the screen

    def increase(self):
        self.value += 1
        if self.value % 10 == 0:
            self.level += 1
            display_milestone(random.choice(CUTE_DOG_MESSAGES))  # Display a random cute dog message
        else:
            self.image = SCORE_FONT.render(f"Level {self.level} - Score: {self.value}", True, SCORE_COLOR)

def display_milestone(message):
    milestone_font = pygame.font.Font(None, 72)
    milestone_text = milestone_font.render(message, True, BLUE_COLOR)  # Blue color for cute dog messages
    milestone_rect = milestone_text.get_rect()
    milestone_rect.center = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))  # Random position on the screen
    screen.blit(milestone_text, milestone_rect)
    pygame.display.flip()
    pygame.time.delay(1000)  # Display message for 1 second

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
score = Score()
player = Player()
all_sprites.add(player)

for _ in range(10):
    enemy = Enemy("ball.png")  # Use the image path
    all_sprites.add(enemy)
    enemies.add(enemy)

all_sprites.add(score)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hits = pygame.sprite.groupcollide(enemies, [player], True, False)  # Remove enemy on collision
    for hit in hits:
        enemy = Enemy("ball.png")  
        all_sprites.add(enemy)
        enemies.add(enemy)
        score.increase()

    all_sprites.update()

    screen.fill(GRASS_COLOR)  # Set the background color to grass green

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
