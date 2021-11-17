from collections import Counter
from itertools import product


class Universe:
    """The universe is the map where the cells grow and die.

    It's conceived as an infinite board, so instead a whole map
    representation, only those living cells are maintained."""

    def __init__(self, cells=None):
        """Initialises this instance.

        :param cells: An optional iterable of Cell elements.
        """
        self.cells = set(cells) if cells else set()
        self.generation = 0

    def step(self):
        """Simulation step, thus the following rules are applied:

        1. Any living cell with two or three living neighbours survives
        2. Any dead cell with three alive neighbours becomes a live cell
        3. Any other cell dies or remains dead
        """
        # Alive cells are obtained applying the rules to all the
        # potential active neighbours
        self.cells = {
            c for c, n in self.active_neighbours().items()
            if n == 3 or (n == 2 and c in self.cells)
        }

        # Now all that remains is to advance the generation by one
        self.generation += 1

    def active_neighbours(self):
        """The potentially active cells with their neighbours count.

        :return: A dictionary form {cell: count}
        """
        return Counter(
            neighbour
            for cell in self.cells
            for neighbour in self.neighbours(cell)
        )

    @staticmethod
    def neighbours(cell):
        """All the neighbour positions for a given cell.

        :param cell: The cell in the form (x, y).
        """
        for x, y in product(range(-1, 2), repeat=2):
            if not (x == 0 and y == 0):
                yield cell[0] + x, cell[1] + y

    def add(self, cell):
        """Adds a new cell to the universe.

        If the cell already exists, the method does nothing at all.

        :param cell: The cell in the form (x, y).
        """
        self.cells.add(cell)

    def remove(self, cell):
        """Removes a cell from the universe.

        If the cell doesn't exists, the methods does nothing.

        :param cell: The cell in the form (x, y).
        """
        self.cells.discard(cell)

    def reset(self):
        """Resets the universe state

        It involves removing all the living cells from the universe and
        returning to the generation 0.
        """
        self.cells.clear()
        self.generation = 0

    @property
    def size(self):
        """How many living cells exist in our universe.

        :return: The number of cells.
        """
        return len(self.cells)
