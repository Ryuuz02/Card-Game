from game import game
from player import player
from enemy import enemy
from card import card
from effect import effect


if __name__ == "__main__":
    # Create player and enemy
    game_instance = game()
    player1 = player("Player 1", game_instance)
    game_instance.add_player(player1)
    enemy1 = enemy("Enemy 1", game_instance)
    game_instance.add_enemy(enemy1)

    # Create cards and effects
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