import tcod
import tcod.event
import os
import logging

from src.main.python.darwins_island_rl.event_handler import handle_event
from src.main.python.darwins_island_rl.entity import Entity
from src.main.python.darwins_island_rl.render_help import render_all, clear_all
from src.main.python.darwins_island_rl.map_objects.game_map import GameMap

logging.basicConfig(filename='game_log.log', filemode='w', level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

COLORS = {
    'DARK_WALL': tcod.Color(30, 30, 30),
    'DARK_GROUND': tcod.Color(50, 50, 150),
}

FONT_LOCATION = os.path.join("resources", os.path.join("arial10x10.png"))

X_INDEX = 0
Y_INDEX = 1


def main():
    logger.info("Game start")
    tcod.console_set_custom_font(FONT_LOCATION, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    root_console = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, "Darwin's Island RL",
                                          fullscreen=False, renderer=tcod.RENDERER_SDL2, order='F', vsync=True)
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    player = Entity(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), '@', tcod.white)
    test_npc = Entity(5, 5, '@', tcod.yellow)
    entities = [player, test_npc]

    tcod.console_put_char(root_console, player.x, player.y, '@', tcod.BKGND_NONE)
    tcod.console_put_char(root_console, test_npc.x, test_npc.y, '@', tcod.BKGND_NONE)

    root_console.blit(root_console, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    while True:
        render_all(root_console, entities, game_map, SCREEN_WIDTH, SCREEN_HEIGHT, COLORS)
        tcod.console_flush()
        clear_all(root_console, entities)

        for event in tcod.event.wait():
            action = handle_event(event)
            if action.get('move'):
                move = action.get('move')
                if not game_map.is_blocked(player.x + move[X_INDEX], player.y + move[Y_INDEX]):
                    player.move(move[X_INDEX], move[Y_INDEX])

            if action.get('exit'):
                return True


if __name__ == '__main__':
    main()
