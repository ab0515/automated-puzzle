"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> from sudoku_puzzle import SudokuPuzzle
    >>> s = SudokuPuzzle(9,
    ...                 ["*", "*", "*", "7", "*", "8", "*", "1", "*",
    ...                  "*", "*", "7", "*", "9", "*", "*", "*", "6",
    ...                  "9", "*", "3", "1", "*", "*", "*", "*", "*",
    ...                  "3", "5", "*", "8", "*", "*", "6", "*", "1",
    ...                  "*", "*", "*", "*", "*", "*", "*", "*", "*",
    ...                  "1", "*", "6", "*", "*", "9", "*", "4", "8",
    ...                  "*", "*", "*", "*", "*", "1", "2", "*", "7",
    ...                  "8", "*", "*", "*", "7", "*", "4", "*", "*",
    ...                  "*", "6", "*", "3", "*", "2", "*", "*", "*"],
    ...                 {"1", "2", "3", "4", "5", "6", "7", "8", "9"})
    >>> sol = depth_first_solve(s)
    >>> while sol.children:
    ...     sol = sol.children[0]
    >>> print(sol)
    645|738|912
    217|594|836
    983|126|574
    -----------
    352|847|691
    498|613|725
    176|259|348
    -----------
    539|461|287
    821|975|463
    764|382|159
    <BLANKLINE>
    <BLANKLINE>
    """
    overlap = {}
    pn = PuzzleNode(puzzle)
    solution_node = puzzle_node_tree(pn, overlap)
    assert solution_node is not None, "The Puzzle is not solvable"
    if solution_node.puzzle.is_solved():
        # Remove the children of the solution.
        solution_node.children = []
        # Goes up while deleting other possible children.
        while solution_node.parent is not None:
            solution_node.parent.children = [solution_node]
            solution_node = solution_node.parent
        return solution_node
    # Return None if there is no further possible solution.
    else:
        return None


def puzzle_node_tree(puzzle_node, overlap):
    """
    Create a PuzzleNode of puzzle_node and return the first node
    of PuzzleNode that is a solution to the puzzle_node.puzzle

    @type puzzle_node: PuzzleNode
    @type overlap: dict[str : Puzzle]
    @rtype: PuzzleNode | None

    >>> from sudoku_puzzle import SudokuPuzzle
    >>> grid = ["4", "*", "2", "*"]
    >>> grid += ["*", "*", "4", "*"]
    >>> grid += ["*", "*", "3", "*"]
    >>> grid += ["2", "*", "*", "*"]
    >>> s = SudokuPuzzle(4, grid, {"1", "2", "3", "4"})
    >>> pn = PuzzleNode(s)
    >>> solution = puzzle_node_tree(pn, {})
    >>> print(solution)
    41|23
    32|41
    -----
    14|32
    23|14
    <BLANKLINE>
    <BLANKLINE>
    """
    # An empty node.
    if puzzle_node is None:
        return None
    # Return the node if it is a solution.
    elif puzzle_node.puzzle.is_solved():
        return puzzle_node
    else:
        puzzle_node.children = generate_children(puzzle_node)
        overlap[puzzle_node.puzzle.__str__()] = puzzle_node.puzzle
        for node in puzzle_node.children:
            # Append the puzzle that has been seen to the overlap.
            if (not node.puzzle.fail_fast()) and node.puzzle.__str__() \
                    not in overlap:
                solution = puzzle_node_tree(node, overlap)
                if solution is not None:
                    return solution
        # Return None if there is no further possible solution.
        return None


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent. Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None
    >>> from sudoku_puzzle import SudokuPuzzle
    >>> s = SudokuPuzzle(9, ["*", "*", "*", "7", "*", "8", "*", "1", "*",
    ... "*", "*", "7", "*", "9", "*", "*", "*", "6",
    ... "9", "*", "3", "1", "*", "*", "*", "*", "*",
    ... "3", "5", "*", "8", "*", "*", "6", "*", "1",
    ... "*", "*", "*", "*", "*", "*", "*", "*", "*",
    ... "1", "*", "6", "*", "*", "9", "*", "4", "8",
    ... "*", "*", "*", "*", "*", "1", "2", "*", "7",
    ... "8", "*", "*", "*", "7", "*", "4", "*", "*",
    ... "*", "6", "*", "3", "*", "2", "*", "*", "*"],
    ... {"1", "2", "3", "4", "5", "6", "7", "8", "9"})
    >>> sol = breadth_first_solve(s)
    >>> while sol.children:
    ...     sol = sol.children[0]
    >>> print(sol)
    645|738|912
    217|594|836
    983|126|574
    -----------
    352|847|691
    498|613|725
    176|259|348
    -----------
    539|461|287
    821|975|463
    764|382|159
    <BLANKLINE>
    <BLANKLINE>
    """
    current_node = PuzzleNode(puzzle)
    queue = deque()
    current_node.children = generate_children(current_node)
    # Add children to the queue.
    for child in current_node.children:
        queue.append(child)
    # Iterate until the queue is empty.
    while len(queue) != 0:
        remove = queue.popleft()
        remove.children = generate_children(remove)
        if remove.puzzle.is_solved():
            # Remove the children of the solution.
            remove.children = []
            # Goes up while deleting other possible children.
            while remove.parent is not None:
                remove.parent.children = [remove]
                remove = remove.parent
            return remove
        # Skip the code that fail fasts for the efficiency.
        elif remove.puzzle.fail_fast():
            pass
        else:
            for child in remove.children:
                queue.append(child)
    # Return None if there is no further possible solution.
    return None


def generate_children(node):
    """
    Return the children (extension) of a node.

    @type node: PuzzleNode
    @rtype: list[PuzzleNode]

    >>> from mn_puzzle import MNPuzzle
    >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
    >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> pn = PuzzleNode(MNPuzzle(target_grid, start_grid))
    >>> lst = generate_children(pn)
    >>> for i in lst:
    ...     print(i)
    ===Current Stage===
    ('1', '2', '3')
    ('4', '*', '5')
    ====Goal Board=====
    ('*', '2', '3')
    ('1', '4', '5')
    <BLANKLINE>
    <BLANKLINE>
    ===Current Stage===
    ('1', '2', '*')
    ('4', '5', '3')
    ====Goal Board=====
    ('*', '2', '3')
    ('1', '4', '5')
    <BLANKLINE>
    <BLANKLINE>
    """
    return [PuzzleNode(x, parent=node) for x in node.puzzle.extensions()]

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
