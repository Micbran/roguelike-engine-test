import logging

import tcod
import tcod.event
import tcod.console

from loader_functions.init_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import save_game, load_game
from event_handler import handle_event, handle_event_main_menu
from entity.entity import get_blocking_entities_at_location
from render_help import render_all, clear_all
from fov_help import init_fov, recompute_fov
from game_state import GameStates
from death_functions import kill_player, kill_monster
from game_messages import Message
from menus import main_menu, message_box

# Logger Set-up
logging.basicConfig(filename='game_log.log', filemode='w', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def main():
    constants = get_constants()
    # Set-up
    logger.info("Game start")
    tcod.console_set_custom_font(constants['FONT_LOCATION'], tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    root_console = tcod.console_init_root(constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], constants['WINDOW_TITLE'],
                                          fullscreen=False, renderer=tcod.RENDERER_SDL2, order='F', vsync=True)
    hp_message_panel = tcod.console.Console(constants['SCREEN_WIDTH'], constants['HP_MESSAGE_PANEL_HEIGHT'], order="F")

    # Player/Entity Predefs
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = tcod.image_load(constants['BACKGROUND_IMAGE_LOCATION'])

    key = tcod.Key()
    mouse = tcod.Mouse()

    while True:
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        action = handle_event_main_menu(key)
        if show_main_menu:
            main_menu(root_console, main_menu_background_image, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])

            if show_load_error_message:
                message_box(root_console, "No save game to load.", 50, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'])

            tcod.console_flush()

            new_game = action.get('new_game')
            load_saved_game = action.get('load_saved_game')
            exit_game = action.get('exit')
            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break
        else:
            root_console.clear(fg=(255, 255, 63))
            play_game(player, entities, game_map, message_log, game_state, root_console, hp_message_panel, constants)
            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, root_console, hp_message_panel, constants):
    fov_recompute = True
    fov_map = init_fov(game_map)

    previous_game_state = game_state

    targeting_item_entity = None
    targeted_entity = None
    target_save_color = None
    prelim_list = []

    root_console.blit(root_console, 0, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], 0, 0, 0)

    # Game Loop
    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['FOV_RADIUS'], constants['FOV_LIGHT_WALLS'],
                          constants['FOV_ALG'])
        render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'], constants['HP_MESSAGE_PANEL_WIDTH'],
                   constants['HP_MESSAGE_PANEL_HEIGHT'], constants['HP_MESSAGE_PANEL_Y_LOC'], constants['COLORS'],
                   game_state)
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
                        player.move(move[constants['X_INDEX']], move[constants['Y_INDEX']])
                        fov_recompute = True
                    game_state = GameStates.ENEMY_TURN

            if action.get('take_stairs') and GameStates.PLAYERS_TURN:
                for entity in entities:
                    if entity.stairs and entity.x == player.x and entity.y == player.y:
                        entities = game_map.next_floor(player, message_log, constants)
                        fov_map = init_fov(game_map)
                        fov_recompute = True
                        root_console.clear(fg=(255, 255, 63))

                        break
                else:
                    message_log.add_message(Message('There are no stairs here.', tcod.yellow))

            if action.get('wait') and game_state is GameStates.PLAYERS_TURN:
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
                    player_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_results.extend(player.inventory.drop_item(item))

            if game_state == GameStates.TARGETING:
                cycle = action.get("cycle")
                submit = action.get("submit")
                max_dist = targeting_item_entity.item.max_range if hasattr(targeting_item_entity.item,
                                                                           'max_range') else 5
                if not prelim_list:  # only "make" prelim list if it's empty
                    for entity in entities:  # turn this into a function
                        if tcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.combat and entity is not player:
                            prelim_list.append(entity)
                    for index in range(len(prelim_list)):  # selection sort using player.distance_to(prelim_list[i])
                        closest_entity = index
                        for sub_index in range(index + 1, len(prelim_list)):
                            if player.distance_to(prelim_list[closest_entity]) > player.distance_to(
                                    prelim_list[sub_index]):
                                closest_entity = sub_index
                        prelim_list[index], prelim_list[closest_entity] = prelim_list[closest_entity], prelim_list[
                            index]
                    for index in range(len(prelim_list)):
                        if player.distance_to(prelim_list[index]) > max_dist:
                            prelim_list.pop(index)
                if not prelim_list:  # if there's nothing in range
                    player_results.append({"targeting_canceled": True})
                    targeted_entity = None
                    target_save_color = None
                    prelim_list.clear()
                    player_results.append({'message': Message(
                        "There is no target within targetable range ({0}).".format(max_dist), tcod.red)})
                if cycle:
                    if target_save_color and targeted_entity:
                        targeted_entity.color = target_save_color
                    select_entity = prelim_list.pop(0)
                    prelim_list.append(select_entity)

                    if select_entity:  # color it white
                        target_save_color = select_entity.color
                        targeted_entity = select_entity
                        targeted_entity.color = tcod.white

                if submit:
                    if target_save_color and targeted_entity:
                        targeted_entity.color = target_save_color
                    if targeted_entity:
                        target_x = targeted_entity.x
                        target_y = targeted_entity.y

                        item_use_results = player.inventory.use(targeting_item_entity, entities=entities,
                                                                fov_map=fov_map, target_x=target_x, target_y=target_y)
                        player_results.extend(item_use_results)
                        prelim_list.clear()
                        targeted_entity = None
                        target_save_color = None
                    else:
                        player_results.append({"targeting_canceled": True})
                        targeted_entity = None
                        target_save_color = None
                        prelim_list.clear()

            if action.get('level_up'):
                level_up_choice = action.get('level_up')
                if level_up_choice == 'hp':
                    player.combat.base_max_hp += 20
                    player.combat.hp += 20
                elif level_up_choice == 'str':
                    player.combat.base_brawn += 1
                elif level_up_choice == 'def':
                    player.combat.base_agility += 1

                game_state = previous_game_state

            if action.get('show_character_sheet'):
                previous_game_state = game_state
                game_state = GameStates.CHARACTER_SCREEN

            if action.get('exit'):
                if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                    game_state = previous_game_state
                elif game_state == GameStates.TARGETING:
                    player_results.append({"targeting_canceled": True})
                    targeted_entity = None
                    target_save_color = None
                    prelim_list.clear()
                else:
                    save_game(player, entities, game_map, message_log, game_state)
                    return True
                root_console.clear(fg=(0, 127, 0))
                render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, True,
                           message_log, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'],
                           constants['HP_MESSAGE_PANEL_WIDTH'],
                           constants['HP_MESSAGE_PANEL_HEIGHT'], constants['HP_MESSAGE_PANEL_Y_LOC'],
                           constants['COLORS'], game_state)

            for result in player_results:
                message = result.get('message')
                dead_entity = result.get('dead')
                item_added = result.get('item_added')
                item_consumed = result.get('consumed')
                item_dropped = result.get('item_dropped')
                equip = result.get('equip')
                targeting = result.get('targeting')
                targeting_canceled = result.get('targeting_canceled')
                xp = result.get('xp')

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
                if targeting:
                    previous_game_state = GameStates.PLAYERS_TURN
                    game_state = GameStates.TARGETING
                    targeting_item_entity = targeting

                    logger.info(targeting_item_entity.item.targeting_message.text)
                    message_log.add_message(targeting_item_entity.item.targeting_message)
                if targeting_canceled:
                    game_state = previous_game_state

                    logger.info("Targeting canceled.")
                    message_log.add_message(Message("Targeting canceled", tcod.yellow))
                if item_dropped:
                    entities.append(item_dropped)
                    game_state = GameStates.ENEMY_TURN
                if equip:
                    equip_results = player.equipment.toggle_equip(equip)

                    for equip_result in equip_results:
                        equipped = equip_result.get('equipped')
                        dequipped = equip_result.get('dequipped')

                        if equipped:
                            message_log.add_message(Message('You equipped the {0}.'.format(equipped.name)))
                        if dequipped:
                            message_log.add_message(Message('You dequipped the {0}.'.format(dequipped.name)))

                    game_state = GameStates.ENEMY_TURN
                if xp:
                    leveled_up = player.level.add_xp(xp)
                    message_log.add_message(Message('You gain {0} experience points!'.format(xp)))

                    if leveled_up:
                        message_log.add_message(Message('You level up! You have reached level {0}.'.format(player.level.level), tcod.yellow))
                        previous_game_state = game_state
                        game_state = GameStates.LEVEL_UP

            root_console.clear(fg=(0, 127, 0))
            render_all(root_console, hp_message_panel, entities, player, game_map, fov_map, True,
                       message_log, constants['SCREEN_WIDTH'], constants['SCREEN_HEIGHT'],
                       constants['HP_MESSAGE_PANEL_WIDTH'],
                       constants['HP_MESSAGE_PANEL_HEIGHT'], constants['HP_MESSAGE_PANEL_Y_LOC'], constants['COLORS'],
                       game_state)

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
