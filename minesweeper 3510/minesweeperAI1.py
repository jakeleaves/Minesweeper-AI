import numpy as np
import random

class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def calculateSafeSquares(self, availableMoves, safeSquares):
        for row in range(self.numRows):
            for col in range(self.numCols):
                if availableMoves[row][col] == 1:
                    safeSquares.append((row, col))

    def unopenedNeighbors(self, boardState, unopenedNeighbors, row, col):
        if row != self.numRows - 1 and col != 0 and boardState[row][col - 1] == -1:
            unopenedNeighbors.append((row, col - 1))
        if row != self.numRows - 1 and boardState[row + 1][col] == -1:
            unopenedNeighbors.append((row + 1, col))
        if row != self.numRows - 1 and col != self.numCols - 1 and boardState[row + 1][col + 1] == -1:
            unopenedNeighbors.append((row + 1, col + 1))
        if col != 0 and boardState[row][col - 1] == -1:
            unopenedNeighbors.append((row, col - 1))
        if col != self.numCols - 1 and boardState[row][col + 1] == -1:
            unopenedNeighbors.append((row, col + 1))
        if row != 0 and col != 0 and boardState[row - 1][col - 1] == -1:
            unopenedNeighbors.append((row - 1, col - 1))
        if row != 0 and boardState[row - 1][col] == -1:
            unopenedNeighbors.append((row - 1, col))
        if row != 0 and col != self.numCols - 1 and boardState[row - 1][col + 1] == -1:
            unopenedNeighbors.append((row - 1, col + 1))
        return unopenedNeighbors

    def surroundingBombs(self, boardState, row, col, surroundingBombs):
        if row != self.numRows - 1 and col != 0 and boardState[row][col - 1] == 9:
            surroundingBombs.append((row + 1, col - 1))
        if row != self.numRows - 1 and boardState[row + 1][col] == 9:
            surroundingBombs.append((row + 1, col))
        if row != self.numRows - 1 and col != self.numCols - 1 and boardState[row + 1][col + 1] == 9:
            surroundingBombs.append((row + 1, col + 1))
        if col != 0 and boardState[row][col - 1] == 9:
            surroundingBombs.append((row, col - 1))
        if col != self.numCols - 1 and boardState[row][col + 1] == 9:
            surroundingBombs.append((row, col + 1))
        if row != 0 and col != 0 and boardState[row - 1][col - 1] == 9:
            surroundingBombs.append((row - 1, col - 1))
        if row != 0 and boardState[row - 1][col] == 9:
            surroundingBombs.append((row - 1, col))
        if row != 0 and col != self.numCols - 1 and boardState[row - 1][col + 1] == 9:
            surroundingBombs.append((row - 1, col + 1))
        return surroundingBombs

    def makeUnavailable(self, availableMoves, row, col):
        availableMoves[row][col] = 0
        if row != self.numRows - 1 and col != 0:
            availableMoves[row + 1][col - 1] = 0
        if row != self.numRows - 1:
            availableMoves[row + 1][col] = 0
        if row != self.numRows - 1 and col != self.numCols - 1:
            availableMoves[row + 1][col + 1] = 0
        if col != 0:
            availableMoves[row][col - 1] = 0
        if col != self.numCols - 1:
            availableMoves[row][col + 1] = 0
        if row != 0 and col != 0:
            availableMoves[row - 1][col - 1] = 0
        if row != 0:
            availableMoves[row - 1][col] = 0
        if row != 0 and col != self.numCols - 1:
            availableMoves[row - 1][col + 1] = 0
        return availableMoves

    def specialCase(self, boardState, bombsFoundSoFar, availableMoves, row, col):
        centerNum = boardState[row][col]
        unopenedNeighbors = []
        surroundingBombs = []
        # if the number on the square - surrounding bombs = the number of available squares,
        # then all the remaining available squares are bombs
        # add those squares to bombsFoundSoFar
        # self.surroundingBombs(boardState, row, col, surroundingBombs)
        # self.unopenedNeighbors(boardState, unopenedNeighbors, row, col)
        #
        if centerNum - len(surroundingBombs) == len(unopenedNeighbors):
            for i in range(len(unopenedNeighbors)):
                bombsFoundSoFar.append(unopenedNeighbors[i])
            self.makeUnavailable(availableMoves, row, col)
        # if the number on the square is equal to the number of surrounding bombs,
        # then all of the remaining squares are non bombs
        # make them unavailable to open
        if centerNum == len(surroundingBombs):
            self.makeUnavailable(availableMoves, row, col)
        return bombsFoundSoFar

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState):
        print(boardState)
        # find all the unopened squares
        unopenedSquares = []
        safeSquares = []
        bombsFoundSoFar = []

        # all squares are available at the beginning, make a 2d array of available moves
        availableMoves = [[1] * self.numCols for i in range(self.numRows)]

        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == -1:
                    unopenedSquares.append((row, col))
                if boardState[row][col] == 0:
                    self.makeUnavailable(availableMoves, row, col)
                if 0 < boardState[row][col] < 8:
                    self.specialCase(boardState, bombsFoundSoFar, availableMoves, row, col)
                if boardState[row][col] == 9:
                    bombsFoundSoFar.append((row, col))
                    availableMoves[row][col] = 0

        self.calculateSafeSquares(availableMoves, safeSquares)

        if len(bombsFoundSoFar) == self.numBombs:
            # If the number of unopened squares is equal to the number of bombs, all squares must be bombs, and we can submit our answer
            print(f"List of bombs is {bombsFoundSoFar}")
            return self.submit_final_answer_format(bombsFoundSoFar)
        else:
            if safeSquares is None:
                squareToOpen = random.choice(unopenedSquares)
            else:
                squareToOpen = random.choice(safeSquares)
            print(f"Square to open is {squareToOpen}")

            # Otherwise, pick a random square and open it
            return self.open_square_format(squareToOpen)

