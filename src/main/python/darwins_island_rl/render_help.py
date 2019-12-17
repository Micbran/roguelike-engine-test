import tcod


def render_all(console, entities_list, game_map, screen_width, screen_height, color_dict):
    for y in range(game_map.height):
        for x in range(game_map.width):
            if game_map.tiles[x][y].sight_block:
                tcod.console_set_char_background(console, x, y, color_dict.get('DARK_WALL'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(console, x, y, color_dict.get('DARK_GROUND'), tcod.BKGND_SET)

    for entity in entities_list:
        draw_entity(console, entity)

        console.blit(console, 0, screen_width, screen_height, 0, 0, 0)


def draw_entity(console, entity):
    console.default_fg = entity.color
    tcod.console_put_char(console, entity.x, entity.y, entity.char)


def clear_all(console, entities_list):
    for entity in entities_list:
        clear_entity(console, entity)


def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ')
