from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> mn1 = MNPuzzle(("1", "2", "3"), ("4", "5", "*"))
        >>> mn2 = MNPuzzle(("1", "2", "3"), ("4", "5", "*"))
        >>> mn3 = MNPuzzle(("1", "*", "3"), ("4", "5", "6"))
        >>> mn1 == mn2
        True
        >>> mn1 == mn3
        False
        """
        return (type(self) == type(other) and
                self.n == other.n and self.m == other.m and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a user-friendly string representation.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(target_grid, start_grid)
        >>> print(mn)
        ===Current Stage===
        ('1', '2', '3')
        ('4', '5', '*')
        ====Goal Board=====
        ('*', '2', '3')
        ('1', '4', '5')
        """
        def align_column(grid):
            board = ""
            for i in range(self.n):
                board += str(grid[i]) + "\n"
            return board.strip()
        return ("===Current Stage===\n"
                "{}\n"
                "====Goal Board=====\n"
                "{}".format(align_column(self.from_grid),
                            align_column(self.to_grid)))

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> target_grid = (("1", "*", "3"), ("4", "5", "6"), ("7", "8", "9"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"), ("7", "8", "9"))
        >>> mn = MNPuzzle(target_grid, start_grid)
        >>> lst = mn.extensions()
        >>> for ext in lst:
        ...    print(ext)
        ===Current Stage===
        ('*', '1', '3')
        ('4', '5', '6')
        ('7', '8', '9')
        ====Goal Board=====
        ('*', '2', '3')
        ('1', '4', '5')
        ('7', '8', '9')
        ===Current Stage===
        ('1', '3', '*')
        ('4', '5', '6')
        ('7', '8', '9')
        ====Goal Board=====
        ('*', '2', '3')
        ('1', '4', '5')
        ('7', '8', '9')
        ===Current Stage===
        ('1', '5', '3')
        ('4', '*', '6')
        ('7', '8', '9')
        ====Goal Board=====
        ('*', '2', '3')
        ('1', '4', '5')
        ('7', '8', '9')
        """
        def check_empty_space(gridcopy):
            """
            Return the place of the empty space.

            @type gridcopy: tuple[tuple[str]]
            @rtype: tuple

            # >>> grid = (("*", "2", "3"), ("4", "5", "6"))
            # >>> check_empty_space(grid)
            # (0, 0)
            # >>> grid = (("1", "2", "3"), ("4", "5", "6"), ("7" , "8" , "*"))
            # >>> check_empty_space(grid)
            # (2, 2)
            """
            for i in range(len(gridcopy)):
                if "*" in gridcopy[i]:
                    return i, gridcopy[i].index("*")
            # Raise Error if there is no empty space in the puzzle.
            return AssertionError, "No empty space in the puzzle."

        def tuple_to_list(tup):
            """
            Return a list which was originally tuple.

            @type tup: tuple
            @rtype: list[str]
            """
            return [element for element in tup]

        def shift_right_left(gridcopy, row_num, column_num):
            """
            Return the list of affected grid. If * cannot move to the specific
            place, it returns an empty list

            @type gridcopy: tuple[tuple[str]]
            @type row_num: int
            @type column_num: int
            @rtype: list[tuple[tuple[str]]]
            """
            result = []
            # Extract the specific row to change.
            current_row = gridcopy[row_num]
            # Change the current_row to list in order to mutate.
            current_row_lst = tuple_to_list(current_row)
            if location[1] != 0:
                # Going left!
                # ("5", "*", "6") to ("*", "5", "6")
                current_row_lst[column_num] = current_row_lst[column_num - 1]
                current_row_lst[column_num - 1] = "*"
                # Switch back to tuple
                left_altered = tuple(current_row_lst)
                board_lst = tuple_to_list(gridcopy)
                board_lst[row_num] = left_altered
                result.append(tuple(board_lst))
            if location[1] != self.m - 1:
                # Going right!
                # ("5", "*", "6") to ("5", "6", "*")
                # Reset the values to swap right.
                current_row = gridcopy[row_num]
                current_row_lst = tuple_to_list(current_row)
                current_row_lst[column_num] = current_row_lst[column_num + 1]
                current_row_lst[column_num + 1] = "*"
                # Switch back to tuple
                right_altered = tuple(current_row_lst)
                board_lst = tuple_to_list(gridcopy)
                board_lst[row_num] = right_altered
                result.append(tuple(board_lst))
            return result

        def shift_down_right(gridcopy, row_num, column_num):
            """
            Return the list of affected grid. If * cannot move to the specific
            place, it returns an empty list

            @type gridcopy: tuple[tuple[str]]
            @type row_num: int
            @type column_num: int
            @rtype: list[tuple[tuple[str]]]
            """
            result = []
            if location[0] != 0:
                current_row = gridcopy[location[0]]
                upper_row = gridcopy[location[0] - 1]
                current_row_lst = tuple_to_list(current_row)
                upper_row_lst = tuple_to_list(upper_row)
                current_row_lst[column_num] = upper_row_lst[column_num]
                upper_row_lst[column_num] = "*"
                current_row, upper_row = tuple(current_row_lst), \
                                         tuple(upper_row_lst)
                board_lst = tuple_to_list(gridcopy)
                board_lst[row_num] = current_row
                board_lst[row_num - 1] = upper_row
                upper_altered = tuple(board_lst)
                result.append(upper_altered)
            if location[0] != self.n - 1:
                upper_row = gridcopy[location[0] + 1]
                lower_row = gridcopy[location[0]]
                upper_lst = tuple_to_list(upper_row)
                lower_lst = tuple_to_list(lower_row)
                lower_lst[location[1]] = upper_lst[location[1]]
                upper_lst[location[1]] = "*"
                upper_row, lower_row = tuple(upper_lst), tuple(lower_lst)
                big_lst = tuple_to_list(gridcopy)
                big_lst[location[0]] = lower_row
                big_lst[location[0] + 1] = upper_row
                changed = tuple(big_lst)
                result.append(changed)
            return result

        grid = self.from_grid
        # Location is the tuple indicator of location of the empty space.
        # (Row, Column)
        location = check_empty_space(grid)
        row = location[0]
        column = location[1]
        possibilities = shift_right_left(grid, row, column) +\
                        shift_down_right(grid, row, column)
        return [MNPuzzle(x, self.to_grid) for x in possibilities]

    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return whether Puzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mn = MNPuzzle(target_grid, start_grid)
        >>> mn.is_solved()
        False
        >>> current_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mn = MNPuzzle(target_grid, current_grid)
        >>> mn.is_solved()
        True
        """
        return self.from_grid == self.to_grid

# def check_empty_space(grid):
#     """
#     Return the place of the empty space.
#
#     @type grid: tuple[tuple[str]]
#     @rtype: tuple
#
#     >>> grid = (("*", "2", "3"), ("4", "5", "6"))
#     >>> check_empty_space(grid)
#     (0, 0)
#     >>> grid = (("1", "2", "3"), ("4", "5", "6"), ("7" , "8" , "*"))
#     >>> check_empty_space(grid)
#     (2, 2)
#     """
#     for i in range(len(grid)):
#         if "*" in grid[i]:
#             return i, grid[i].index("*")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
