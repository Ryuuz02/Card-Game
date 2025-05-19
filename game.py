from random import randint
from copy import deepcopy
from event import player_action, enemy_action

class game:
    """Main game logic and state."""
    def __init__(self, player=None, enemy=None, events=None):
        self.player = player
        self.enemy = enemy
        self.events = events if events is not None else []
        self.event_seeds = []
        self.event_idx = 0
        self.game_seed = randint(0, 1000000)

    def resolve_all_events(self):
        """Resolves all events in the game."""
        hand_copy = self.player.hand.copy()
        deck_copy = self.player.deck.copy()
        discard_copy = self.player.discard_pile.copy()
        self.player = deepcopy(self.player_copy)
        self.enemy = deepcopy(self.enemy_copy)
        self.player.game = self
        self.enemy.game = self
        self.player.deck = deck_copy
        self.player.hand = hand_copy
        self.player.discard_pile = discard_copy
        self.update_targets()
        print(self.events)
        for event in self.events:
            event.resolve()
        self.event_idx = len(self.events)

    def resolve_events_from_idx(self):
        """Resolves events from the current index onward."""
        for event in self.events[self.event_idx:]:
            event.resolve()
        self.event_idx = len(self.events)

    def play_round(self):
        """Plays a round: player turn, then enemy turn."""
        self.player.start_turn()
        self.resolve_all_events()
        if self.check_alive():
            self.enemy.take_turn(self.player)
            self.resolve_all_events()
            if self.check_alive():
                print(f"Round played. {self.player.name} has {self.player.health} health left.")
                print(f"{self.enemy.name} has {self.enemy.health} health left.")

    def update_targets(self):
        """Updates effect targets for all events."""
        for event in self.events:
            if isinstance(event, player_action):
                for effect in event.card.effects:
                    if effect.target == self.enemy:
                        effect.target = self.enemy
                    elif effect.target == self.player:
                        effect.target = self.player
            elif isinstance(event, enemy_action):
                event.target = self.player

    def check_alive(self):
        """Checks if both player and enemy are alive."""
        if self.player.health <= 0:
            print(f"{self.player.name} has been defeated.")
            return False
        elif self.enemy.health <= 0:
            print(f"{self.enemy.name} has been defeated.")
            return False
        return True

    def add_player(self, player):
        self.player = player
        print(f"Player {player.name} added to the game.")

    def add_enemy(self, enemy):
        self.enemy = enemy
        print(f"Enemy {enemy.name} added to the game.")

    def play_fight(self):
        """Starts the fight loop."""
        self.player_copy = deepcopy(self.player)
        self.enemy_copy = deepcopy(self.enemy)
        while self.check_alive():
            self.play_round()
        print("Game Over")