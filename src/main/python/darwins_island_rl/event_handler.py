import tcod
from tcod import event


def handle_event(game_event):
    if game_event.type == "QUIT":
        raise SystemExit()
    elif game_event.type == "KEYDOWN":
        return handle_keypress(game_event)

    return {}


def handle_keypress(game_event):
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

    if game_event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    return {}
