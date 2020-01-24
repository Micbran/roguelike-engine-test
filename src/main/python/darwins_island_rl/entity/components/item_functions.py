import tcod


from entity.components.ai import ConfusedMonster
from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.combat.hp == entity.combat.max_hp:
        results.append({'consumed': False, 'message': Message("You are already at full health.", tcod.yellow)})
    else:
        heal_res = entity.combat.heal(amount)
        results.append({'consumed': True, 'message': Message("Your wounds close up, healing you for {0} hit points!".format(heal_res), tcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    max_range = kwargs.get("max_range")

    results = []

    target = None
    closest_distance = max_range + 1

    for entity in entities:
        if entity.combat and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message("A lightning bolt strikes {0} with a loud thunderclap! The {0} takes {1} points of damage!".format(target.name, damage))})
        results.extend(target.combat.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message("There is no target within range ({0}).".format(max_range), tcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message("You cannot target a file outside your field of view.", tcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('A fireball explodes!')})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message("{0} is burned and takes {1} damage!".format(entity.name, damage), tcod.orange)})
            results.extend(entity.combat.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get("entities")
    fov_map = kwargs.get("fov_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message("You cannot target a file outside your field of view.", tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message("{0} is confused!".format(entity.name), tcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message("There is no target at that location.", tcod.yellow)})

    return results
