import tcod


def render_all(console, entities_list, game_map, fov_map, fov_recompute, screen_width, screen_height, color_dict):
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
    for entity in entities_list:
        draw_entity(console, entity, fov_map)

        console.blit(console, 0, screen_width, screen_height, 0, 0, 0)


def draw_entity(console, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        console.default_fg = entity.color
        tcod.console_put_char(console, entity.x, entity.y, entity.char)


def clear_all(console, entities_list):
    for entity in entities_list:
        clear_entity(console, entity)


def clear_entity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ')
