from locale import currency
from django.shortcuts import render

def validator(board, i, j, value):
    #Check current row
    for x in range(9):
        if board[i][x] == value:
            return False

    #Check current column
    for x in range(9):
        if board[x][j] == value:
            return False
    
    #Check Current sub-grid
    start_row = (i // 3) * 3
    start_col = (j // 3) * 3
    for x in range(start_row, start_row + 3):
        for y in range(start_col, start_col + 3):
            if board[x][y] == value:
                return False
    
    return True

def validate_initial(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] not in range(0,10):
                return False
            if board[i][j] != 0:
                currVal = board[i][j]
                board[i][j] = 0
                if not validator(board, i, j, currVal):
                    return False
                board[i][j] = currVal
    return True

def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for possibleval in range(1,10):
                    if validator(board, i, j, possibleval):
                        board[i][j] = possibleval
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True