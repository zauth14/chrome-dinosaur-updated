import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = pygame.image.load(os.path.join("Assets/Thief", "ThiefRun1.png"))
JUMPING = RUNNING 

BG = pygame.image.load(os.path.join("Assets/Other", "MuseumTrack.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
WEBPAGE = pygame.image.load(os.path.join("Assets/Other", "WebMockup.png"))

COP_IMG = pygame.image.load(os.path.join("Assets/Obstacles", "Cop.png"))
MOTION_ZONE_IMG = pygame.image.load(os.path.join("Assets/Obstacles", "MotionZone.png"))
LASER_IMG = pygame.image.load(os.path.join("Assets/Obstacles", "LaserMaze.png"))

TARGET_POINTS = 3000

class Thief:
    X_POS = 80
    Y_POS = SCREEN_HEIGHT - 180
    JUMP_VEL = 8.5

    def __init__(self):
        self.image = RUNNING
        self.thief_jump = False
        self.jump_vel = self.JUMP_VEL
        self.y_initial = self.Y_POS
        self.thief_rect = self.image.get_rect(topleft=(self.X_POS, self.Y_POS))

    def update(self, userInput):
        if self.thief_jump:
            self.jump()

        if userInput[pygame.K_SPACE] and not self.thief_jump:
            self.thief_jump = True

    def jump(self):
        if self.thief_jump:
            self.thief_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
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
        if self.rect.right < 0:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PatrollingCop(Obstacle):
    def __init__(self):
        super().__init__(COP_IMG, SCREEN_HEIGHT - 180, speed=2)

class MotionSensorZone(Obstacle):
    def __init__(self):
        super().__init__(MOTION_ZONE_IMG, SCREEN_HEIGHT - 180)

class LaserMaze(Obstacle):
    def __init__(self):
        super().__init__(LASER_IMG, SCREEN_HEIGHT - 180)


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles

    player = Thief()
    game_speed = 20
    x_pos_bg = 0
    points = 0
    obstacles = []
    font = pygame.font.Font('freesansbold.ttf', 20)
    clock = pygame.time.Clock()
    run = True

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, 0))
        SCREEN.blit(BG, (image_width + x_pos_bg, 0))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        userInput = pygame.key.get_pressed()
        SCREEN.fill((255, 255, 255))

        background()
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            obstacle_type = random.choice(['cop', 'sensor', 'laser'])
            if obstacle_type == 'cop':
                obstacles.append(PatrollingCop())
            elif obstacle_type == 'sensor':
                obstacles.append(MotionSensorZone())
            elif obstacle_type == 'laser':
                obstacles.append(LaserMaze())

        for obstacle in obstacles[:]:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.thief_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                return

        score()

        if points >= TARGET_POINTS:
            pygame.time.delay(1000)
            show_loaded_page()
            return

        pygame.display.update()
        clock.tick(30)


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
    font = pygame.font.Font('freesansbold.ttf', 28)
    code_font = pygame.font.Font('freesansbold.ttf', 40)

    while run:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(WEBPAGE, (100, 50))

        code_text = code_font.render("AUTH CODE: 7281-WIFI-RESTORED", True, (0, 0, 0))
        SCREEN.blit(code_text, (SCREEN_WIDTH // 2 - code_text.get_width() // 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return


intro_screen()