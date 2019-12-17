import tcod
from tcod import event as event

def handle_event(event):
    if event.type == "QUIT":
        raise SystemExit()
    elif event.type == "KEYDOWN":
        return handle_keypress(event)

    return {}


def handle_keypress(event):
    if event.sym == tcod.event.K_KP_6:
        return {'move': (1, 0)}
    elif event.sym == tcod.event.K_KP_4:
        return {'move': (-1, 0)}
    elif event.sym == tcod.event.K_KP_8:
        return {'move': (0, 1)}
    elif event.sym == tcod.event.K_KP_2:
        return {'move': (0, -1)}
    elif event.sym == tcod.event.K_KP_9:
        return {'move': (1, 1)}
    elif event.sym == tcod.event.K_KP_7:
        return {'move': (-1, 1)}
    elif event.sym == tcod.event.K_KP_1:
        return {'move': (-1, -1)}
    elif event.sym == tcod.event.K_KP_3:
        return {'move': (1, -1)}
    elif event.sym == tcod.event.K_KP_5:
        return {'move': (0, 0)}

    if event.sym == tcod.event.K_ESCAPE:
        return {'exit': True}

    return {}
