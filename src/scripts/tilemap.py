import pygame

NEIGHBOURHOOD_OFFSETS = ((1,0), (1,1), (0,1), (-1,1), (0,0), (-1,0), (-1,-1), (0,-1), (1,-1))
PHYSICS_TILES = {'stone', 'grass'}

class Tilemap:
    def __init__(self, game, tileSize = 16):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offGridTiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 0, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 0, 'pos': (10, 5 + i)}

    def tiles_around(self, pos):
        tiles = []
        tileLoc = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize)) # converting pixel coords to grid coords

        for offset in NEIGHBOURHOOD_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ';' + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])
        return tiles # return neighborhood tiles
    
    def physics_enabled_tiles(self, pos):
        rects = [] # we will create rects around the entities that have physics enabled on them to do the collision detection

        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def render(self, surface, offset=(0, 0)):
        for loc in self.offGridTiles:
            tile = self.offGridTiles[loc]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tileSize, (offset[0] + surface.get_width()) // self.tileSize):
            for y in range(offset[1] // self.tileSize, (offset[1] + surface.get_height()) // self.tileSize):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))