from Minesweeper import *
import unittest


class TestMinesweeperGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(1)

    def test_GameSelect(self):
        # Check the effects of out of bounds row and column.
        # For the first move, the inital variable should
        # remain false. Here we check if it did.
        self.game.Select(100, 100)
        self.assertEqual(self.game.initial, False)
        # Checking changes to the board:
        board = [True if j.reveal is False else False
                 for i in self.game.board.board for j in i]
        self.assertEqual(all(board), True)

        # Checking the out of bounds for the non-first move.
        self.game.Select(5, 5)  # The initial move
        b1 = self.game.board.board  # The board after the first move
        self.game.Select(100, 100)  # Out of bounds move
        b2 = self.game.board.board
        # Checking if the board has changed after making the second
        # move.
        self.assertEqual(b1, b2)

        # Above we selected row 5, column 5. Now we check if
        # this cell was in fact revealed, and it has 0
        # adjacent bombs.
        revealed = self.game.board.board[5][5].reveal
        type = self.game.board.board[5][5].type
        self.assertEqual(revealed, True)
        self.assertEqual(type, 0)

    def test_CheckGame(self):
        # Check that when the total number of cells on the
        # board to be revealed is 0, the game is won.
        self.game.board.total = 0
        self.game.CheckGame()
        self.assertEqual(self.game.GameWin, True)
        self.game.board.total = 100

        # Check that when the bombReveal variable is set to True
        # The game will be declared as lost.
        self.game.board.bombReveal = True
        self.game.CheckGame()
        self.assertEqual(self.game.GameWin, False)

    def test_LayFlag(self):
        # Test that toggling a flag for a cell on and off works.
        self.game.LayFlag(5, 5)  # Toggle on
        self.assertEqual(self.game.board.board[5][5].flag, True)

        self.game.LayFlag(5, 5)  # Toggle off
        self.assertEqual(self.game.board.board[5][5].flag, False)


class TestMinesweeperBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(1)

    def test_InitiateBoard(self):
        # Check the board is initiated with all Cell type
        board = self.board.InitiateBoard(1)
        check = [True if isinstance(c, Cell) else False
                 for row in board for c in row]
        self.assertEqual(all(check), True)

    def test_BoardSize(self):
        # Can initiate board with three difficulties which
        # lead to 3 different square sizes.
        b1 = self.board.InitiateBoard(1)
        self.assertEqual((len(b1), len(b1[0])), (10, 10))
        b2 = self.board.InitiateBoard(2)
        self.assertEqual((len(b2), len(b2[0])), (15, 15))
        b3 = self.board.InitiateBoard(3)
        self.assertEqual((len(b3), len(b3[0])), (20, 20))

    def test_InitialSelect(self):
        # Check the out of bounds condition is met and returns None
        s = self.board.InitialSelect(100, 100)
        self.assertEqual(s, None)
        # Checking further that no cell in the board was revealed
        # upon an out of bounds selection.
        b = [True if i.reveal is False else False
             for j in self.board.board for i in j]
        self.assertEqual(all(b), True)

    def test_InitialSelect_bombs(self):
        # Test the correct no. of bombs are laid.
        self.board.InitialSelect(5, 5)
        bombs = len(self.board.board)**2//5
        b = sum(1 if i.type == "B" else 0 for j in self.board.board for i in j)
        self.assertEqual(bombs, b)

        # check that no bomb is placed in off-limit area
        for i in range(4, 5, 6):
            for j in range(4, 5, 6):
                self.assertNotEqual(self.board.board[i][j], "B")

    def test_SetBoard(self):
        # Testing that the board holds the correct number for
        # adjacent bombs.

        # Laying one bomb on the board and setting the board.
        self.board.board[5][5].type = "B"
        self.board.SetBoard()

        # Checking that the no. of bombs for adjacent cells
        # is 1.
        for r in (4, 5, 6):
            for c in (4, 5, 6):
                if r == 5 and c == 5:
                    continue
                val = self.board.board[r][c].type
                self.assertEqual(val, 1)

        # Checking that all remaining cells still have a
        # no. of bombs value of 0
        for r in range(len(self.board.board)):
            for c in range(len(self.board.board)):
                if r in (4, 5, 6) and c in (4, 5, 6):
                    continue
                val = self.board.board[r][c].type
                self.assertEqual(val, 0)

    def test_ClearEmpty(self):
        # Testing that only the adjacent 0 cells
        # have their adjacent cells revealed.

        # Creating a row of bombs for row 2, and calling the
        # ClearEmpty function at 0, 0 so that all rows above
        # the bombs should be revealed.
        for i in range(len(self.board.board[0])):
            self.board.board[2][i].type = "B"

        self.board.SetBoard()  # Set the board cells
        self.board.ClearEmpty(0, 0)  # Begin the function

        # The first 2 rows will show as revealed and all others
        # as not revealed.
        for r in range(2):
            for c in range(len(self.board.board[0])):
                revealed = self.board.board[r][c].reveal
                self.assertEqual(revealed, True)

        for r in range(3, len(self.board.board[0])):
            for c in range(len(self.board.board)):
                revealed = self.board.board[r][c].reveal
                self.assertEqual(revealed, False)

    def test_Select_NoChange(self):
        # Check the out of bounds condition is met and returns None
        s = self.board.Select(100, 100)
        self.assertEqual(s, None)
        # Checking further that no cell in the board was revealed
        # upon an out of bounds selection.
        b = [True if i.reveal is False else False
             for j in self.board.board for i in j]
        self.assertEqual(all(b), True)

        # Checking that nothing happens when selecting cell that's
        # already revealed.
        # We're setting one cell to revealed and keeping a copy
        # of the board. We then call the function for the same
        # cell and seeing if there was any change to the board.
        self.board.board[5][5].reveal = True
        previous = self.board.board
        self.board.Select(5, 5)
        self.assertEqual(self.board.board, previous)
        self.board.board[5][5].reveal = False

    def test_Select_Bombs(self):
        # Testing that once one bomb is selected all are revealed.
        # Below we set several bombs, select one of them, and
        # then check that they all have been revealed.
        self.board.board[4][5].type = "B"
        self.board.board[2][8].type = "B"
        self.board.board[7][1].type = "B"
        self.board.board[3][2].type = "B"

        self.board.Select(4, 5)

        self.assertEqual(self.board.board[4][5].reveal, True)
        self.assertEqual(self.board.board[2][8].reveal, True)
        self.assertEqual(self.board.board[7][1].reveal, True)
        self.assertEqual(self.board.board[3][2].reveal, True)

        # Need to check that once a bomb is selected, bombReveal
        # var is set to true so that the CheckGame method can
        # determine the game is lost.
        self.assertEqual(self.board.bombReveal, True)

        # Check that when one non-bomb piece is selected, it's
        # revealed.
        self.board.board[4][5].type = "B"
        self.board.board[3][5].type = 1
        self.board.Select(3, 5)  # Selecting non-bomb cell
        self.assertEqual(self.board.board[3][5].reveal, True)

    def test_Select_Clear(self):
        # Testing that when a 0 cell is selected, surrounding
        # cells are revealed also.

        # Setting the bombs
        self.board.board[2][0].type = "B"
        self.board.board[2][1].type = "B"
        self.board.board[2][2].type = "B"
        self.board.board[1][2].type = "B"
        self.board.board[0][2].type = "B"

        # Setting the board and selecting a piece
        self.board.SetBoard()
        self.board.Select(0, 0)

        self.assertEqual(self.board.board[0][0].reveal, True)
        self.assertEqual(self.board.board[0][1].reveal, True)
        self.assertEqual(self.board.board[1][0].reveal, True)
        self.assertEqual(self.board.board[1][1].reveal, True)

    def test_RevealCell(self):
        # Testing that if a cell is not revealed, then it will be.
        self.board.RevealCell(0, 0)
        revealed = self.board.board[0][0].reveal
        self.assertEqual(revealed, True)

        # Testing that if a cell is revealed, nothing changes.
        # Taking a copy of board prior to method call. Then
        # comparing it to board after.
        previous = self.board.board
        self.board.RevealCell(0, 0)
        self.assertEqual(self.board.board[0][0].reveal, True)
        self.assertEqual(self.board.board, previous)

    def test_SetFlag(self):
        # Test that flag is switched on for non-revealed piece.
        self.board.SetFlag(5, 5)
        flag = self.board.board[5][5].flag
        self.assertEqual(flag, True)

        # Test that if flagged cell is selected, it is unflagged.
        self.board.SetFlag(5, 5)
        flag = self.board.board[5][5].flag
        self.assertEqual(flag, False)

        # Test that nothing happens for cell that is revealed.
        self.board.RevealCell(5, 5)
        self.board.SetFlag(5, 5)
        cell = self.board.board[5][5].flag
        self.assertEqual(cell, False)


class TestMinesweeperCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell()

    def test_rep(self):
        # Testing that if a cell is not revealed, it will show as -.
        self.assertEqual(str(self.cell), "-")

        # Testing that if a cell is not revealed but is flagged,
        # it will show.
        self.cell.flag = True
        self.assertNotEqual(str(self.cell), "-")
        self.cell.flag = False

        # Testing that if a cell is revealed, it will show the type.
        self.cell.reveal = True
        self.assertNotEqual(str(self.cell), "-")
