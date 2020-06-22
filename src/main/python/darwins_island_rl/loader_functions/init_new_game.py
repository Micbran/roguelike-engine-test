import tcod
import os.path

from entity.components.combat_component import Combat
from entity.components.inventory import Inventory
from entity.components.level import Level
from entity.entity import Entity
from entity.components.equipment import Equipment
from entity.components.equippable import Equippable
from map_objects.game_map import GameMap
from game_messages import MessageLog
from game_state import GameStates
from render_help import RenderOrder

from equipment_slots import EquipmentSlots


def get_constants():
    WINDOW_TITLE = 'RL Engine Test'
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    HP_MESSAGE_PANEL_WIDTH = 20
    HP_MESSAGE_PANEL_HEIGHT = 7
    HP_MESSAGE_PANEL_Y_LOC = SCREEN_HEIGHT - HP_MESSAGE_PANEL_HEIGHT

    MESSAGE_X_LOC = HP_MESSAGE_PANEL_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - HP_MESSAGE_PANEL_WIDTH - 2
    MESSAGE_HEIGHT = HP_MESSAGE_PANEL_HEIGHT - 1

    FOV_ALG = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    MAP_WIDTH = 80
    MAP_HEIGHT = 43
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30
    MAX_ENTITIES_PER_ROOM = 3
    MAX_ITEMS_PER_ROOM = 2

    COLORS = {
        'DARK_WALL': tcod.Color(30, 30, 30),
        'DARK_GROUND': tcod.Color(50, 50, 150),
        'LIGHT_WALL': tcod.Color(130, 110, 50),
        'LIGHT_GROUND': tcod.Color(200, 180, 50),
    }

    FONT_LOCATION = os.path.join("resources", os.path.join("arial10x10.png"))
    BACKGROUND_IMAGE_LOCATION = os.path.join("resources", os.path.join("menu_background.png"))
    X_INDEX = 0
    Y_INDEX = 1

    constants = {
        'WINDOW_TITLE': WINDOW_TITLE,
        'SCREEN_WIDTH': SCREEN_WIDTH,
        'SCREEN_HEIGHT': SCREEN_HEIGHT,
        'HP_MESSAGE_PANEL_WIDTH': HP_MESSAGE_PANEL_WIDTH,
        'HP_MESSAGE_PANEL_HEIGHT': HP_MESSAGE_PANEL_HEIGHT,
        'HP_MESSAGE_PANEL_Y_LOC': HP_MESSAGE_PANEL_Y_LOC,
        'MESSAGE_X_LOC': MESSAGE_X_LOC,
        'MESSAGE_WIDTH': MESSAGE_WIDTH,
        'MESSAGE_HEIGHT': MESSAGE_HEIGHT,
        'FOV_ALG': FOV_ALG,
        'FOV_LIGHT_WALLS': FOV_LIGHT_WALLS,
        'FOV_RADIUS': FOV_RADIUS,
        'MAP_WIDTH': MAP_WIDTH,
        'MAP_HEIGHT': MAP_HEIGHT,
        'ROOM_MAX_SIZE': ROOM_MAX_SIZE,
        'ROOM_MIN_SIZE': ROOM_MIN_SIZE,
        'MAX_ROOMS': MAX_ROOMS,
        'MAX_ENTITIES_PER_ROOM': MAX_ENTITIES_PER_ROOM,
        'MAX_ITEMS_PER_ROOM': MAX_ITEMS_PER_ROOM,
        'COLORS': COLORS,
        'FONT_LOCATION': FONT_LOCATION,
        'BACKGROUND_IMAGE_LOCATION': BACKGROUND_IMAGE_LOCATION,
        'X_INDEX': X_INDEX,
        'Y_INDEX': Y_INDEX
    }

    return constants


def get_game_variables(constants):
    combat_component = Combat(vigor=100, agility=1, brawn=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, brawn_bonus=2)
    dagger = Entity(0, 0, '-', tcod.sky, 'Dagger', equippable=equippable_component)
    player = Entity(int(constants['SCREEN_WIDTH'] / 2), int(constants['SCREEN_HEIGHT'] / 2), '@', tcod.white, "Player",
                    blocks=True, combat=combat_component, inventory=inventory_component, render_order=RenderOrder.ACTOR, level=level_component, equipment=equipment_component)
    entities = [player]
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(constants['MAP_WIDTH'], constants['MAP_HEIGHT'])
    game_map.make_map(constants['MAX_ROOMS'], constants['ROOM_MIN_SIZE'], constants['ROOM_MAX_SIZE'], constants['MAP_WIDTH'], constants['MAP_HEIGHT'], player, entities)

    message_log = MessageLog(constants['MESSAGE_X_LOC'], constants['MESSAGE_WIDTH'], constants['MESSAGE_HEIGHT'])
    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
