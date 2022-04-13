import os
import random

import numpy as np
import pandas as pd


class Card():
    # The suit character
    suit_characters = {"Spades": "\u2660", "Hearts": "\u2665",
                       "Clubs": "\u2663", "Diamonds": "\u2666"}

    # The rank value
    rank_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
                   "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                   "J": 10, "Q": 10, "K": 10}

    def __init__(self, suit: str, rank: str):
        # The suit of the card (Spades, Hearts, Clubs, Diamonds)
        self.suit = suit

        # The unicode value for the suit of the card (Visual resource)
        self.character = self.suit_characters[suit]

        # The rank of the card (A, 1, 2, ..., Q, K)
        self.rank = rank

        # The value of the card (Ex: King is a 10)
        self.value = self.rank_values[rank]

    def __repr__(self):
        return f"Card object: {self.rank} of {self.suit}, value = {self.value}"


class Deck():
    # The card suits
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]

    # The card ranks
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, num_decks: int):

        self.num_decks = num_decks

        self.deck = []

    def __repr__(self):
        return f"Deck object: {self.num_decks} decks"

    def create_deck(self):
        #  Create cards for each deck
        for i in self.num_decks:
            # Iterate through suits
            for suit in self.suits:
                # Iterate through ranks
                for rank in self.ranks:
                    # Add the new card to the deck
                    self.deck.append(Card(suit, rank))

    def cut(self):
        cut_index = random.randint(-(0.4 * self.num_decks * 52),
                                   -(0.2 * self.num_decks * 52))
        self.deck.insert(cut_index, "cut")

    def shuffle(self):
        # Randomly shuffle the deck
        random.shuffle(self.deck)

        # Cut the deck and insert the shuffle indicator
        if self.num_decks > 2:
            self.cut()

    def empty(self):
        # Empty the deck of card
        for card in self.deck:
            del card


class Dealer():
    def __init(self, stand_soft_17: bool):

        self.hand = []
        self.score = 0

    def __repr__(self):
        pass

    def draw_card(self, deck):
        return deck.deck.pop(random.choice(deck.deck))

    def deal_hand(self, players, deck):

        for i in range(2):
            for player in players:
                player.hand.append(self.draw_card(deck))

                self.hand.append(self.draw_card())


class Player():
    def __init__(self, name: str, starting_cash: int, strategy, count_strategy):

        self.name = name
        self.balance = starting_cash
        self.strategy = pd.readcsv(
            "blackjack_basic_strategy.csv", index_col=0).astype(str)
        self.count_strategy = count_strategy

        # Round relevant variables
        self.bet = 0
        self.hand = []
        self.hand_value = 0
        self.hand_decision = None

        self.wins = 0
        self.losses = 0
        self.total_rounds = self.wins + self.losses

    def __repr__(self):
        return f"Player object: {self.name}, balance = {self.balance}"

    def place_bet(self, min_bet, max_bet):
        self.bet = min_bet

    def hand_total(self):
        self.hand_value = sum(card.value for card in self.hand)

    def check_ace(self):
        if 'A' in [card.rank for card in self.hand]:
            return True
        else:
            return False

    def make_decision(self, dealer_card):

        if self.hand_value == 21:
            pass

        else:

            self.hand_decision = self.strategy.at[self.hand_value, dealer_card]


class Rules():
    def __init__(self, min_bet, max_bet, win_multiplier, blackjack_multiplier):

        # Betting Rules
        self.min_bet = min_bet
        self.max_bet = max_bet

        # The bet multiplier if the player wins
        self.win_multiplier = win_multiplier
        # The bet multiplier if the player gets a blackjack
        self.blackjack_multiplier = blackjack_multiplier

    def generate_rule_dict(self):
        return {'min_bet': self.min_bet,
                'max_bet': self.max_bet,
                'win_multiplier': self.win_multiplier,
                'blackjack_multiplier': self.blackjack_multiplier}


class Game():
    def __init__(self, rules: dict, deck: Deck, dealer: Dealer, players: list):

        self.rules = rules.generate_rule_dict() if isinstance(Rules) else rules
        self.deck = deck
        self.dealer = dealer
        self.players = players if isinstance(players, list) else list(players)

        self.round_count = 0

    def place_bets(self):
        for player in self.players:
            player.place_bet(self.rules['min_bet'], self.rules['max_bet'])

    def deal_hand(self):
        self.dealer.deal_hand(self.players, self.deck)

    def make_decisions(self):
        for player in self.players:
            player.make_decision(self.dealer.hand[0])

    def play_round(self):
        self.place_bets()
        self.deal_hand()
        self.make_decisions()


def clear():
    if os.name == 'nt':
        os.system('CLS')
    if os.name == 'posix':
        os.system('clear')


if __name__ == '__main__':
    pass
