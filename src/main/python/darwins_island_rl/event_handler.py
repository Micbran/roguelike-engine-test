import tcod
from tcod import event
from game_state import GameStates


def handle_event(game_event, game_state):
    if game_event.type == "QUIT":
        raise SystemExit()
    elif game_event.type == "KEYDOWN" and game_state == GameStates.PLAYERS_TURN:
        return handle_keypress_player_turn(game_event)
    elif game_event.type == "KEYDOWN" and game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_keypress_inventory(game_event)
    elif game_event.type == "KEYDOWN" and game_state == GameStates.PLAYER_DEAD:
        return handle_keypress_dead(game_event)
    elif game_event.type == "KEYDOWN" and game_state == GameStates.TARGETING:
        return handle_keypress_targeting(game_event)
    elif game_event.type == "KEYDOWN" and game_state == GameStates.LEVEL_UP:
        return handle_keypress_level_up_menu(game_event)
    elif game_event.type == "KEYDOWN" and game_state == GameStates.CHARACTER_SCREEN:
        return handle_keypress_character_sheet(game_event)

    return {}


def handle_keypress_player_turn(game_event):
    if game_event.sym == tcod.event.K_KP_6:
        return {'move': (1, 0)}
    elif game_event.sym == tcod.event.K_KP_4:
        return {'move': (-1, 0)}
    elif game_event.sym == tcod.event.K_KP_2:
        return {'move': (0, 1)}
    elif game_event.sym == tcod.event.K_KP_8:
        return {'move': (0, -1)}
    elif game_event.sym == tcod.event.K_KP_3:
        return {'move': (1, 1)}
    elif game_event.sym == tcod.event.K_KP_1:
        return {'move': (-1, 1)}
    elif game_event.sym == tcod.event.K_KP_7:
        return {'move': (-1, -1)}
    elif game_event.sym == tcod.event.K_KP_9:
        return {'move': (1, -1)}
    elif game_event.sym == tcod.event.K_KP_5:
        return {'wait': True}
    elif game_event.sym == tcod.event.K_g:
        return {'pickup': True}
    elif game_event.sym == tcod.event.K_i:
        return {'show_inventory': True}
    elif game_event.sym == tcod.event.K_d:
        return {'drop_inventory': True}
    elif game_event.sym == tcod.event.K_KP_GREATER or game_event.sym == tcod.event.K_KP_ENTER or game_event.sym == tcod.event.K_RETURN or game_event.sym == tcod.event.K_GREATER:
        return {'take_stairs': True}
    elif game_event.sym == tcod.event.K_c:
        return {'show_character_sheet': True}

    if game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    # TODO for look function, check code at end of part 7

    return {}


def handle_keypress_inventory(game_event):
    index = game_event.sym - 97  # a key is 97 (sym)

    if index >= 0:
        return {'inventory_index': index}
    elif game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    return {}


def handle_keypress_dead(game_event):
    if game_event.sym == tcod.event.K_i:
        return {'show_inventory': True}
    elif game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    return {}


def handle_keypress_targeting(game_event):
    if game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}
    if game_event.sym == tcod.event.K_KP_MULTIPLY:
        return {'cycle': True}
    if game_event.sym == tcod.event.K_KP_ENTER or game_event.sym == tcod.event.K_RETURN or game_event.sym == tcod.event.K_RETURN2:
        return {'submit': True}

    return {}


def handle_event_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_saved_game': True}
    elif key_char == 'c' or key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_keypress_level_up_menu(game_event):
    if game_event.sym == tcod.event.K_a:
        return {'level_up': 'hp'}
    elif game_event.sym == tcod.event.K_b:
        return {'level_up': 'str'}
    elif game_event.sym == tcod.event.K_c:
        return {'level_up': 'def'}

    return {}


def handle_keypress_character_sheet(game_event):
    if game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    return {}