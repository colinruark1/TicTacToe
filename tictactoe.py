"""
Tic Tac Toe Player
"""

import math
from random import random

X = "X"
O = "O"
EMPTY = None

#Class defining coordinates used in the game
class Coords:
    def __init__(self, x, y):
        self.xC = x
        self.yC = y

    def getX(self):
        return self.xC

    def getY(self):
        return self.yC


#sets the initial state of the board, that being 9 empty squares.
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    numX = 0
    numO = 0
    #determining turn by adding up all X's and O's, seeing if there are more X's than O's
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                numX = numX + 1
            elif board[i][j] == O:
                numO = numO + 1
    if numX > numO:
        return O
    else:
        return X


#defines all possible actions for either X or O on any given board state
def actions(board):
    actionS = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actionS += [Coords(i, j)]
    return actionS

#determines what the board state will become after a player makes a specific move
def result(board, action):
    if(type(action) == tuple):
        first, last = action[0], action[1]
    else:
        first, last = Coords.getX(action), Coords.getY(action)
    res = [[EMPTY]*3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            res[i][j] = board[i][j]
    try:
        if board[first][last] != EMPTY:
            raise BoardError
    except BoardError:
        print("Invalid Move. Please try again.")
    res[first][last] = player(board)
    return res

#through a somewhat repetitive process, determines if someone has gotten three in a row, anywhere on the board.
def winner(board):
    three = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                three += 1
        if three == 3:
            return X
        three = 0
    for i in range(3):
        for j in range(3):
            if board[j][i] == X:
                three += 1
        if three == 3:
            return X
        three = 0
    for i in range(3):
        if board[i][i] == X:
            three += 1
    if three == 3:
        return X
    three = 0
    for i in range(3):
        if board[i][2-i] == X:
            three += 1
    if three == 3:
        return X
    three = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == O:
                three += 1
        if three == 3:
            return O
        three = 0
    for i in range(3):
        for j in range(3):
            if board[j][i] == O:
                three += 1
        if three == 3:
            return O
        three = 0
    for i in range(3):
        if board[i][i] == O:
            three += 1
    if three == 3:
        return O
    three = 0
    for i in range(3):
        if board[i][2-i] == O:
            three += 1
    if three == 3:
        return O
    return None

#determines if the game has ended, based on if X/O has won.
def terminal(board):
    if winner(board) != None:
        return True
    gameOver = True
    for i in range(9):
        if board[i // 3][i % 3] == EMPTY:
            gameOver = False
    return gameOver

#gives the engine a definitive value for winning/losing. This is essential to minimax searching
def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def Search(board, n, alpha, beta, isMaximizing):
    if terminal(board) or n == 0: #considered the "terminal state", as this is a recursion algorithm.
        return utility(board) #Determines if the theoretical branch was a win, loss, or draw.

    if(isMaximizing):
        moves = actions(board)
        best = -1 * 1000000000
        for move in moves:
            #finds all moves and evaluates them to the furthest depth recursively.
            #finds the move with the highest value and plays it.
            eval = Search(result(board, move), n - 1, alpha, beta, False)
            best = max(eval, best)
            alpha = max(eval, alpha)
            if(beta <= alpha):
                break
                #Alpha-Beta Pruning:
                #If a search of a deeper branch turns out to be worse, in every variation,
                #then something already found, stops exploring that branch
    else: #does the same thing but for the opposing side.
        moves = actions(board)
        best = 1000000000
        for move in moves:
            eval = Search(result(board, move), n - 1, alpha, beta, True)
            best = min(eval, best)
            beta = min(eval, beta)
            if(beta <= alpha):
                break
    return best


def minimax(board):
    moves = actions(board)
    if(player(board) == O):
        best = 100000
        bestMove = None
        for move in moves:
            #recursively searches for each possible initial move until it finds one with a higher value
            eval = Search(result(board, move), 9, -1000000, 1000000, True)
            if (eval < best):
                best = eval
                bestMove = move
        print("FINAL:", best)
        return bestMove
    else:
        #Does the same thing for when the computer is playing X's
        worst = -100000
        worstMove = None
        for move in moves:
            eval = Search(result(board, move), 9, -1000000, 1000000, False)
            if (eval > worst):
                worst = eval
                worstMove = move
        return worstMove
