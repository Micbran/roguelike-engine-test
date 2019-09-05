import curses
from curses import wrapper
import logging
import os

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
RESOURCE_FOLDER_LOCATION = os.path.join('resources')
logging.basicConfig(level=logging.DEBUG,
                    filename='game_log.log',
                    filemode='w',
                    format='%(name)s:%(levelname)s: %(message)s')


def main(main_screen):
    logging.info("-----------Game start-----------")
    main_screen.clear()
    curses.noecho()
    curses.cbreak()
    main_screen.keypad(True)
    quit_console(main_screen)
    logging.info(main_screen)
    logging.info("Game End")


def quit_console(console_window):
    curses.nocbreak()
    console_window.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    wrapper(main)
