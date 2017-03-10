from puzzle import Puzzle
from time import time

class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

        # TODO
        # implement __eq__ and __str__
    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> w1 = WordLadderPuzzle("same", "cost", {"crime", "money", "list"})
        >>> w2 = WordLadderPuzzle("same", "cost", {"crime", "money", "list"})
        >>> w3 = WordLadderPuzzle("cold", "bald", {"cream", "egg"})
        >>> w1 == w2
        True
        >>> w1 == w3
        False
        """
        return (type(self) == type(other) and self._from_word ==
                other._from_word and self._to_word == other._to_word and
                self._word_set == other._word_set)
        # __repr__ is up to you

    def __str__(self):
        """
        Return a string representation of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> w1 = WordLadderPuzzle("same", "pole", {"most", "unique", "equal"})
        >>> print(w1)
        same
        """
        return self._from_word

        # TODO
        # override extensions
        # legal extensions are WordLadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars
    def extensions(self):
        """
        Return list of legal extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> w1 = WordLadderPuzzle('cost', 'list', {'most', 'flat', 'length',\
        'copy', 'cast', 'range'})
        >>> L1 = w1.extensions()
        >>> L2 = [WordLadderPuzzle('cast', 'list', {'most', 'flat', 'length',\
        'copy', 'cast', 'range'}), WordLadderPuzzle('most', 'list',\
        {'most', 'flat', 'length', 'copy', 'cast', 'range'})]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        """
        extension = []
        cur_word, ws = self._from_word, self._word_set
        result, lst = [], []
        for x in ws:
            if len(x) == len(cur_word):
                result.append(x)
        for i in range(len(cur_word)):
            for ch in self._chars:
                temp = list(cur_word)[:]
                temp[i] = ch
                new_word = "".join(temp)
                if new_word in result and new_word != cur_word:
                    extension.append(WordLadderPuzzle(new_word, self._to_word,
                                                      self._word_set))

        #         lst.append("".join(temp))

        # common = lst.intersection(result) - {self._from_word}
        return extension


        # TODO
        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word
    def is_solved(self):
        """
        Return whether _from_word is equivalent to _to_word.

        @type self: WordLadderPuzzle
        @rtype: bool

        """
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words.txt", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
