import logging
import os

import tcod
import tcod.event
import tcod.console

from event_handler import handle_event
from entity.entity import Entity, get_blocking_entities_at_location
from entity.components.combat_component import Combat
from entity.components.inventory import Inventory
from entity.components.ai import BasicMonster
from render_help import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_help import init_fov, recompute_fov
from game_state import GameStates
from death_functions import kill_player, kill_monster
from game_messages import MessageLog, Message

# Logger Set-up
logging.basicConfig(filename='game_log.log', filemode='w', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# "Constants"
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

X_INDEX = 0
Y_INDEX = 1


def main():
    # Set-up
    logger.info("Game start")
    tcod.console_set_custom_font(FONT_LOCATION, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    root_console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "Darwin's Island RL",
                                          fullscreen=False, renderer=tcod.RENDERER_SDL2, order='F', vsync=True)
    hp_message_panel = tcod.console.Console(SCREEN_WIDTH, HP_MESSAGE_PANEL_HEIGHT, order="F")
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    message_log = MessageLog(MESSAGE_X_LOC, MESSAGE_WIDTH, MESSAGE_HEIGHT)

    # Player/Entity Predefs
    combat_component = Combat(vigor=30, agility=5, brawn=5)
    inventory_component = Inventory(26)
    player = Entity(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), '@', tcod.white, "Player", blocks=True, combat=combat_component, inventory=inventory_component, render_order=RenderOrder.ACTOR)
    entities = [player]

    game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player, entities, MAX_ENTITIES_PER_ROOM, MAX_ITEMS_PER_ROOM)
    fov_recompute = True
    fov_map = init_fov(game_map)

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    root_console.blit(root_console, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    # Game Loop
    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALG)
        render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, fov_recompute, message_log, SCREEN_WIDTH, SCREEN_HEIGHT, HP_MESSAGE_PANEL_WIDTH, HP_MESSAGE_PANEL_HEIGHT, HP_MESSAGE_PANEL_Y_LOC, COLORS, game_state)
        fov_recompute = False
        tcod.console_flush()
        clear_all(root_console, entities)

        # Event Handling
        for event in tcod.event.wait():
            player_results = []
            action = handle_event(event, game_state)
            if action.get('move') and game_state is GameStates.PLAYERS_TURN:
                move = action.get('move')
                dx, dy = move
                dest_x = player.x + dx
                dest_y = player.y + dy
                if not game_map.is_blocked(dest_x, dest_y):
                    target = get_blocking_entities_at_location(entities, dest_x, dest_y)

                    if target:
                        attack_results = player.combat.attack(target)
                        player_results.extend(attack_results)
                    else:
                        player.move(move[X_INDEX], move[Y_INDEX])
                        fov_recompute = True
                    game_state = GameStates.ENEMY_TURN

            if action.get('pickup') and game_state is GameStates.PLAYERS_TURN:
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity)
                        player_results.extend(pickup_results)

                        break
                else:
                    message_log.add_message(Message("There is nothing to pick up here.", tcod.yellow))
            if action.get('show_inventory') and game_state is GameStates.PLAYERS_TURN:
                previous_game_state = game_state
                game_state = GameStates.SHOW_INVENTORY

            if action.get('drop_inventory') and game_state is GameStates.PLAYERS_TURN:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY

            if action.get('inventory_index') is not None and previous_game_state != GameStates.PLAYER_DEAD and action.get('inventory_index') < len(player.inventory.items):
                item = player.inventory.items[action.get('inventory_index')]
                if game_state == GameStates.SHOW_INVENTORY:
                    player_results.extend(player.inventory.use(item))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_results.extend(player.inventory.drop_item(item))
            if action.get('exit'):
                if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                    game_state = previous_game_state
                    root_console.clear()
                    render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, True,
                               message_log, SCREEN_WIDTH, SCREEN_HEIGHT, HP_MESSAGE_PANEL_WIDTH,
                               HP_MESSAGE_PANEL_HEIGHT, HP_MESSAGE_PANEL_Y_LOC, COLORS, game_state)
                else:
                    return True

            for result in player_results:
                message = result.get('message')
                dead_entity = result.get('dead')
                item_added = result.get('item_added')
                item_consumed = result.get('consumed')
                item_dropped = result.get('item_dropped')

                if message:
                    logger.info(message.text)
                    message_log.add_message(message)
                if dead_entity:
                    if dead_entity == player:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    logger.info(message.text)
                    message_log.add_message(message)
                if item_added:
                    entities.remove(item_added)
                    game_state = GameStates.ENEMY_TURN
                if item_consumed:
                    game_state = GameStates.ENEMY_TURN
                if item_dropped:
                    entities.append(item_dropped)
                    game_state = GameStates.ENEMY_TURN

            root_console.clear(fg=(0, 127, 0))
            render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, True,
                       message_log, SCREEN_WIDTH, SCREEN_HEIGHT, HP_MESSAGE_PANEL_WIDTH,
                       HP_MESSAGE_PANEL_HEIGHT, HP_MESSAGE_PANEL_Y_LOC, COLORS, game_state)

            if game_state is GameStates.ENEMY_TURN:
                for entity in entities:
                    if entity.ai:
                        enemy_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                        for result in enemy_results:
                            message = result.get('message')
                            dead_entity = result.get('dead')

                            if message:
                                logger.info(message.text)
                                message_log.add_message(message)
                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                logger.info(message.text)
                                message_log.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break

                        if game_state == GameStates.PLAYER_DEAD:
                            break
                else:
                    game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
