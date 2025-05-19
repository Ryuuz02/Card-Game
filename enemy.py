from random import random
from event import enemy_action

class enemy:
    """Represents the enemy."""
    def __init__(self, name, game, health=30, damage=10, action_weights=None):
        if action_weights is None:
            action_weights = {"attack": 0.5, "defend": 0.3, "do_nothing": 0.2}
        self.name = name
        self.game = game
        self.health = health
        self.damage = damage
        self.armor = 0
        self.action_weights = action_weights

    def attack(self, player):
        attack = enemy_action(self, player, damage=self.damage)
        attack.add_to_game(self.game)

    def defend(self, player):
        defend = enemy_action(self, self, armor=1)
        defend.add_to_game(self.game)

    def do_nothing(self, player):
        nothing = enemy_action(self, self)
        nothing.add_to_game(self.game)

    def take_turn(self, player):
        """Enemy chooses an action based on weights."""
        action = random()
        cumulative_weight = 0
        for action_name, weight in self.action_weights.items():
            cumulative_weight += weight
            if action < cumulative_weight:
                getattr(self, action_name)(player)
                break

    def __str__(self):
        return self.name

    def __eq__(self, value):
        return isinstance(value, enemy) and self.name == value.name