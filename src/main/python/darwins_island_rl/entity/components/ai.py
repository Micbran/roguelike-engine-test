import tcod


class BasicMonster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.combat.hp > 0:
                attack_results = monster.combat.attack(target)
                results.extend(attack_results)

        return results
