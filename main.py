import pygame, sys, random, time

pygame.init()

WIDTH, HEIGHT = 1280, 720
FONT = pygame.font.SysFont("Consolas", int(WIDTH / 20))

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

# Paddles
player = pygame.Rect(0, 0, 10, 100)
player.center = (WIDTH - 100, HEIGHT / 2)

opponent = pygame.Rect(0, 0, 10, 100)
opponent.center = (100, HEIGHT / 2)

player_score, opponent_score = 0, 0

# Ball
ball = pygame.Rect(0, 0, 20, 20)
ball.center = (WIDTH / 2, HEIGHT / 2)
x_speed, y_speed = 1, 1

# === PowerUp class ===
class PowerUp:
    def __init__(self, type, color):
        self.type = type
        self.color = color
        self.rect = pygame.Rect(-100, -100, 50, 50)
        self.spawn_time = pygame.time.get_ticks()
        self.active = False
        self.activated_at = 0

    def spawn(self):
        self.rect.x = random.randint(200, WIDTH - 200)
        self.rect.y = random.randint(100, HEIGHT - 100)
        self.spawn_time = pygame.time.get_ticks()

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def activate(self):
        self.active = True
        self.activated_at = pygame.time.get_ticks()
        self.hide()

    def update(self, current_time):
        if self.active and current_time - self.activated_at > 10000:
            self.active = False

    def should_respawn(self, current_time):
        return not self.active and self.rect.x < 0 and current_time - self.spawn_time >= 30000

    def draw(self, screen):
        if self.rect.x > 0:
            pygame.draw.rect(screen, self.color, self.rect)

# === Create powerups ===
powerups = [
    PowerUp("paddle", "blue"),
    PowerUp("slow", "green"),
    PowerUp("freeze", "red"),
]
for p in powerups:
    p.spawn()

# Delay start
time.sleep(2)

while True:
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP] and player.top > 0:
        player.top -= 2
    if keys_pressed[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.bottom += 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update powerups
    current_time = pygame.time.get_ticks()
    for p in powerups:
        if p.should_respawn(current_time):
            p.spawn()
        p.update(current_time)

    # Ball collisions with edges
    if ball.y >= HEIGHT:
        y_speed = -1
    if ball.y <= 0:
        y_speed = 1
    if ball.x <= 0:
        player_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])
    if ball.x >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])

    if player.colliderect(ball):
        x_speed = -1
    if opponent.colliderect(ball):
        x_speed = 1

    # Check collisions with powerups
    for p in powerups:
        if ball.colliderect(p.rect):
            p.activate()

    # Apply powerup effects
    paddle_active = any(p.active for p in powerups if p.type == "paddle")
    slow_active = any(p.active for p in powerups if p.type == "slow")
    freeze_active = any(p.active for p in powerups if p.type == "freeze")

    # Paddle size effect
    player.height = 200 if paddle_active else 100

    # Ball speed effect
    ball_speed = 1 if slow_active else 2

    # Opponent AI movement (frozen if active)
    if not freeze_active:
        if opponent.y < ball.y:
            opponent.top += 1
        if opponent.bottom > ball.y:
            opponent.bottom -= 1

    # Move ball
    ball.x += x_speed * ball_speed
    ball.y += y_speed * ball_speed

    # Drawing
    SCREEN.fill("Black")
    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.circle(SCREEN, "white", ball.center, 10)

    for p in powerups:
        p.draw(SCREEN)

    player_score_text = FONT.render(str(player_score), True, "white")
    opponent_score_text = FONT.render(str(opponent_score), True, "white")
    SCREEN.blit(player_score_text, (WIDTH / 2 + 50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH / 2 - 50, 50))

    pygame.display.update()
    CLOCK.tick(300)



#att lägga till: text som visar hur länge powerupsen är aktiverade
#startmeny och slutmeny
