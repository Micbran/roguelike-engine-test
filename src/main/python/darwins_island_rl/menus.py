import tcod
import tcod.console


def menu(console, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

    # calculate header height
    header_height = tcod.console_get_height_rect(console, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create a new console
    window = tcod.console_new(width, height)

    # print header with wrap
    window.default_fg = tcod.white
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit contents
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, console, x, y, 1.0, 0.7)


def inventory_menu(console, header, inventory, inventory_width, screen_width, screen_height):
    # show a menu with each item in inventory as an option
    if len(inventory.items) == 0:
        options = ["Inventory is empty."]
    else:
        options = [item.name for item in inventory.items]

    return menu(console, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    tcod.image_blit_2x(background_image, con, 0, 0)

    tcod.console_set_default_foreground(con, tcod.light_yellow)
    tcod.console_print_ex(con, int(screen_width / 2), int(screen_height / 2) - 4, tcod.BKGND_NONE, tcod.CENTER,
                          'RL Engine Test')
    tcod.console_print_ex(con, int(screen_width / 2), int(screen_height - 2), tcod.BKGND_NONE, tcod.CENTER,
                          'By Brandon Komplin')

    menu(con, '', ['New Game', 'Continue', 'Quit'], 24, screen_width, screen_height)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)

