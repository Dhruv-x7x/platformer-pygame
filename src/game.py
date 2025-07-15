import pygame
import sys

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init() # initialize pygame

        pygame.display.set_caption("Platformer Game") # edit the title of the window
        self.screen = pygame.display.set_mode((640, 480)) # create the display window
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock() # create the clock, we need this to set the target FPS, or the cpu will try to go as fast as possible
        
        self.assets = {
            'grass': load_images('grass'),
            'stone': load_images('stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds')
        }

        self.clouds = Clouds(self.assets['clouds'], count=12)

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        self.movement = [False, False] # LEFT RIGHT

        self.tilemap = Tilemap(self)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0)) # if we don't have this, the assets moving across the screen leave a trail
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, renderScroll)

            self.tilemap.render(self.display, offset=renderScroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=renderScroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()