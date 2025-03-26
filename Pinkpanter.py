import pygame
import random
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("پلنگ صورتی")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)
BLUE = (0, 0, 255)

# Load online images (replace with actual URLs if needed)
# Note: In a real implementation, you would download these images first
try:
    player_img = pygame.image.load("https://example.com/pink_panther.png")
    player_img = pygame.transform.scale(player_img, (50, 50))
except:
    # Fallback if image can't be loaded
    player_img = pygame.Surface((50, 50))
    player_img.fill(PINK)

try:
    obstacle_img = pygame.image.load("https://example.com/obstacle.png")
    obstacle_img = pygame.transform.scale(obstacle_img, (40, 40))
except:
    obstacle_img = pygame.Surface((40, 40))
    obstacle_img.fill(BLUE)

try:
    background_img = pygame.image.load("https://example.com/background.png")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_img.fill(WHITE)

# Load sounds
try:
    jump_sound = mixer.Sound("https://example.com/jump.wav")
except:
    jump_sound = None

try:
    game_over_sound = mixer.Sound("https://example.com/game_over.wav")
except:
    game_over_sound = None

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.jumping = False
        
    def update(self):
        # Gravity
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y
        
        # Ground collision
        if self.rect.y > SCREEN_HEIGHT - 100:
            self.rect.y = SCREEN_HEIGHT - 100
            self.velocity_y = 0
            self.jumping = False
    
    def jump(self):
        if not self.jumping:
            self.velocity_y = -12
            self.jumping = True
            if jump_sound:
                jump_sound.play()

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 100 - self.rect.height
        self.speed = 5
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()

# Game setup
def game():
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)
    
    obstacle_timer = 0
    running = True
    game_over = False
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    game_over = False
                    score = 0
                    all_sprites.empty()
                    obstacles.empty()
                    player = Player()
                    all_sprites.add(player)
        
        if not game_over:
            # Update
            all_sprites.update()
            
            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer > random.randint(50, 150):
                obstacle = Obstacle()
                obstacles.add(obstacle)
                all_sprites.add(obstacle)
                obstacle_timer = 0
            
            # Collision detection
            if pygame.sprite.spritecollide(player, obstacles, False):
                game_over = True
                if game_over_sound:
                    game_over_sound.play()
            
            # Increase score
            score += 0.1
        
        # Drawing
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        
        # Score display
        score_text = font.render(f"امتیاز: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("بازی تمام شد! دکمه R را برای شروع مجدد بزنید", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    game()
