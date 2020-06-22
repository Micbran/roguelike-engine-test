

class Equippable:
    def __init__(self, slot, brawn_bonus=0, agility_bonus=0, hp_bonus=0):
        self.slot = slot
        self.brawn_bonus = brawn_bonus
        self.agility_bonus = agility_bonus
        self.hp_bonus= hp_bonus
