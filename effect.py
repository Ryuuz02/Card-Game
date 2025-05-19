class effect:
    """Represents an effect applied by a card."""
    def __init__(self, user, target, effect_type, value, card_target=None):
        self.user = user
        self.target = target
        self.effect_type = effect_type
        self.value = value
        self.card_target = card_target

    def apply(self):
        """Applies the effect to the target."""
        print(self.target)
        if self.effect_type == "damage":
            damage = max(0, self.value - self.target.armor)
            self.target.health -= damage
        elif self.effect_type == "armor":
            self.target.armor += self.value
        elif self.effect_type == "heal":
            self.target.health += self.value
        elif self.effect_type == "enhance":
            self.card_target.add_effect(effect(self.user, self.target, "damage", self.value))

    def __str__(self):
        return f"{self.effect_type} {self.value} to {self.target.name}"