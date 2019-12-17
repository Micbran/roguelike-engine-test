from src.main.python.darwins_island_rl.map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].move_block = True
        tiles[30][22].sight_block = True
        tiles[31][22].move_block = True
        tiles[31][22].sight_block = True
        tiles[32][22].move_block = True
        tiles[32][22].sight_block = True

        return tiles

    def is_blocked(self, x, y):
        return self.tiles[x][y].move_block
