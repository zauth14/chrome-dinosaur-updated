import pygame
import os
import random

pygame.init()

# Screen setup
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Museum Heist")

# Load assets
RUNNING = pygame.image.load(os.path.join("Assets/Thief", "ThiefRun1.png")).convert_alpha()
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets/Other", "MuseumTrack.png")).convert(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
WEBPAGE = pygame.image.load(os.path.join("Assets/Other", "WebMockup.png")).convert_alpha()
RESTART_BTN = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets/Other", "Reset.png")).convert_alpha(),
    (80, 80)
)

COP_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets/Obstacles", "Cop.png")).convert_alpha(),
    (250, 250)
)
MOTION_ZONE_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets/Obstacles", "MotionZone.png")).convert_alpha(),
    (200, 200)
)
LASER_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets/Obstacles", "LaserMaze.png")).convert_alpha(),
    (80, 80)
)

# Preload masks
COP_MASK = pygame.mask.from_surface(COP_IMG)
SENSOR_MASK = pygame.mask.from_surface(MOTION_ZONE_IMG)
LASER_MASK = pygame.mask.from_surface(LASER_IMG)

TARGET_POINTS = 3000

class Thief:
    X_POS = 80
    Y_POS = SCREEN_HEIGHT - 180
    JUMP_VEL = 9

    def __init__(self):
        self.image = RUNNING
        self.thief_jump = False
        self.jump_vel = self.JUMP_VEL
        self.y_initial = self.Y_POS
        self.thief_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, userInput):
        if self.thief_jump:
            self.jump()
        if userInput[pygame.K_SPACE] and not self.thief_jump:
            self.thief_jump = True

    def jump(self):
        if self.thief_jump:
            self.thief_rect.y -= self.jump_vel * 3.5
            self.jump_vel -= 0.7
        if self.jump_vel < -self.JUMP_VEL:
            self.thief_jump = False
            self.jump_vel = self.JUMP_VEL
            self.thief_rect.y = self.y_initial

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.thief_rect)

class Obstacle:
    def __init__(self, image, y_pos, speed=0):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = y_pos
        self.speed = speed

    def update(self):
        self.rect.x -= game_speed + self.speed
        if self.rect.right < 0 and self in obstacles:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PatrollingCop(Obstacle):
    def __init__(self):
        super().__init__(COP_IMG, SCREEN_HEIGHT - 300, speed=2)
        self.mask = COP_MASK

class MotionSensorZone(Obstacle):
    def __init__(self):
        super().__init__(MOTION_ZONE_IMG, SCREEN_HEIGHT - 260)
        self.mask = SENSOR_MASK

class LaserMaze(Obstacle):
    def __init__(self):
        super().__init__(LASER_IMG, SCREEN_HEIGHT - 230)
        self.mask = LASER_MASK

def main():
    global game_speed, x_pos_bg, points, obstacles

    player = Thief()
    game_speed = 12
    x_pos_bg = 0
    points = 0
    obstacles = []
    font = pygame.font.Font('freesansbold.ttf', 20)
    clock = pygame.time.Clock()
    run = True

    obstacle_timer = 0
    min_spawn_delay = 50
    max_spawn_delay = 120
    next_spawn_time = random.randint(min_spawn_delay, max_spawn_delay)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (950, 40))

    def background():
        global x_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, 0))
        SCREEN.blit(BG, (image_width + x_pos_bg, 0))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        userInput = pygame.key.get_pressed()
        SCREEN.fill((255, 255, 255))

        background()
        player.draw(SCREEN)
        player.update(userInput)

        obstacle_timer += 1
        if obstacle_timer >= next_spawn_time:
            if len(obstacles) == 0 or obstacles[-1].rect.x < SCREEN_WIDTH - 300:
                obstacle_type = random.choice(['cop', 'sensor', 'laser'])
                if obstacle_type == 'cop':
                    obstacles.append(PatrollingCop())
                elif obstacle_type == 'sensor':
                    obstacles.append(MotionSensorZone())
                elif obstacle_type == 'laser':
                    obstacles.append(LaserMaze())
                obstacle_timer = 0
                next_spawn_time = random.randint(min_spawn_delay, max_spawn_delay)

        for obstacle in obstacles[:]:
            obstacle.draw(SCREEN)
            obstacle.update()
            offset = (obstacle.rect.x - player.thief_rect.x, obstacle.rect.y - player.thief_rect.y)
            if player.mask.overlap(obstacle.mask, offset):
                pygame.time.delay(1000)
                game_over_screen()
                return

        score()

        if points >= TARGET_POINTS:
            pygame.time.delay(1000)
            show_loaded_page()
            return

        pygame.display.update()

def game_over_screen():
    font = pygame.font.Font('freesansbold.ttf', 32)
    run = True
    restart_x = SCREEN_WIDTH // 2 - 40
    restart_y = 350
    restart_rect = pygame.Rect(restart_x, restart_y, 80, 80)

    while run:
        SCREEN.fill((255, 255, 255))
        text = font.render("GAME OVER", True, (0, 0, 0))
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
        SCREEN.blit(RESTART_BTN, (restart_x, restart_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(pygame.mouse.get_pos()):
                    main()
                    return

def intro_screen():
    font = pygame.font.Font('freesansbold.ttf', 30)
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        text = font.render("Museum Heist: WiFi Gone", True, (0, 0, 0))
        instructions = font.render(f"Reach {TARGET_POINTS} points to escape the museum", True, (0, 0, 0))
        start_text = font.render("Press any key to start", True, (0, 0, 0))

        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
        SCREEN.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 250))
        SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                main()
                run = False

def show_loaded_page():
    run = True
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    message_font = pygame.font.Font('freesansbold.ttf', 28)
    code_font = pygame.font.Font('freesansbold.ttf', 30)

    congrats_text = title_font.render("Congratulations!", True, (0, 100, 0))
    wifi_text = message_font.render("WiFi has been successfully restored.", True, (0, 0, 0))
    code_text = code_font.render("SECRET CODE: AHA — All Hail Avocados", True, (128, 0, 128))

    while run:
        SCREEN.fill((240, 210, 100))  # Light yellow ochre
        total_height = congrats_text.get_height() + wifi_text.get_height() + code_text.get_height() + 40
        start_y = (SCREEN_HEIGHT - total_height) // 2

        SCREEN.blit(congrats_text, ((SCREEN_WIDTH - congrats_text.get_width()) // 2, start_y))
        SCREEN.blit(wifi_text, ((SCREEN_WIDTH - wifi_text.get_width()) // 2, start_y + 50))
        SCREEN.blit(code_text, ((SCREEN_WIDTH - code_text.get_width()) // 2, start_y + 100))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

intro_screen()
