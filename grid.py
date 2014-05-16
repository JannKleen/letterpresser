__author__ = 'Jann Kleen'

from collections import defaultdict, Counter
from operator import itemgetter
from copy import deepcopy


class Grid(object):
    def __init__(self, letters=None):
        assert isinstance(letters, (list, tuple)), "List of letters needs to be list or tuple"

        self.letters = letters
        self.alphabet = Counter(map(itemgetter(0), letters))

        # create list of scores for each letter
        self.letter_buckets = defaultdict(list)
        for letter, score in letters:
            self.letter_buckets[letter].append(score)

        # and sort them
        for letter, scores in self.letter_buckets.items():
            self.letter_buckets[letter] = sorted(scores)

    def score_word(self, word):
        if Counter(list(word)) - self.alphabet:
            return None  # can't create that word with our alphabet

        _letter_buckets = deepcopy(self.letter_buckets)

        return sum(map(lambda c: _letter_buckets[c].pop(), list(word)))
