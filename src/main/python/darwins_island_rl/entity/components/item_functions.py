import tcod

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
