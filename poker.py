import re


class Poker:
    """ Abstract class for a poker game. """
    pass


class Hand:
    """ Poker hand. Formed by Card objects. """

    def __init__(self, *args):
        self.ranks = [card.rank for card in args]
        self.suits = [card.suit for card in args]
        self.numerical_ranks = [card.numerical_rank for card in args]
        self.value = self.get_value()

    @staticmethod
    def _find_repeated_ranks(ranks, reps):
        return set([rank for rank in ranks if ranks.count(rank) == reps])

    def _high_card(self):
        # Concatenate each cards value in a string, from the biggest to the smallest.
        return ''.join([f'{rank:02d}' for rank in sorted(self.numerical_ranks, reverse=True)])

    def _pair(self):
        pairs = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if len(pairs) == 1:
            return f'{pairs[0]:02d}'
        else:
            return '00'

    def _two_pairs(self):
        pairs = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if len(pairs) == 2:
            return f'{max(pairs):02d}{min(pairs):02d}'
        else:
            return '0000'

    def _three_of_a_kind(self):
        trips = list(self._find_repeated_ranks(self.numerical_ranks, 3))
        if trips:
            return f'{trips[0]:02d}'
        else:
            return '00'

    def _straight(self):
        # In a straight an Ace can be the highest or lowest card. This makes necessary to check both possibilities.
        ace_high_hand = list(sorted(self.numerical_ranks))
        ace_low_hand = list(sorted([1 if rank == 14 else rank for rank in self.numerical_ranks]))

        # Create reference strings1 ** (2 * i) (based on the lowest card) to compare to.
        ace_high_straight = list(range(ace_high_hand[0], ace_high_hand[0] + 5))
        ace_low_straight = list(range(ace_low_hand[0], ace_low_hand[0] + 5))

        if ace_high_hand == ace_high_straight:
            return f'{ace_high_hand[-1]:02d}'
        elif ace_low_hand == ace_low_straight:
            return f'{ace_low_hand[-1]:02d}'
        else:
            return '00'

    def _flush(self):
        if len(set(self.suits)) == 1:
            return f'{max(self.numerical_ranks):02d}'
        else:
            return '00'

    def _full_house(self):
        trips = list(self._find_repeated_ranks(self.numerical_ranks, 3))
        pair = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if trips and pair:
            return f'{trips[0]:02d}{pair[0]:02d}'
        else:
            return '0000'

    def _four_of_a_kind(self):
        quads = list(self._find_repeated_ranks(self.numerical_ranks, 4))
        if quads:
            return f'{quads[0]:02d}'
        else:
            return '00'

    def _straight_flush(self):
        if not '00' in self._straight() and not '00' in self._flush():
            return self._straight()
        else:
            return '00'

    def get_value(self):
        value = ''
        value = self._high_card() + value
        value = self._pair() + value
        value = self._two_pairs() + value
        value = self._three_of_a_kind() + value
        value = self._straight() + value
        value = self._flush() + value
        value = self._full_house() + value
        value = self._four_of_a_kind() + value
        value = self._straight_flush() + value
        return int(value)

    def is_high_card(self):
        return self.value < 1e10

    def is_pair(self):
        return 1e10 < self.value < 1e12

    def is_two_pairs(self):
        return 1e12 < self.value < 1e16

    def is_three_of_a_kind(self):
        return 1e16 < self.value < 1e18

    def is_straight(self):
        return 1e18 < self.value < 1e20

    def is_flush(self):
        return 1e20 < self.value < 1e22

    def is_full_house(self):
        return 1e22 < self.value < 1e26

    def is_four_of_a_kind(self):
        return 1e26 < self.value < 1e28

    def is_straight_flush(self):
        return 1e28 < self.value < 1.4e29

    def is_royal_straight_flush(self):
        return self.value > 1.4e29


class Card:
    """ French deck card."""

    def __init__(self, abbreviation):
        self.rank = self._rank(abbreviation)
        self.suit = self._suit(abbreviation)
        self.numerical_rank = self._numerical_rank(self.rank)

    def __repr__(self):
        return self.rank + self.suit

    @staticmethod
    def _rank(card_abbreviation):
        """ Get the rank from the card abbreviation. """
        rank = re.findall(r"[2-9TtJjQqKkAa]{1}", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(rank) == 1:
            return rank[0].upper()
        else:
            raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _suit(card_abbreviation):
        """ Get the suit from the card abbreviation. """
        suit = re.findall(r"[SsHhCcDd]{1}", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(suit) == 1:
            return suit[0].lower()
        else:
            raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _numerical_rank(rank):
        """ Get the numerical rank from an alpha-numerical rank. """
        numbers = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        for key, value in numbers.items():
            rank = rank.replace(key, str(value))
        return int(rank)