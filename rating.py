__author__ = 'Jann Kleen'

from operator import itemgetter


def get_words(filename='fixtures/wordlist.txt'):
    with open(filename, 'r') as fp:
        words = fp.readlines()
        words = [line.strip() for line in words]
    return words


def get_best_choices(grid, limit=100, offset=0):
    words = get_words()
    scores = [(word, grid.score_word(word)) for word in words]
    return sorted(scores, key=itemgetter(1), reverse=True)[offset:offset+limit]
