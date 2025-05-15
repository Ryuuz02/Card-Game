from random import shuffle, random

class card:
    def __init__(self, id, name, cost=0, damage=0, armor=0):
        self.id = id
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __eq__(self, value):
        if isinstance(value, card):
            return self.id == value.id
        return False

    def __str__(self):
        return self.name

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
            self.discard_pile = shuffle(self.discard_pile)
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
            if self.energy >= card.cost:
                self.energy -= card.cost
                self.game.add_event(self, self.game.enemy, damage=card.damage, armor=card.armor)
                self.hand.remove(card)
                self.discard_pile.append(card)
            else:
                print(f"{self.name} does not have enough energy to play this card.")
        else:
            print(f"{self.name} does not have this card in hand.")
    
    def end_turn(self):
        self.discard_hand()
    
    def start_turn(self):
        self.energy = self.max_energy
        print(f"{self.name} started their turn with {self.energy} energy.")
        self.draw_to_max_hand()
    
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

class game:
    def __init__(self, player=None, enemy=None, events=[]):
        self.player = player
        self.enemy = enemy
        self.events = events
        self.event_idx = 0
    
    def add_event(self, user, target, damage=0, armor=0):
        created_event = event(idx=len(self.events), user=user, target=target, damage=damage, armor=armor)
        self.events.append(created_event)
        print(f"Event added: {created_event}")
    
    def resolve_events(self):
        for event in self.events[self.event_idx:]:
            if event.resolve():
                print(f"Event {event.idx} resolved.")
            else:
                print(f"Event {event.idx} failed to resolve.")
        self.event_idx = len(self.events)
    
    def play_round(self):
        self.player.start_turn()
        self.player.end_turn()
        self.resolve_events()
        self.enemy.take_action(self.player)
        self.resolve_events()
        print(f"Round played. {self.player.name} has {self.player.health} health left.")
        print(f"{self.enemy.name} has {self.enemy.health} health left.")
    
    def add_player(self, player):
        self.player = player
        print(f"Player {player.name} added to the game.")
    
    def add_enemy(self, enemy):
        self.enemy = enemy
        print(f"Enemy {enemy.name} added to the game.")

class event:
    def __init__(self, idx, user, target, damage=0, armor=0):
        self.idx = idx
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
            self.user.armor += self.armor
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
        self.game.add_event(self, player, damage=self.damage)
    
    def defend(self, player):
        self.game.add_event(self, self, armor=1)
    
    def do_nothing(self, player):
        self.game.add_event(self, self)
        
    def take_action(self, player):
        action = random()
        cumulative_weight = 0
        for action_name, weight in self.action_weights.items():
            cumulative_weight += weight
            if action < cumulative_weight:
                getattr(self, action_name)(player)
                break
    
    def __str__(self):
        return self.name

if __name__ == "__main__":
    # Create player and enemy
    game_instance = game()
    player1 = player("Player 1", game_instance)
    game_instance.add_player(player1)
    enemy1 = enemy("Enemy 1", game_instance)
    game_instance.add_enemy(enemy1)
    

    # Create cards
    card1 = card(1, "Fireball", cost=2, damage=5)
    card2 = card(2, "Shield", cost=1, armor=3)

    # Add cards to player's deck
    for _ in range(7):
        player1.add_card_to_deck(card1)
    for _ in range(3):
        player1.add_card_to_deck(card2)
    player1.shuffle_deck()
    game_instance.play_round()