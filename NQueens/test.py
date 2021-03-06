import pygame 
from pygame.locals import * 
import time 
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_PINK = (255, 110, 151)
LIGHT_PINK = (241, 170, 166)
DARK_PINK = (255, 110, 151)
LENGTH_UNIT = 40


class NQueens(object):
    def __init__(self, n):
        self.n = n
        self.isFound = False
        self.matrix = [[0 for i in range(n)] for j in range(n)]

        # pygame.init()
        self.clock = pygame.time.Clock()
        SCREEN = [self.n * LENGTH_UNIT, self.n * LENGTH_UNIT]
        self.screen = pygame.display.set_mode(SCREEN)
        self.screen.fill(WHITE)
        self.initScreen()

        self.colVector = [0 for i in range(self.n)]
        self.rowVector = [0 for i in range(self.n)]
        self.pDiagVector = [0 for i in range(self.n*2 - 1)]
        self.cDiagVector = [0 for i in range(self.n*2 - 1)]

    def printMatrix(self):
        for i in self.matrix:
            print(i)

    def getpDiagVectorIdx(self, row, col):
        return row + col 
    def getcDiagVectorIdx(self, row, col):
        return col - row + self.n - 1
    def calcuConflict(self, row, col):
        return self.colVector[col] + self.pDiagVector[self.getpDiagVectorIdx(row, col)] + self.cDiagVector[self.getcDiagVectorIdx(row, col)]
    def checkStatus(self):
        if 0 in self.colVector:
            return False
        for i in self.pDiagVector:
            if i != 0 and i != 1:
                return False
        for i in self.cDiagVector:
            if i != 0 and i != 1:
                return False
        return True

    def initMatrix(self):
        for row in range(self.n):
            col = random.randint(0, self.n-1)
            while col < self.n and self.colVector[col] == 1:
                col = random.randint(0, self.n-1)
            self.colVector[col] = 1
            self.rowVector[row] = col
            self.matrix[row][col] = 1
            self.pDiagVector[ self.getpDiagVectorIdx(row, col)] += 1
            self.cDiagVector[ self.getcDiagVectorIdx(row, col)] += 1

    def updateMatrix(self):
        iCount = 0
        while not self.checkStatus():
            # print("iteraion: %d" % iCount)
            iCount += 1

            # print(self.matrix)
            # time.sleep(1)
            for iRow in range(self.n):
                col = self.rowVector[iRow]
                self.rowVector[iRow] = -1
                self.matrix[iRow][col] = 0
                

                self.colVector[col] -= 1
                if self.pDiagVector[self.getpDiagVectorIdx(iRow, col)] > 0:
                    self.pDiagVector[self.getpDiagVectorIdx(iRow, col)] -= 1
                if self.cDiagVector[self.getcDiagVectorIdx(iRow, col)] > 0:
                    self.cDiagVector[self.getcDiagVectorIdx(iRow, col)] -= 1

                minConflict = self.calcuConflict(iRow, col)
                betterCol = col
                for iCol in range(self.n):
                    if self.calcuConflict(iRow, iCol) < minConflict:
                        minConflict = self.calcuConflict(iRow, iCol)
                        betterCol = iCol 
                    elif self.calcuConflict(iRow, iCol) == minConflict:
                        if random.randint(0, 1) == 1:
                            minConflict = self.calcuConflict(iRow, iCol)
                            betterCol = iCol

                col = betterCol
                self.rowVector[iRow] = col
                self.matrix[iRow][col] = 1
                self.colVector[col] += 1
                self.pDiagVector[self.getpDiagVectorIdx(iRow, col)] += 1
                self.cDiagVector[self.getcDiagVectorIdx(iRow, col)] += 1

        # self.printMatrix()
        print("iteraion: %d" % iCount)
 
    def useLeastConflict(self):
        self.initMatrix()
        self.updateMatrix()


    def evalue(self, level):
        iCount = 0
        for iCol in range(self.n):
            for iRow in range(level):
                pos = self.matrix[iRow].index(1)
                if(iCol != pos and iCol - pos != level - iRow and pos - iCol != level - iRow):
                    iCount += 1
        return iCount

    def DFS(self, level):
        if level == self.n:
            self.isFound = True
            time.sleep(5)
            return
        else:
            tmpArray = [0 for col in range(self.n)]
            for col in range(self.n):
                flag = True
                for row in range(level):
                    # print(level)
                    pos = self.matrix[row].index(1)
                    if(col == pos or col-pos == level-row or pos-col == level-row):
                        flag = False
                        break
                if flag:
                    # tmpArray[col] = evalue(level , col)
                    self.matrix[level][col] = 1
                    tmpArray[col] = evalue(level+1)
                    self.matrix[level][col] = 0

            while max(tmpArray) > 0:
                # print(level,  tmpArray)
                col = tmpArray.index(max(tmpArray))
                self.matrix[level][col] = 1
                self.drawGrid(level, col)
                self.DFS(level+1)
                tmpArray[col] = 0
                if self.isFound:
                    return
                self.matrix[level][col] = 0
                self.resetGrid(level, col)
       
    def initScreen(self):
        pygame.font.init()
        pygame.display.set_caption("NQueens")
        self.drawLines()
        pygame.display.update()      

    def drawLines(self):
        for raw_index in range(1, self.n):
            pygame.draw.line(self.screen, GRAY, (0, raw_index * LENGTH_UNIT), (self.n * LENGTH_UNIT, raw_index * LENGTH_UNIT), 2)
        for col_index in range(1, self.n):
            pygame.draw.line(self.screen, GRAY, (col_index * LENGTH_UNIT, 0), (col_index * LENGTH_UNIT, self.n * LENGTH_UNIT), 2)

    def drawGrid(self, raw, col):
        pygame.draw.rect(self.screen, DARK_PINK, [raw*LENGTH_UNIT,col*LENGTH_UNIT, LENGTH_UNIT, LENGTH_UNIT])
        self.drawLines()
        pygame.display.update()
    def resetGrid(self, raw, col):
        pygame.draw.rect(self.screen, WHITE, [raw*LENGTH_UNIT,col*LENGTH_UNIT, LENGTH_UNIT, LENGTH_UNIT])
        self.drawLines()
        pygame.display.update()


          
    
if __name__ == '__main__':
    nQueens = NQueens(1000)
    # nQueens.DFS(0)
    t = time.clock()
    # nQueens.useLeastConflict()
    # nQueens.DFS(0)
    print("time cost: ", time.clock() - t)
    # nQueens.printMatrix()
    