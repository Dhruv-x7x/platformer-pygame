import pygame
import sys

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init() # initialize pygame

        pygame.display.set_caption("Platformer Game - Level Editor") # edit the title of the window
        self.screen = pygame.display.set_mode((640, 480)) # create the display window
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock() # create the clock, we need this to set the target FPS, or the cpu will try to go as fast as possible
        
        self.assets = {
            'grass': load_images('grass'),
            'stone': load_images('stone'),
            'decor': load_images('decor')
        }

        self.tileList = list(self.assets)
        self.tileGroup = 0
        self.tileVariant = 0

        self.movement = [False, False, False, False] 

        self.tilemap = Tilemap(self)
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
    
        self.scroll = [0, 0]

        self.clicking = False
        self.rightClicking = False
        self.shift = False

        self.onGrid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, renderScroll)

            currentTile = self.assets[self.tileList[self.tileGroup]][self.tileVariant].copy()
            currentTile.set_alpha(100)

            mPos = pygame.mouse.get_pos()
            mPos = (mPos[0] / RENDER_SCALE, mPos[1] / RENDER_SCALE)

            tilePos = (int((mPos[0] + self.scroll[0]) // self.tilemap.tileSize), int((mPos[1] + self.scroll[1]) // self.tilemap.tileSize))

            if self.onGrid:
                self.display.blit(currentTile, (tilePos[0] * self.tilemap.tileSize - self.scroll[0], tilePos[1] * self.tilemap.tileSize - self.scroll[1]))
            else:
                self.display.blit(currentTile, mPos)

            if self.clicking and self.onGrid:
                self.tilemap.tilemap[str(tilePos[0]) + ';' + str(tilePos[1])] = {'type': self.tileList[self.tileGroup], 'variant': self.tileVariant, 'pos': tilePos}
            if self.rightClicking:
                tileLoc = str(tilePos[0]) + ';' + str(tilePos[1])
                if tileLoc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tileLoc]
                for tile in self.tilemap.offGridTiles.copy():
                    tileImg = self.assets[tile['type']][tile['variant']]
                    tileR = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tileImg.get_width(), tileImg.get_height())
                    if tileR.collidepoint(mPos):
                        self.tilemap.offGridTiles.remove(tile)

            self.display.blit(currentTile, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.onGrid:
                            self.tilemap.offGridTiles.append({'type': self.tileList[self.tileGroup], 'variant': self.tileVariant, 'pos': (mPos[0] + self.scroll[0], mPos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.rightClicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tileVariant = (self.tileVariant - 1) % len(self.assets[self.tileList[self.tileGroup]])
                        if event.button == 5:
                            self.tileVariant = (self.tileVariant + 1) % len(self.assets[self.tileList[self.tileGroup]])
                    else:
                        if event.button == 4:
                            self.tileGroup = (self.tileGroup - 1) % len(self.tileList)
                            self.tileVariant = 0
                        if event.button == 5:
                            self.tileGroup = (self.tileGroup + 1) % len(self.tileList)
                            self.tileVariant = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.onGrid = not self.onGrid

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.rightClicking = False
        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()