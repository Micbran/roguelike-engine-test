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
        return {'move': (0, 0)}
    elif game_event.sym == tcod.event.K_g:
        return {'pickup': True}
    elif game_event.sym == tcod.event.K_i:
        return {'show_inventory': True}
    elif game_event.sym == tcod.event.K_d:
        return {'drop_inventory': True}

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
    if game_event.sym == tcod.event.K_KP_ENTER or game_event.sym == tcod.event.K_RETURN or tcod.event.K_RETURN2:
        return {'submit': True}

    return {}
