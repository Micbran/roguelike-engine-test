import tcod


def init_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].sight_block,
                                    not game_map.tiles[x][y].move_block)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls, alg):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, alg)
