import logging
logger = logging.getLogger(__name__)

from game_messages import Message


class Combat:
    def __init__(self, vigor, agility, brawn):
        self.max_hp = vigor  # TODO some forumula
        self.hp = vigor
        self.agility = agility
        self.brawn = brawn
        self.owner = None

    def take_damage(self, damage):
        results = []

        self.hp -= damage

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.brawn - target.combat.agility
        print(damage)

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
