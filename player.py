from random import shuffle

class player:
    """Represents the player."""
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
        """Draws a card from the deck to the hand."""
        if not self.deck:
            self.shuffle_discard_into_deck()
        card_drawn = self.deck.pop(0)
        self.hand.append(card_drawn)
        print(f"{self.name} drew a card: {card_drawn}")

    def shuffle_discard_into_deck(self):
        """Shuffles the discard pile back into the deck."""
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
        """Plays a card from the hand."""
        if card in self.hand:
            self.hand.remove(card)
            self.energy -= card.cost
            card.play(self.game)
            self.discard_pile.append(card)
            print(f"{self.name} played {card}.")
        else:
            print(f"{self.name} does not have {card} in hand.")

    def start_turn(self):
        """Starts the player's turn."""
        self.energy = self.max_energy
        print(f"{self.name} started their turn with {self.energy} energy.")
        self.draw_to_max_hand()
        self.take_turn()

    def take_turn(self):
        """Handles the player's turn logic."""
        while True:
            print("Current Hand:")
            for i, card in enumerate(self.hand):
                print(f"{i + 1}: {card}")
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
        """Ends the player's turn."""
        self.discard_hand()

    def discard_hand(self):
        """Discards all cards from hand."""
        self.discard_pile.extend(self.hand)
        self.hand.clear()
        print(f"{self.name} discarded their hand.")

    def draw_to_max_hand(self):
        """Draws cards until hand is at max size."""
        for _ in range(self.max_hand_size):
            self.draw_card()
        print(f"{self.name} drew cards to max hand size. Hand size is now {len(self.hand)}.")

    def shuffle_deck(self):
        shuffle(self.deck)
        print(f"{self.name} shuffled their deck.")

    def __str__(self):
        return self.name

    def __eq__(self, value):
        return isinstance(value, player) and self.name == value.name