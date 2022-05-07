import numpy as np
import random

class AI2():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

        '''OUR CODE'''
        self.bombStatus = np.full((self.numRows, self.numCols), -1)
        self.probBoard = np.full((self.numRows, self.numCols), -2)
        self.totalBombs = self.numBombs
        '''OUR CODE'''

    def open_square_format(self, squaresToOpen): #CHANGED THIS HEADER AND METHOD 
        opened = []
        for x in squaresToOpen:
            opened.append(("open_square", x))

        return opened  
        # return ("open_square", squaresToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    # TODO: implement a better algorithm
    def performAI(self, boardState, safeSquare, gridInput):

        covered = self.readBoard()
        bombsFoundSoFar = []

        ''' OUR CODE '''
        print("starting our algorithm")
        print(self.bombStatus)
        print(self.probBoard)
        print("number of bombs we are looking for in this game: ")
        print(self.numBombs)

        squaresOpened = []
            
        gi = np.full((self.numRows, self.numCols), -1)
        i = 0
        for r in range(self.numRows): 
            for c in range(self.numCols): 
                gi[r][c] = gridInput[i]
                i = i + 1

        gridInput = gi
             
        # handle safe square first  
        covered.remove((safeSquare[0], safeSquare[1]))
        self.probBoard[safeSquare[0]][safeSquare[1]] = 0 
        self.bombStatus[safeSquare[0]][safeSquare[1]] = 0
        c = gridInput[safeSquare[0]][safeSquare[1]]
        cLoc = (safeSquare[0], safeSquare[1])
        squaresOpened.append(cLoc)
        #solve center square and it's neighbors 
        squaresOpened, bombsFoundSoFar, covered = self.solveC(c, cLoc, covered, bombsFoundSoFar, gridInput, squaresOpened)

        #now handle the rest 
        while (len(bombsFoundSoFar) != self.numBombs): 
            # select next square to uncover and solve based on square with highest probability on board 
            [c, cLoc] = self.nextLocation(covered, gridInput)
            covered.remove((cLoc[0], cLoc[1])) #remove location we just uncovered
            
            #solve center square and it's neighbors 
            squaresOpened, bombsFoundSoFar, covered = self.solveC(c, cLoc, covered, bombsFoundSoFar, gridInput, squaresOpened)
            squaresOpened.append(cLoc)
        
        if len(bombsFoundSoFar) == self.numBombs:
            print(f"List of bombs is {bombsFoundSoFar}")
            firstReturn = self.open_square_format(squaresOpened)
            secondReturn = self.submit_final_answer_format(bombsFoundSoFar)
            return firstReturn, secondReturn    
        else: 
            print("unable to solve")
            return 
        ''' OUR CODE '''


    def solveC(self, center, cLoc, covered, bombsFoundSoFar, gridInput, squaresOpened):

        neighbors = self.getNeighbors(cLoc)
        ogNeighbors = self.getNeighbors(cLoc)
        coveredNeighbors, cnNum = self.getCoveredNeighbors(neighbors, covered)
        bombNeighbors, bnNum = self.getBombNeighbors(neighbors, bombsFoundSoFar)

        #check special cases 
        if center == 9: 
            bombsFoundSoFar.append(cLoc)
            self.probBoard[cLoc[0]][cLoc[1]] = -1
            self.bombStatus[cLoc[0]][cLoc[1]] = 1
            self.totalBombs = self.totalBombs - 1
            bombsToFind = 0
        elif center == 0:
            for n in neighbors: 
                self.setProb(n, 0)
                self.setBombStatus(n, 0)
            bombsToFind = center 
        elif center == (cnNum- bnNum): 
            for cn in coveredNeighbors: 
                self.setBombStatus(cn, 1)
                self.setProb(cn, -1)
            bombsToFind = 0 
        elif center - bnNum == 0 : #this location can already be solved without openeing any neighbors
            #all remaining neighbors not bombs  
            for cn in coveredNeighbors: 
                self.setBombStatus(cn, 0)
                self.setProb(cn, 0)
            bombsToFind = 0     
        else: 
            bombsToFind = center - bnNum
            #initalize all covered square probabilities
            self.initalizeProbs(coveredNeighbors, center)

        #general cases
        while (bombsToFind != 0):
            #reGET covered neighbors and bombNeighbors 
            coveredNeighbors, cnNum = self.getCoveredNeighbors(neighbors, covered)
            bombNeighbors, bnNum = self.getBombNeighbors(neighbors, bombsFoundSoFar) 

            #pick next location
            hp, hpLoc = self.findhpNeighbor(coveredNeighbors, gridInput) 
            self.updateUncovered(hp, hpLoc)
            squaresOpened.append(hpLoc)
            covered.remove((hpLoc[0], hpLoc[1])) #remove location we just uncovered 
            # Window.open_button(hpLoc[0], hpLoc[1])

            #update hp neighbors 
            hpNeighbors, hpcnNum = self.getCoveredNeighbors(self.getNeighbors(hpLoc), covered)
            if hp == 0: 
                for x in hpNeighbors: 
                    self.setProb(x,0)
                    self.setBombStatus(x,0)
            elif hp == 9:
                bombsFoundSoFar.append(hpLoc)
                self.totalBombs = self.totalBombs - 1
                bombsToFind = bombsToFind - 1 #decrease number of bombs to find 

                ogcoveredNeighbors, ogcnNum = self.getCoveredNeighbors(ogNeighbors, covered)
                ogbombNeighbors, ogbnNum = self.getBombNeighbors(ogNeighbors, bombsFoundSoFar)
                for n in ogcoveredNeighbors: 
                    prevProb = self.probBoard[n[0]][n[1]]
                    if (prevProb - 1) >= 0: 
                        self.setProb(n, prevProb-1) #decrease neighbors bombProb by 1 
                    else: 
                        self.setProb(n, 0) #make sure not to set it below 0
                # for n in hpNeighbors: 
                #     prevProb = self.probBoard[n[0]][n[1]]
                #     if (prevProb - 1) >= 0: 
                #         self.setProb(n, prevProb-1) #decrease neighbors bombProb by 1 
                #     else: 
                #         self.setProb(n, 0) #make sure not to set it below 0
            else:
                hpBombNeighbors, hpbnNum = self.getBombNeighbors(self.getNeighbors(hpLoc), bombsFoundSoFar)
                for n in hpNeighbors: 
                    val = hp - hpbnNum
                    prevProb = self.probBoard[n[0]][n[1]]
                    self.setProb(n, prevProb+val)

        #HAVE SOLVED CENTER AND IT'S NEIGHBORS 
        coveredNeighbors, cnNum = self.getCoveredNeighbors(neighbors, covered) #reGET covered neighbors
        for cn in coveredNeighbors: #bc remaining covered neighbors can't be bombs bc all bombs found 
            self.setProb(cn, 0)
            self.setBombStatus(cn, 0)
        return squaresOpened, bombsFoundSoFar, covered

                
    
    ''' 
    NEXT LOCATION HELPER FUNCTION
    this function picks the next location to uncover based 
    off of which square on the board has the HIGHEST PROBABILITY
    ''' 
    def nextLocation(self, covered, gridInput):
        currMax = -10
        maxLoc = []
        value = 0
        holdProbs = []

        for row in range(self.numRows): 
            for col in range(self.numCols):
                if self.probBoard[row][col] > currMax:
                    if (row,col) in covered:  
                        holdProbs = []
                        currMax = self.probBoard[row][col]
                        maxLoc = (row,col)
                        value = gridInput[row][col]
                        holdProbs.append([value, maxLoc])
                elif self.probBoard[row][col] == currMax: 
                    if (row,col) in covered:  
                        maxLoc = (row,col)
                        value = gridInput[row][col]
                        holdProbs.append([value, maxLoc])

        [value, maxLoc] = random.choice(holdProbs)
        
        return [value, maxLoc]
        
    ''' 
    GET NEIGHBORS HELPER FUNCTION 
    returns all neighbors of current square location passed in 
    ''' 
    def getNeighbors(self, cLoc): 
        r = cLoc[0]
        c = cLoc[1]
        neighbors = []

        #top
        if self.squareInBounds(r-1, c):
            neighbors.append((r-1, c)) 
        #top-right 
        if self.squareInBounds(r-1, c+1):
            neighbors.append((r-1, c+1)) 
        #right 
        if self.squareInBounds(r, c+1):
            neighbors.append((r, c+1)) 
        #bottom-right
        if self.squareInBounds(r+1, c+1):
            neighbors.append((r+1, c+1))  
        #bottom
        if self.squareInBounds(r+1, c):
            neighbors.append((r+1, c))  
        #bottom-left
        if self.squareInBounds(r+1, c-1):
            neighbors.append((r+1, c-1)) 
        #left
        if self.squareInBounds(r, c-1):
            neighbors.append((r, c-1))  
        #top-left
        if self.squareInBounds(r-1, c-1):
            neighbors.append((r-1, c-1)) 

        return neighbors
     

    ''' 
    SET PROBABILITY HELPER FUNCTION 
    sets probability of given location to given value 
    '''
    def setProb(self, loc, value): 
        if ((self.probBoard[loc[0]][loc[1]] != 0) or (self.probBoard[loc[0]][loc[1]] != -1)): 
            self.probBoard[loc[0]][loc[1]] = value

    ''' 
    SET BOMB STATUS HELPER FUNCTION 
    sets bomb status of given location to given value 
    '''
    def setBombStatus(self, loc, value): 
        if self.bombStatus[loc[0]][loc[1]] == -1:  
            self.bombStatus[loc[0]][loc[1]] = value

    ''' 
    GET COVERED NEIGHBORS HELPER FUNCTION 
    returns the location(s) and number of covered neighbors 
    '''
    def getCoveredNeighbors(self, neighbors, covered): 
        cn = []
        numOfcn = 0 

        for n in neighbors: 
            if n in covered: 
                cn.append(n)
                numOfcn += 1

        return cn, numOfcn

    ''' 
    GET BOMB NEIGHBORS HELPER FUNCTION 
    returns the location(s) and number of neighbors that are bombs  
    '''
    def getBombNeighbors(self, neighbors, bombsFoundSoFar): 
        bn = []
        numOfbn = 0 

        for n in neighbors: 
            if n in bombsFoundSoFar: 
                bn.append(n)
                numOfbn += 1

        return bn, numOfbn

    ''' 
    INITALIZE PROBABILITY OF ALL COVERED NEIGHBORS HELPER FUNCTION 
    initalized the probabilities of all the covered neighbors based off of center's value... duh
    '''
    def initalizeProbs(self, cn, value): 

        for c in cn:
            self.setProb(c, value)

    ''' 
    FINDS THE NEIGHBOR WITH THE HIGHEST PROBABILITY HELPER FUNCTION
    '''
    def findhpNeighbor(self, neighbors, gridInput): 
        currMax = -100
        maxLoc = []
        # hp = 0
        hp = []
        value = 0

        for n in neighbors: 
            if self.probBoard[n[0]][n[1]] > currMax: 
                hp = []
                currMax = self.probBoard[n[0]][n[1]]
                maxLoc = n
                value = gridInput[n[0], n[1]]
                hp.append([value, n])
            elif self.probBoard[n[0]][n[1]] == currMax: 
                value = gridInput[n[0], n[1]]
                hp.append([value, n])

        #pick randomly of neighbors with equally highest probability 
        [hp, maxLoc] = random.choice(hp) 

        return hp, maxLoc

    ''' 
    UPDATES THE PROB AND BOMB STATUS OF NEWLY UNCOVERED SQUARE 
    '''
    def updateUncovered(self, value, loc):
        if value == 9:
            self.setProb(loc, -1)
            self.setBombStatus(loc, 1) 
            # self.probBoard[loc[0]][loc[1]] = -1
            # self.bombStatus[loc[0]][loc[1]] = 1
        else: #not a bomb
            self.setProb(loc, 0)
            self.setBombStatus(loc, 0) 
            # self.probBoard[loc[0]][loc[1]] = 0
            # self.bombStatus[loc[0]][loc[1]] = 0

    ''' 
    RETURNS TRUE IF AND ONLY IF A SQUARE (R,C) IS WITHIN THE GAME GRID
    '''
    def squareInBounds(self, r, c):
        return r >= 0 and c >= 0 and r < self.numRows and c < self.numCols


    ''' 
    ANALYSES THE BOARD AND RETURNS COVERED SQUARE LOCATIONS AND BOMBS FOUND SO FAR LOCATIONS 
    '''
    def readBoard(self): 
        # find all the unopened squares
        covered = []
        bombsFoundSoFar = []

        for row in range(self.numRows):
            for col in range(self.numCols):
                if self.bombStatus[row][col] == -1: #EDITED THIS LINE 
                    covered.append((row, col))
                # elif boardState[row][col] == 9:
                #     bombsFoundSoFar.append((row, col))

        return covered
        
        









    
    




        
