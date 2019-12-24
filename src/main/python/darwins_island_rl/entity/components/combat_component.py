import logging
logger = logging.getLogger(__name__)


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

        if damage > 0:
            target.combat.take_damage(damage)
            results.append({'message': "{0} attacks {1}, dealing {2} damage!".format(self.owner.name.capitalize(), target.name, str(damage))})
            results.extend(target.combat.take_damage(damage))
        else:
            results.append({'message': "{0} attacks {1}, but {1} is unaffected!".format(self.owner.name.capitalize(), target.name)})

        return results
