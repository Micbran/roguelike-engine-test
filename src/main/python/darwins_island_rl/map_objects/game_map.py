from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rectangle
from entity.entity import Entity
from entity.components.combat_component import Combat
from entity.components.ai import BasicMonster
from entity.components.item import Item
from entity.components.stairs import Stairs
from render_help import RenderOrder
from entity.components.item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from game_messages import Message
from random_utils import random_choice_from_dict, from_dungeon_level

import tcod

# TODO if controls get mappable, these will need to be updated
fireball_target_message = Message("Select a target for fireball. Esc to cancel, keypad * to cycle targets.", tcod.light_cyan)
confuse_target_message = Message("Select a target for confuse. Esc to cancel, keypad * to cycle targets.", tcod.light_cyan)


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()
        self.dungeon_level = dungeon_level

    def init_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def is_blocked(self, x, y):
        return self.tiles[x][y].move_block

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0  # Potential candidate for refactoring (just use rooms len)

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)

            x_pos = randint(0, map_width - width - 1)
            y_pos = randint(0, map_height - height - 1)

            rand_room = Rectangle(x_pos, y_pos, width, height)

            for other_room in rooms:
                if rand_room.intersect(other_room):
                    break
            else:  # Means that room was valid; no intersections
                self.create_room(rand_room)

                center_x, center_y = rand_room.center()

                center_of_last_room_x = center_x
                center_of_last_room_y = center_y

                if num_rooms == 0:
                    player.x = center_x
                    player.y = center_y
                else:
                    prev_x, prev_y = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_hori_tunnel(prev_x, center_x, prev_y)
                        self.create_vert_tunnel(prev_y, center_y, center_x)
                    else:
                        self.create_vert_tunnel(prev_y, center_y, prev_x)
                        self.create_hori_tunnel(prev_x, center_x, center_y)

                self.place_entities(rand_room, entities)

                rooms.append(rand_room)
                num_rooms += 1
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', tcod.white, 'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room: Rectangle):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].move_block = False
                self.tiles[x][y].sight_block = False  # Could be refactored into a function

    def create_hori_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].move_block = False
            self.tiles[x][y].sight_block = False

    def create_vert_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].move_block = False
            self.tiles[x][y].sight_block = False

    def place_entities(self, room, entities):
        number_of_entities = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        number_of_items = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        monster_chances = {'orc': 80,
                           'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)}

        item_chances = {'healing_potion': 35,
                        'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
                        'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
                        'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)}

        for new_entity in range(number_of_entities):
            new_entity_x = randint(room.x1 + 1, room.x2 - 1)
            new_entity_y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == new_entity_x and entity.y == new_entity_y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == 'orc':
                    orc_combat = Combat(vigor=20, agility=0, brawn=4, xp=35)
                    ai_component = BasicMonster()
                    new_entity = Entity(new_entity_x, new_entity_y, 'o', tcod.desaturated_green, "Orc", blocks=True, combat=orc_combat, ai=ai_component, render_order=RenderOrder.ACTOR)
                elif monster_choice == 'troll':
                    troll_combat = Combat(vigor=30, agility=2, brawn=8, xp=100)
                    ai_component = BasicMonster()
                    new_entity = Entity(new_entity_x, new_entity_y, 'T', tcod.darker_green, "Troll", blocks=True, combat=troll_combat, ai=ai_component, render_order=RenderOrder.ACTOR)

                entities.append(new_entity)

        for new_item in range(number_of_items):
            new_item_x = randint(room.x1 + 1, room.x2 - 1)
            new_item_y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == new_item_x and entity.y == new_item_y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    new_item = Entity(new_item_x, new_item_y, "!", tcod.violet, "Healing Potion", item=item_component, render_order=RenderOrder.ITEM)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=fireball_target_message, damage=25, radius=3, max_range=7)
                    new_item = Entity(new_item_x, new_item_y, "?", tcod.red, "Fireball Scroll", render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=confuse_target_message, max_range=5)
                    new_item = Entity(new_item_x, new_item_y, "?", tcod.light_pink, "Confusion Scroll", render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, max_range=5)
                    new_item = Entity(new_item_x, new_item_y, "?", tcod.darker_cyan, "Lightning Scroll", render_order=RenderOrder.ITEM, item=item_component)

                entities.append(new_item)

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.init_tiles()
        self.make_map(constants['MAX_ROOMS'], constants['ROOM_MIN_SIZE'], constants['ROOM_MAX_SIZE'], constants['MAP_WIDTH'], constants['MAP_HEIGHT'], player, entities)

        player.combat.heal(player.combat.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest and recover your strength.', tcod.light_violet))

        return entities
