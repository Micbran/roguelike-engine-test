from equipment_slots import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, body=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.body = body

    @property
    def hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.hp_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.hp_bonus
        if self.body and self.body.equippable:
            bonus += self.body.equippable.hp_bonus

        return bonus

    @property
    def brawn_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.brawn_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.brawn_bonus
        if self.body and self.body.equippable:
            bonus += self.body.equippable.brawn_bonus

        return bonus

    @property
    def agility_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.agility_bonus
        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.agility_bonus
        if self.body and self.body.equippable:
            bonus += self.body.equippable.agility_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.BODY:
            if self.body == equippable_entity:
                self.body = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.body:
                    results.append({'dequipped': self.body})

                self.body = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
