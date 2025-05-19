class event:
    """Base class for game events."""
    def __init__(self, type):
        self.type = type

    def add_to_game(self, game):
        game.events.append(self)
        game.event_seeds.append(game.game_seed + game.event_idx + hash(self.type))
        return True

class player_action(event):
    """Event for player playing a card."""
    def __init__(self, card):
        super().__init__("Player_Action")
        self.card = card

    def resolve(self):
        self.card.activate()
        return True

class enemy_action(event):
    """Event for enemy action."""
    def __init__(self, user, target, damage=0, armor=0):
        super().__init__("Enemy_Action")
        self.user = user
        self.target = target
        self.damage = damage
        self.armor = armor

    def resolve(self):
        if self.damage > 0:
            damage = max(0, self.damage - self.target.armor)
            self.target.health -= damage
            print(f"{self.user.name} dealt {self.damage} damage to {self.target.name}.")
        if self.armor > 0:
            self.target.armor += self.armor
            print(f"{self.user.name} gained {self.armor} armor.")
        return True
