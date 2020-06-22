import logging
logger = logging.getLogger(__name__)

from game_messages import Message


class Combat:
    def __init__(self, vigor, agility, brawn, xp=0):
        self.base_max_hp = vigor
        self.hp = vigor
        self.base_agility = agility
        self.base_brawn = brawn
        self.xp = xp
        self.owner = None

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def brawn(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.brawn_bonus
        else:
            bonus = 0

        return self.base_brawn + bonus

    @property
    def agility(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.agility_bonus
        else:
            bonus = 0

        return self.base_agility + bonus

    def take_damage(self, damage):
        results = []

        self.hp -= damage

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def attack(self, target):
        results = []

        damage = self.brawn - target.combat.agility

        if damage > 0:
            results.append({'message': Message("{0} attacks {1}, dealing {2} damage!".format(self.owner.name.capitalize(), target.name, str(damage)))})
            results.extend(target.combat.take_damage(damage))
        else:
            results.append({'message': Message("{0} attacks {1}, but {1} is unaffected!".format(self.owner.name.capitalize(), target.name))})

        return results

    def heal(self, amount):
        save_hp = self.hp
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
        return self.hp - save_hp
