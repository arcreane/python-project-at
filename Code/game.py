import pygame
import pytmx
import pyscroll
from audio import AudioManager
from Code.dialog import DialogBox
from player import Player
from map import MapManager
from Code.minigame import CodeMiniGame

class Game:
    def __init__(self):
        music_map = {
            "world": f"../Audio/Nuitforet.mp3",
            "world2": f"../Audio/Angoisse.mp3",
            "house": f"../Audio/House.mp3",
            "house2": f"../Audio/mystery.mp3"
        }
        self.audio = AudioManager(music_map)
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Nochnitsa")
        self.player = Player()
        self.map_manager = MapManager(self,self.screen,self.player)
        self.dialog_box = DialogBox()
        self.minigame = CodeMiniGame()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()

        running = True

        while running:

            self.player.save_loaction()
            self.handle_input()
            self.update()
            self.map_manager.draw()

            if self.minigame.active:
                self.minigame.update()
                self.minigame.render(self.screen)
            else:
                self.dialog_box.render(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.minigame.active:
                    self.minigame.handle_event(event)  # 👈 ESSENTIEL
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.map_manager.check_npc_collisions(self.dialog_box)
                        elif event.key == pygame.K_e:
                            if self.map_manager.current_map == "hospital":
                                zone = self.map_manager.get_object("computer_zone")
                                if self.player.feet.colliderect(pygame.Rect(zone.x, zone.y, zone.width, zone.height)):
                                    self.minigame.start()

            clock.tick(60)

        pygame.quit