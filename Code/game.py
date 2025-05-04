import pygame
import pytmx
import pyscroll
from player import Player
from map import MapManager

class Game:
    def __init__(self):        
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Nochnitsa")
        self.player = Player()
        self.map_manager = MapManager(self.screen,self.player)

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
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit