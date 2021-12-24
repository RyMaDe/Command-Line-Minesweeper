from random import randint
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


class Game:
    def __init__(self, difficulty):
        self.board = Board(difficulty)  # Game board class setup
        self.DisplayBoard()
        self.initial = False  # Has the initial move been made
        self.GameWin = None  # Used to determine whether game is over

    def Select(self, r, c):
        if r < 0 or r >= len(self.board.board) or c < 0 or c >= len(self.board.board):
            return None
        # When player makes a selection, need to check if it's
        # the first move made as the board is setup after the
        # first move.
        if self.initial is False:
            self.board.InitialSelect(r, c)
            self.initial = True
        else:
            self.board.Select(r, c)
        self.CheckGame()  # Check if the game is over
        self.DisplayBoard()

    def DisplayBoard(self):
        # Display the board to the screen
        self.board.DisplayBoard()

    def CheckGame(self):
        # Check the whether the game is over by checking how
        # many non-bomb cells are yet to be revealed or by
        # checking if a bomb has been revealed. Change the
        # GameWin variable according to this.
        if self.board.total == 0:
            self.GameWin = True
        elif self.board.bombReveal is True:
            self.GameWin = False

    def LayFlag(self, r, c):
        # Enables the user to set a flag at a cell
        self.board.SetFlag(r, c)
        self.DisplayBoard()


class Board:
    def __init__(self, difficulty):
        self.board = self.InitiateBoard(difficulty)
        self.total = len(self.board)**2
        # We subtract no. of bombs from total in InitialSelect.
        # total should show no. of cells subtract no. of bombs.
        # Helps to determine when the game is won.
        self.bombReveal = False
        # Updated when a bomb is selected, helps to determine
        # when the game is lost.

    def InitiateBoard(self, difficulty):
        # Build a list of lists containing empty Cell objects.
        # Size of the board is based off of the difficulty.
        Diff = {1: 10, 2: 15, 3: 20}
        board = [[Cell() for j in range(Diff[difficulty])]
                 for i in range(Diff[difficulty])]
        return board

    def DisplayBoard(self):
        # Display board to the screen along with numberings
        # along the top and left side of the board to show
        # indicies.
        top = range(len(self.board))
        top = list(map(str, top))
        # Need to split the indicies along the top due to char length
        first = "  ".join(top[0:10])
        second = " ".join(top[10:])
        print("   ", first, second)  # Top row indices
        for row in range(len(self.board)):
            # Left Indices and rows
            num = str(row)+" " if row < 10 else row
            print(num, self.board[row])
        print("")

    def InitialSelect(self, r, c):
        # Check the r, c is in bounds
        if r < 0 or r >= len(self.board) or c < 0 or c >= len(self.board):
            return None

        noBombs = len(self.board)**2//5  # Select the no. bombs to have
        self.total -= noBombs
        # Used to deduce the no. of cells we to reveal
        rowOffLimit = (r-1, r, r+1)  # The rows surrounding user selected r
        colOffLimit = (c-1, c, c+1)  # The cols surrounding user selected c

        while noBombs > 0:
            # Select a random row and column.
            row = randint(0, len(self.board)-1)
            col = randint(0, len(self.board)-1)

            if row in rowOffLimit and col in colOffLimit:
                # If the row and column are within the off-limits range
                # then find another row and column
                continue
            elif self.board[row][col].type == "B":
                # If the row, column already has a bomb there.
                continue

            # Lay the bomb and reduce the bombs count
            self.board[row][col].type = "B"
            noBombs -= 1

        self.SetBoard()  # Updates the cells to hold the no. of nearby bombs.
        self.ClearEmpty(r, c)
        # As the initial cell is always type 0, we need to reveal all
        # cells adjacent to it. If any are 0 then repeat.

    def SetBoard(self):
        # Set each cell of the board to hold no. of bombs nearby
        for r in range(len(self.board)):
            for c in range(len(self.board)):

                if self.board[r][c].type == "B":
                    # Loop through each cell on the board until we get
                    # to a bomb, then increment all cells around it.

                    for row in (r-1, r, r+1):
                        if row < 0 or row >= len(self.board):
                            # Check row is within bounds
                            continue
                        for col in (c-1, c, c+1):
                            if col < 0 or col >= len(self.board):
                                # Check column is within bounds
                                continue
                            if row == r and col == c:
                                # This is the cell with the bomb
                                continue
                            if self.board[row][col].type == "B":
                                # If an adjacent cells is a bomb then skip
                                continue
                            self.board[row][col].type += 1

    def ClearEmpty(self, r, c):
        # When user selects a cell with a value of 0, we
        # reveal all cells around it. Those that are also
        # 0 will need to have the cells around it revealed too.
        for row in (r-1, r, r+1):  # Loop through rows around r
            if row < 0 or row >= len(self.board):
                # Check row is in bounds
                continue
            for col in (c-1, c, c+1):  # Loop through cols around c
                if col < 0 or col >= len(self.board):
                    # Check col is in bounds
                    continue
                if row == r and col == c:
                    # We will still land on original r,c so we need
                    # to skip it, but first make sure it's revealed.
                    self.RevealCell(row, col)
                    continue
                if self.board[row][col].reveal is True:
                    # If a cell is revealed then it was already checked
                    continue
                self.RevealCell(row, col)
                if self.board[row][col].type == 0:
                    # We only reveal surrounding cells for 0 cells.
                    self.ClearEmpty(row, col)

    def Select(self, r, c):
        if r < 0 or r >= len(self.board) or c < 0 or c >= len(self.board):
            # Check the r, c is within bounds
            return None

        if self.board[r][c].reveal is True:
            # If the cell has already been selected then return
            return None
        elif self.board[r][c].type == "B":
            # If a bomb is selected then reveal all the bombs
            self.bombReveal = True  # To mark the game as lost.
            for row in range(len(self.board)):
                for col in range(len(self.board)):
                    # Loop through whole board and reveal all bombs.
                    if self.board[row][col].type == "B":
                        self.board[row][col].reveal = True
        elif self.board[r][c].type > 0:
            # If number cell then reveal it
            self.RevealCell(r, c)
        elif self.board[r][c].type == 0:
            # If a 0 cell then need to reveal all surrounding cells
            self.ClearEmpty(r, c)

    def RevealCell(self, r, c):
        # If a cell han't already been revealed, reveal it,
        # reduce the total no. of cells to reveal, and switch
        # the flag to False in case it was on.
        if self.board[r][c].reveal is False:
            self.board[r][c].reveal = True
            self.total -= 1
            self.board[r][c].flag = False

    def SetFlag(self, r, c):
        # Toggles the cell's flag on or off
        if r < 0 or r >= len(self.board) or c < 0 or c >= len(self.board):
            # Check the r, c is within bounds
            return None

        if self.board[r][c].reveal is True:
            # If cell is already revealed then no need for flag
            return None

        self.board[r][c].flag = False if self.board[r][c].flag else True


class Cell:
    def __init__(self):
        # Bomb or next to a bomb? A 0 is neither.
        self.type = 0
        self.reveal = False
        self.flag = False
        self.col = {0: Fore.WHITE, 1: Fore.BLUE, 2: Fore.GREEN,
                    3: Fore.RED, 4: Fore.MAGENTA, 5: Fore.YELLOW,
                    6: Fore.CYAN, 7: Fore.CYAN, 8: Fore.CYAN,
                    "B": Fore.BLACK}
        # The colours used to represent the cells depending on
        # proximity to bombs.

    def __repr__(self):
        if self.reveal is False:
            if self.flag is True:
                return Back.BLACK + "F" + Back.RESET
            else:
                return "-"
        else:
            return self.col[self.type] + str(self.type) + Fore.RESET


if __name__ == "__main__":

    difficulty = 0
    while difficulty not in (1, 2, 3):
        difficulty = input("Difficulty (1, 2, 3): ")
        if difficulty.isdigit():
            difficulty = int(difficulty)
    print("")

    game = Game(difficulty)  # Initiate game object
    Flag = False  # toggled when needed to place flag

    while game.GameWin is None:
        select = input("Enter row and column as r, c: ").split("/")

        if select[0] == "f":
            # The user can change between revealing cells and
            # placing flags.
            Flag = False if Flag else True
            print("Flag is", Flag)
        elif len(select) >= 2 and all(i.isdigit() for i in select):
            select = list(map(int, select))
            if Flag is True:
                game.LayFlag(select[0], select[1])
            else:
                game.Select(select[0], select[1])

    if game.GameWin is True:
        print("Congratulations")
    elif game.GameWin is False:
        print("Game Over")
