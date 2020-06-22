from enum import Enum, auto

import tcod
from game_state import GameStates
from menus import inventory_menu, level_up_menu, character_sheet


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def render_bar(panel, x, y, total_width, name, value, max_value, bar_color, back_color):
    bar_width = int(float(value) / max_value * total_width)
    panel.default_bg = back_color
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    panel.default_bg = bar_color
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    panel.default_fg = tcod.white
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                          "{0}: {1}/{2}".format(name, value, max_value))


def render_all(console, panel, entities_list, player, game_map, fov_map, fov_recompute, message_log,
               screen_width, screen_height, bar_width, panel_height, panel_y, color_dict, game_state):
    # Render Walls/Ground
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                if visible:
                    if game_map.tiles[x][y].sight_block:
                        tcod.console_set_char_background(console, x, y, color_dict.get('LIGHT_WALL'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, color_dict.get('LIGHT_GROUND'), tcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if game_map.tiles[x][y].sight_block:
                        tcod.console_set_char_background(console, x, y, color_dict.get('DARK_WALL'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, color_dict.get('DARK_GROUND'), tcod.BKGND_SET)

    # Render Entities
    entities_list_render_order = sorted(entities_list, key=lambda val: val.render_order.value)
    for entity in entities_list_render_order:
        draw_entity(console, entity, fov_map, game_map)

    console.blit(console, 0, screen_width, screen_height, 0, 0, 0)
    panel.default_bg = tcod.black
    tcod.console_clear(panel)
    y = 1
    for message in message_log.messages:
        panel.default_fg = message.color
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, "HP", player.combat.hp, player.combat.max_hp, tcod.light_red, tcod.darker_red)
    tcod.console_print_ex(panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, 'Dungeon Level: {0}'.format(game_map.dungeon_level))

    # panel.blit(panel, 0, 0, screen_width, panel_height, 0, 0) # Work with blit somehow?
    tcod.console_blit(panel, 0, 0, screen_width, panel_height, console, 0, panel_y)

    inventory_title = "No handler."

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = "Press the key next to an item to use it or press Esc to exit.\n"
        if game_state == GameStates.DROP_INVENTORY:
            inventory_title = "Press the key next to an item to drop it or press Esc to exit.\n"

        inventory_menu(console, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(console, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_sheet(player, 30, 10, screen_width, screen_height)


def draw_entity(console, entity, fov_map, game_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        console.default_fg = entity.color
        tcod.console_put_char(console, entity.x, entity.y, entity.char)


def clear_all(console, entities_list):
    for entity in entities_list:
        clear_entity(console, entity)


def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ')
