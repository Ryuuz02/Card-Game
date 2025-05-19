from event import player_action

class card:
    """Represents a card with effects."""
    def __init__(self, id, name, cost=0, effects=None):
        self.id = id
        self.name = name
        self.cost = cost
        self.effects = effects if effects is not None else []

    def __eq__(self, value):
        return isinstance(value, card) and self.id == value.id

    def __str__(self):
        return self.name

    def add_effect(self, effect):
        self.effects.append(effect)

    def activate(self):
        """Activates all effects of the card."""
        for effect in self.effects:
            effect.apply()

    def play(self, game):
        """Plays the card as a player action event."""
        played_card = player_action(self)
        print(played_card.add_to_game(game))
        print(game.events)