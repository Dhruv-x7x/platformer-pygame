class Tilemap:
    def __init__(self, game, tileSize = 16):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offGridTiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 0, 'pos': (3 + i, 10)}
            # self.tilemap[';10' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    def render(self, surface):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize))