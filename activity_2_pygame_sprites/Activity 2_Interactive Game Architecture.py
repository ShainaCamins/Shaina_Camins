import pygame
import random
import sys

# Initialize Pygame modules
pygame.init()
pygame.font.init()

# Display Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Activity 2: Sprite System & Collision Arena')
clock = pygame.time.Clock()
FPS = 60

# Palette & Fonts
COLOR_BG = (20, 24, 33)
COLOR_PLAYER = (52, 152, 219)      # Dodger Blue
COLOR_TARGET = (231, 76, 60)       # Crimson Red
COLOR_OBSTACLE = (149, 165, 166)   # Concrete Gray
COLOR_PARTICLE = (241, 196, 15)    # Warm Yellow
COLOR_TEXT = (236, 240, 241)       # Bright White

FONT_HUD = pygame.font.SysFont('Arial', 18, bold=True)
FONT_TITLE = pygame.font.SysFont('Arial', 24, bold=True)

# -----------------------------------------------------------------------------
# 1. SPRITE CLASSES (OBJECT-ORIENTED ENCAPSULATION)
# -----------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    """Interactive player entity controlled via Arrow Keys or WASD."""
    def __init__(self):
        super().__init__()
        # 32-bit Surface with Alpha Transparency for clean circular rendering
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLOR_PLAYER, (20, 20), 20)
        pygame.draw.circle(self.image, (255, 255, 255), (20, 20), 20, 2)
        
        # Rect Coordinate System using center anchor
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def move_axis(self, dx, dy, obstacles):
        """Moves player per axis and resolves collisions independently."""
        # --- Horizontal Movement ---
        if dx != 0:
            self.rect.x += dx
            hits = pygame.sprite.spritecollide(self, obstacles, False)
            for obstacle in hits:
                if dx > 0:  # Moving right
                    self.rect.right = obstacle.rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = obstacle.rect.right

        # --- Vertical Movement ---
        if dy != 0:
            self.rect.y += dy
            hits = pygame.sprite.spritecollide(self, obstacles, False)
            for obstacle in hits:
                if dy > 0:  # Moving down
                    self.rect.bottom = obstacle.rect.top
                elif dy < 0:  # Moving up
                    self.rect.top = obstacle.rect.bottom

        # Screen Boundary Enforcement
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > SCREEN_WIDTH - 10:
            self.rect.right = SCREEN_WIDTH - 10
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10


class Target(pygame.sprite.Sprite):
    """Collectible entity spawned at random positions across the arena."""
    def __init__(self, existing_obstacles):
        super().__init__()
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLOR_TARGET, (0, 0, 28, 28), border_radius=6)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 28, 28), 2, border_radius=6)
        
        self.rect = self.image.get_rect()
        self.respawn(existing_obstacles)

    def respawn(self, obstacles_group):
        """Relocate target ensuring no overlap with static obstacles."""
        valid_position = False
        while not valid_position:
            rand_x = random.randint(40, SCREEN_WIDTH - 60)
            rand_y = random.randint(80, SCREEN_HEIGHT - 60)
            self.rect.topleft = (rand_x, rand_y)
            
            # Verify no immediate overlap with obstacles
            if not pygame.sprite.spritecollideany(self, obstacles_group):
                valid_position = True


class Obstacle(pygame.sprite.Sprite):
    """Static wall object blocking movement."""
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_OBSTACLE)
        pygame.draw.rect(self.image, (200, 200, 200), (0, 0, width, height), 2)
        self.rect = self.image.get_rect(topleft=(x, y))


class Particle(pygame.sprite.Sprite):
    """Short-lived visual particle burst on collision."""
    def __init__(self, pos_x, pos_y):
        super().__init__()
        size = random.randint(4, 8)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((*COLOR_PARTICLE, random.randint(180, 255)))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
        self.vx = random.uniform(-3.0, 3.0)
        self.vy = random.uniform(-3.0, 3.0)
        self.lifetime = random.randint(15, 30)

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


# -----------------------------------------------------------------------------
# 2. GAME SETUP & SPRITE GROUPS
# -----------------------------------------------------------------------------
all_sprites = pygame.sprite.Group()
targets_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()

# Instantiate Player
player = Player()
all_sprites.add(player)

# Instantiate Obstacles (Placed safely away from center spawn)
arena_obstacles = [
    Obstacle(150, 150, 120, 20),
    Obstacle(530, 150, 120, 20),
    Obstacle(200, 430, 150, 20),
    Obstacle(450, 430, 150, 20)
]
for obs in arena_obstacles:
    obstacles_group.add(obs)
    all_sprites.add(obs)

# Instantiate Collectible Targets
for _ in range(3):
    target = Target(obstacles_group)
    targets_group.add(target)
    all_sprites.add(target)

score = 0

# -----------------------------------------------------------------------------
# 3. MAIN GAME LOOP
# -----------------------------------------------------------------------------
running = True
while running:
    # A. Regulate FPS
    clock.tick(FPS)

    # B. Process Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                score = 0
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # C. Handle Continuous Key Press Movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= player.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += player.speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= player.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += player.speed

    # Execute movement with axis-aligned collision checks
    player.move_axis(dx, dy, obstacles_group)

    # D. Target Collection Check
    collected_targets = pygame.sprite.spritecollide(player, targets_group, False)
    for target in collected_targets:
        score += 10
        for _ in range(12):
            particles_group.add(Particle(target.rect.centerx, target.rect.centery))
        target.respawn(obstacles_group)

    particles_group.update()

    # E. Render Display
    screen.fill(COLOR_BG)

    all_sprites.draw(screen)
    particles_group.draw(screen)

    # Render HUD
    hud_panel = pygame.Surface((SCREEN_WIDTH, 50), pygame.SRCALPHA)
    hud_panel.fill((30, 36, 50, 220))
    screen.blit(hud_panel, (0, 0))
    pygame.draw.line(screen, (70, 80, 100), (0, 50), (SCREEN_WIDTH, 50), 2)

    txt_title = FONT_TITLE.render("Sprite Arena Engine", True, COLOR_TEXT)
    txt_score = FONT_HUD.render(f"Score: {score}", True, COLOR_PARTICLE)
    txt_fps = FONT_HUD.render(f"FPS: {int(clock.get_fps())}", True, COLOR_TEXT)

    screen.blit(txt_title, (20, 10))
    screen.blit(txt_score, (360, 15))
    screen.blit(txt_fps, (710, 15))

    # F. Flip Display
    pygame.display.flip()

pygame.quit()
sys.exit()