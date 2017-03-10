from puzzle import Puzzle
from copy import deepcopy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # TODO
    # implement __eq__, __str__ methods
    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.
        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> g1 = [["#", "*", "*", "*", "#"]]
        >>> g1 += [["*", ".", "*", "*", "*"]]
        >>> g1 += [["*", "*", "*", "*", "*"]]
        >>> g1 += [["#", "*", "*", "*", "#"]]
        >>> s1 = GridPegSolitairePuzzle(g1, {"*", ".", "#"})
        >>> g2 = [["*", "*", "*", "*", "*"]]
        >>> g2 += [["*", "*", "*", ".", "*"]]
        >>> g2 += [["*", "*", "*", "*", "*"]]
        >>> g2 += [["*", "*", "*", "*", "*"]]
        >>> s2 = GridPegSolitairePuzzle(g2, {"*", ".", "#"})
        >>> s1.__eq__(s2)
        False
        >>> g3 = [["*", "*", "*", "*", "*"]]
        >>> g3 += [["*", "*", "*", ".", "*"]]
        >>> g3 += [["*", "*", "*", "*", "*"]]
        >>> g3 += [["*", "*", "*", "*", "*"]]
        >>> s3 = GridPegSolitairePuzzle(g3, {"*", ".", "#"})
        >>> s2.__eq__(s3)
        True
        """
        return (type(self) == type(other) and self._marker == other._marker and
                self._marker_set == self._marker_set)

    def __str__(self):
        """
        Return a string representation of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [["#", "#", "*", "*", "#", "#"],\
        ["*", "*", "*", "*", "*", "*"],\
        ["*", "*", ".", "*", "*", "*"],\
        ["*", "*", "*", "*", "*", "*"],\
        ["#", "#", "*", "*", "#", "#"]]
        >>> s = GridPegSolitairePuzzle(grid, {"#", "*", "."})
        >>> print(s)
        ##**##
        ******
        **.***
        ******
        ##**##
        """
        result = ""
        for i in self._marker:
            for j in i:
                result += j
            result += "\n"
        return result[:len(result)-1]

    # __repr__ is up to you

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return list of legal extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> pl = GridPegSolitairePuzzle(grid, {".", "#", "*"})
        >>> T1 = list(pl.extensions())
        >>> p = {"#", ".", "*"}
        >>> grid1 = [["*", "*", ".", "*", "*"],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> grid2 = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", ".", "."],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> grid3 = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            [".", ".", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"]]
        >>> grid4 = [["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", "*", "*", "*"],\
            ["*", "*", ".", "*", "*"],\
            ["*", "*", ".", "*", "*"]]
        >>> T2 = [GridPegSolitairePuzzle(grid1, p),\
        GridPegSolitairePuzzle(grid2, p), GridPegSolitairePuzzle(grid3, p),\
        GridPegSolitairePuzzle(grid4, p)]
        >>> len(T1) == len(T2)
        True
        >>> all([s in T2 for s in T1])
        True
        >>> all([s in T1 for s in T2])
        True
        """
        def jump_right_left(board, marker_set):
            """
            Return a list of str where a peg can jump over in a row

            @type board: list[str]
            @type marker_set: set[str]
            @rtype: list[[str]]

            #>>> grid = [["*", "*", "*", "*", "*"],\
            #        ["*", "*", "*", "*", "*"],\
            #        ["*", "*", "*", "*", "*"],\
            #        ["*", "*", ".", "*", "*"],\
            #        ["*", "*", "*", "*", "*"]]
            #>>> ls = jump_right_left(grid)
            #>>> print(ls)
            [['']]
            """
            peg, empty, hole = "*", "#", "."
            lst = []
            for x in range(len(board)):
                for j in range(len(board[x])):
                    l = deepcopy(board)
                    if board[x][j] == peg:
                        if j - 2 >= 0 and board[x][j - 2] == hole and\
                                        board[x][j - 1] == peg:
                            l[x][j - 1] = l[x][j] = hole, hole
                            l[x][j - 2] = peg
                            lst.append(l)
                        elif j + 2 < len(board[x]) and board[x][j + 2] == hole\
                                and board[x][j + 1] == peg:
                            l[x][j + 1] = l[x][j] = hole
                            l[x][j + 2] = peg
                            lst.append(l)
            return lst

        def jump_up_down(board, marker_set):
            """
            Return a list of list of str which contains a modified configuration

            @type board: list of list of str
            @type marker_set: set[str]
            @rtype: list of list of list of str

            #>>> grid = [["*", "*", "*", "*", "*"],\
            #        ["*", "*", "*", "*", "*"],\
            #        ["*", "*", "*", "*", "*"],\
            #        ["*", "*", ".", "*", "*"],\
            #        ["*", "*", "*", "*", "*"]]
            #>>> jump_up_down(grid)
            """
            peg, empty, hole = "*", "#", "."
            lst = []
            for x in range(len(board)):
                for j in range(len(board[x])):
                    l = deepcopy(board)
                    if board[x][j] == peg:
                        if x-2 >= 0 and board[x-1][j] == peg and board[x-2][j]\
                                == hole:
                            l[x-1][j] = l[x][j] = hole
                            l[x-2][j] = peg
                            lst.append(l)
                        elif x+2 < len(board) and board[x+1][j] == peg and \
                                        board[x+2][j] == hole:
                            l[x+1][j] = l[x][j] = hole
                            l[x+2][j] = peg
                            lst.append(l)
            return lst

        marker, marker_set, extension = self._marker, self._marker_set, []
        extension = (jump_right_left(marker, marker_set) +
                     jump_up_down(marker, marker_set))
        r= []
        for i in extension:
            r.append(GridPegSolitairePuzzle(i, marker_set))
        return r

    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return True iff Puzzle self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid = [[".", ".", ".", ".", "."],\
        [".", ".", "*", ".", "."],\
        [".", ".", ".", ".", "."],\
        [".", ".", ".", ".", "."],\
        [".", ".", ".", ".", "."]]
        >>> p = GridPegSolitairePuzzle(grid, {".", "#", "*"})
        >>> p.is_solved()
        True
        """
        marker, count = self._marker, 0
        for i in marker:
            count += i.count("*")
            if count > 1:
                return False
        return count == 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
