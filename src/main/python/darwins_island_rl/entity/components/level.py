
class Level:
    def __init__(self, level=1, xp=0, level_up_base=200, level_up_factor=150):
        self.level = level
        self.xp = xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    @property
    def xp_to_next_level(self):
        return self.level_up_base + self.level * self.level_up_factor

    def add_xp(self, xp):
        self.xp += xp

        if self.xp > self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1

            return True

        else:
            return False
