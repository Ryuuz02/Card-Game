from random import shuffle, random
from copy import deepcopy

class card:
    def __init__(self, id, name, cost=0, effects=None):
        self.id = id
        self.name = name
        self.cost = cost
        self.effects = effects if effects is not None else []

    def __eq__(self, value):
        if isinstance(value, card):
            return self.id == value.id
        return False

    def __str__(self):
        return self.name
    
    def add_effect(self, effect):
        self.effects.append(effect)
    
    def activate(self):
        for effect in self.effects:
            effect.apply()
        
    def play(self, game):
        played_card = player_action(self)
        print(played_card.add_to_game(game))
        print(game.events)

class effect:
    def __init__(self, user, target, effect_type, value, card_target=None, ):
        self.user = user
        self.target = target
        self.effect_type = effect_type
        self.value = value
        self.card_target = card_target
    
    def apply(self):
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


class player:
    def __init__(self, name, game, health=100, armor=0, max_hand_size=5, max_energy=3):
        self.name = name
        self.game = game
        self.health = health
        self.armor = armor
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.max_hand_size = max_hand_size
        self.max_energy = max_energy
        self.energy = max_energy

    def draw_card(self):
        if not self.deck:
            self.shuffle_discard_into_deck()
        card_drawn = self.deck.pop(0)
        self.hand.append(card_drawn)
        print(f"{self.name} drew a card: {card_drawn}")

    def shuffle_discard_into_deck(self):
        if self.discard_pile:
            shuffle(self.discard_pile)
            self.deck.extend(self.discard_pile)
            self.discard_pile.clear()
            print(f"{self.name} shuffled discard pile into deck.")
        else:
            print(f"{self.name} has no cards to shuffle into the deck.")

    def add_card_to_deck(self, card):
        self.deck.append(card)
        print(f"{self.name} added card to deck: {card}")
    
    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.energy -= card.cost
            card.play(self.game)
            self.discard_pile.append(card)
            print(f"{self.name} played {card}.")
        else:
            print(f"{self.name} does not have {card} in hand.")
    
    def start_turn(self):
        self.energy = self.max_energy
        print(f"{self.name} started their turn with {self.energy} energy.")
        self.draw_to_max_hand()
        self.take_turn()

    def take_turn(self):
        while True:
            print("Current Hand:")
            for i in range(len(self.hand)):
                card = self.hand[i]
                print(str(i + 1) + ": " + str(card))
            choice = -2
            while choice not in range(-1, len(self.hand) + 1):
                choice = int(input("Type the number of the card you want to play, or 0 to end the turn ")) - 1
            if choice == -1:
                break
            chosen_card = self.hand[choice]
            if chosen_card.cost > self.energy:
                print(f"{self.name} does not have enough energy to play this card.")
                continue
            else:
                self.play_card(chosen_card)
                print(f"{self.name} played {chosen_card}.")
        self.end_turn()

    def end_turn(self):
        self.discard_hand()
    
    def discard_hand(self):
        for card in self.hand:
            self.discard_pile.append(card)
        self.hand.clear()
        print(f"{self.name} discarded their hand.")
    
    def draw_to_max_hand(self):
        for _ in range(self.max_hand_size):
            self.draw_card()
        print(f"{self.name} drew cards to max hand size. Hand size is now {len(self.hand)}.")
    
    def shuffle_deck(self):
        shuffle(self.deck)
        print(f"{self.name} shuffled their deck.")
    
    def __str__(self):
        return self.name
    
    def __eq__(self, value):
        if isinstance(value, player):
            return self.name == value.name
        return False


class game:
    def __init__(self, player=None, enemy=None, events=[]):
        self.player = player
        self.enemy = enemy
        self.events = events
        self.event_idx = 0
    
    def resolve_all_events(self):
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
        for event in self.events[self.event_idx:]:
            event.resolve()
        self.event_idx = len(self.events)
    
    def play_round(self):
        self.player.start_turn()
        self.resolve_all_events()
        if self.check_alive():
            self.enemy.take_turn(self.player)
            self.resolve_all_events()
            if self.check_alive():
                print(f"Round played. {self.player.name} has {self.player.health} health left.")
                print(f"{self.enemy.name} has {self.enemy.health} health left.")
            else:
                pass
        else:
            pass
    
    def update_targets(self):
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
        self.player_copy = deepcopy(self.player)
        self.enemy_copy = deepcopy(self.enemy)
        while self.check_alive():
            self.play_round()
        print("Game Over")

class event:
    def __init__(self, type):
        self.type = type

    def add_to_game(self, game):
        game.events.append(self)
        return True

class player_action(event):
    def __init__(self, card):
        super().__init__("Player_Action")
        self.card = card
    
    def resolve(self):
        self.card.activate()
        return True

class enemy_action(event):
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

class enemy:
    def __init__(self, name, game, health=30, damage=10, action_weights={"attack": 0.5, "defend": 0.3, "do_nothing": 0.2}, ):
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
        if isinstance(value, enemy):
            return self.name == value.name
        return False

if __name__ == "__main__":
    # Create player and enemy
    game_instance = game()
    player1 = player("Player 1", game_instance)
    game_instance.add_player(player1)
    enemy1 = enemy("Enemy 1", game_instance)
    game_instance.add_enemy(enemy1)
    

    # Create cards
    card1 = card(1, "Fireball", 1)
    fireball1 = effect(player1, enemy1, "damage", 5)
    card1.add_effect(fireball1)
    card2 = card(2, "Shield", 1)
    shield1 = effect(player1, player1, "armor", 2)
    card2.add_effect(shield1)
    card3 = card(3, "Heal", 2)
    heal1 = effect(player1, player1, "heal", 7)
    card3.add_effect(heal1)
    card4 = card(4, "Enhance", 1)
    enhance1 = effect(player1, enemy1, "enhance", 3, card_target=card1)
    card4.add_effect(enhance1)

    # Add cards to player's deck
    for _ in range(7):
        player1.add_card_to_deck(card1)
    for _ in range(3):
        player1.add_card_to_deck(card2)
    for _ in range(2):
        player1.add_card_to_deck(card3)
    for _ in range(1):
        player1.add_card_to_deck(card4)

    player1.shuffle_deck()
    game_instance.play_fight()