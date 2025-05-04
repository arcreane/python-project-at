import pygame
import random
import math

class FalloutLockpickMiniGame:
    def __init__(self):
        self.active = False
        self.angle = 90  # initial angle (middle)
        self.correct_angle = random.randint(30, 150)
        self.tries = 3
        self.font = pygame.font.SysFont("couriernew", 28)
        self.status = ""
        self.success = False
        self.finished = False
        pygame.mixer.init()
        self.success_sound = pygame.mixer.Sound("../Audio/success.mp3")
        self.fail_sound = pygame.mixer.Sound("../Audio/lock.mp3")

    def start(self):
        self.active = True
        self.angle = 90
        self.correct_angle = random.randint(30, 150)
        self.tries = 3
        self.status = ""
        self.success = False
        self.finished = False

    def handle_event(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.angle = max(0, self.angle - 5)
            elif event.key == pygame.K_RIGHT:
                self.angle = min(180, self.angle + 5)
            elif event.key == pygame.K_SPACE:
                self.check_angle()
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                self.status = "Crochetage annulé."

    def check_angle(self):
        if abs(self.angle - self.correct_angle) <= 5:
            self.status = "VERROU OUVERT"
            self.success = True
            self.success_sound.play()
            self.active = False
            self.finished = True
        else:
            self.tries -= 1
            self.fail_sound.play()
            if self.tries <= 0:
                self.status = "ÉCHEC - EPINGLE CASSÉE"
                self.active = False
                self.finished = True
            else:
                self.status = f"Mauvais angle... Il reste {self.tries} essai(s)."

    def update(self):
        pass

    def render(self, screen):
        if not self.active:
            return

        screen.fill((0, 0, 0))
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        gray = (100, 100, 100)

        center_x, center_y = 400, 300
        lock_radius = 60

        pygame.draw.rect(screen, green, (50, 50, 700, 500), 2)

        pygame.draw.circle(screen, gray, (center_x, center_y), lock_radius)

        pygame.draw.line(screen, yellow, (center_x, center_y + lock_radius), (center_x, center_y + lock_radius + 40), 5)

        pin_length = 80
        angle_rad = math.radians(self.angle - 90)
        end_x = center_x + pin_length * math.cos(angle_rad)
        end_y = center_y + pin_length * math.sin(angle_rad)
        pygame.draw.line(screen, green, (center_x, center_y), (end_x, end_y), 3)

        if self.status:
            status_txt = self.font.render(self.status, True, green)
            screen.blit(status_txt, (80, 440))

        tries_txt = self.font.render(f"Crochets restants : {self.tries}", True, green)
        screen.blit(tries_txt, (80, 480))

        esc_txt = self.font.render("[ECHAP] Quitter    [←][→] Bouger épingle    [ESPACE] Forcer", True, green)
        screen.blit(esc_txt, (80, 520))

    def should_teleport(self):
        return self.success and self.finished

    def teleport_to_secret_room(self, map_manager):
        if self.should_teleport():
            map_manager.current_map = "secret_room"
            map_manager.teleport_player("secret_room_spawn")
            self.finished = False

