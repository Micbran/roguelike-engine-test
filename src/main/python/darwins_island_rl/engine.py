import tcod
import tcod.event
import os
import logging

from src.main.python.darwins_island_rl.event_handler import handle_event

logging.basicConfig(filename='game_log.log', filemode='w', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FONT_LOCATION = os.path.join("resources", os.path.join("arial10x10.png"))

X_INDEX = 0
Y_INDEX = 1


def main():
    logger.info("Game start")
    tcod.console_set_custom_font(FONT_LOCATION, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    root_console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "Darwin's Island RL",
                                          fullscreen=False, renderer=tcod.RENDERER_SDL2, order='F', vsync=True)

    player_x = int(SCREEN_WIDTH/2)
    player_y = int(SCREEN_HEIGHT/2)
    tcod.console_put_char(root_console, player_x, player_y, '@', tcod.BKGND_NONE)
    root_console.blit(root_console, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    while True:
        tcod.console_flush()

        for event in tcod.event.wait():
            action = handle_event(event)
            if action.get('move'):
                move = action.get('move')
                player_x += move[X_INDEX]
                player_y += move[Y_INDEX]

            if action.get('exit'):
                return True


if __name__ == '__main__':
    main()
