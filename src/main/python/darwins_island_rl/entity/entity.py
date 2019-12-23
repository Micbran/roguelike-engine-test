
class Entity:
    """
    Base object to represent things on screen.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks = blocks
        self.name = name

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, dest_x, dest_y):
    for entity in entities:
        if entity.blocks and entity.x == dest_x and entity.y == dest_y:
            return entity

    return None
