import tcod

from game_state import GameStates
from render_help import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return "You died!", GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = 'The {0} dies!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.combat = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
