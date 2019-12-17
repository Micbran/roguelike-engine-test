
class Tile:
    """
    Class to represent tiles on the map.
    Can be a Movement Block Tile (Can't be moved through)
    Can be a Sight Block Tile (Can't be seen through)
    """
    def __init__(self, move_block, sight_block=None):
        self.move_block = move_block

        if not sight_block:
            sight_block = move_block

        self.sight_block = sight_block
