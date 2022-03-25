![Tests](https://github.com/RyMaDe/Command-Line-Minesweeper/actions/workflows/tests.yml/badge.svg)
# Command Line Minesweeper
A basic minesweeper game played on command line prompt.

## Instructions
When starting, you must first select the difficulty which corresponds to the gridsize:

> 1 - 10x10

> 2 - 15x15

> 3 - 20x20

Once a difficulty is selected, the board appears and you can begin selecting a cell. You select a cell in the following format:

    5/7

This is row 5, column 7. Seperated by a slash (/) and no spaces.

### Flags
Just like in the normal game, you can lay flags on suspected bombs.

When selecting a cell, instead type **"f"** and hit enter. You can then begin selecting cells to flag. To unflag a cell, just select that cell again.

When you're finished laying flags just type **"f"** again and hit enter. You can now go back to selecting cells, including cells where a flag was layed.