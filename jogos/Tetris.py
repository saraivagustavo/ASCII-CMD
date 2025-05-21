# Reference: https://github.com/ravi-ojha/Terminal-Tetris/blob/master/play_tetris.py

import os
import random
from colorama import Fore, Style
from copy import deepcopy
from keyboard import is_pressed
from time import sleep, time

BOARD_SIZE = 30
EFF_BOARD_SIZE = BOARD_SIZE + 2

# Delayed Auto Shift
DAS = 0.3

BOARD_CHR = "█"
PIECE_CHR = "█"
FILL_CHR = " "


PIECES = [
    [[2], [2], [2], [2]],

    [[3, 0],
     [3, 0],
     [3, 3]],

    [[0, 4],
     [0, 4],
     [4, 4]],

    [[5, 5],
     [5, 5]],

    [[0, 6, 0],
     [6, 6, 6]],

    [[0, 7],
     [7, 7],
     [7, 0]],
]

GHOST = -1
GHOST_COLOR = Fore.LIGHTBLACK_EX
BOARD_COLOR = Fore.BLUE
COLORS = [
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.LIGHTBLUE_EX,
    Fore.MAGENTA,
    Fore.CYAN
]

# Constants for user input
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right' 
ROTATE_ANTICLOCKWISE = 'z'
ROTATE_CLOCKWISE = 'x'
QUIT_GAME = 'q'

def print_board(board, pieces: (tuple, ...)):
    board_copy = deepcopy(board)

    for piece in pieces:
        curr_piece, piece_pos = piece
        curr_piece_size_x = len(curr_piece)
        curr_piece_size_y = len(curr_piece[0])
        for i in range(curr_piece_size_x):
            for j in range(curr_piece_size_y):
                board_copy[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | board[piece_pos[0]+i][piece_pos[1]+j]

    for i in range(EFF_BOARD_SIZE):
        for j in range(EFF_BOARD_SIZE):
            if board_copy[i][j] == 1:
                print(f"{BOARD_COLOR}{BOARD_CHR}", end='')
            elif board_copy[i][j] > 1:
                print(f"{COLORS[board_copy[i][j] - 2]}{PIECE_CHR}", end='')
            elif board_copy[i][j] == -1:
                print(f"{GHOST_COLOR}{PIECE_CHR}", end='')
            else:
                print(FILL_CHR, end='')
        print('')


def init_board():
    board = [[0 for x in range(EFF_BOARD_SIZE)] for y in range(EFF_BOARD_SIZE)]

    for i in range(EFF_BOARD_SIZE):
        board[i][0] = 1
        board[EFF_BOARD_SIZE-1][i] = 1
        board[i][EFF_BOARD_SIZE-1] = 1
        board[0][i] = 1
    return board


def get_random_piece():
    idx = random.randrange(len(PIECES))
    return PIECES[idx]


def get_random_position(curr_piece):
    curr_piece_size = len(curr_piece)

    i = 1
    j = random.randrange(1, EFF_BOARD_SIZE-curr_piece_size-1)
    return [i, j]


def is_game_over(board, curr_piece, piece_pos):
    if not can_move_down(board, curr_piece, piece_pos) and piece_pos[0] == 1:
        return True
    return False


def get_left_move(piece_pos, unit = 1):
    new_piece_pos = [piece_pos[0], piece_pos[1] - unit]
    return new_piece_pos


def get_right_move(piece_pos, unit=1):
    new_piece_pos = [piece_pos[0], piece_pos[1] + unit]
    return new_piece_pos


def get_down_move(piece_pos, unit=1):
    new_piece_pos = [piece_pos[0] + unit, piece_pos[1]]
    return new_piece_pos


def rotate_clockwise(piece):
    piece_copy = deepcopy(piece)
    reverse_piece = piece_copy[::-1]
    return list(list(elem) for elem in zip(*reverse_piece))


def rotate_anticlockwise(piece):
    piece_copy = deepcopy(piece)
    piece_1 = rotate_clockwise(piece_copy)
    piece_2 = rotate_clockwise(piece_1)
    return rotate_clockwise(piece_2)


def merge_board_and_piece(board, curr_piece, piece_pos):
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])
    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            board[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | board[piece_pos[0]+i][piece_pos[1]+j]


def remove_filled_rows(board):
    empty_row = [0]*EFF_BOARD_SIZE
    empty_row[0] = 1
    empty_row[EFF_BOARD_SIZE-1] = 1

    filled_row = [1]*EFF_BOARD_SIZE

    rows_to_remove = []
    for row in board[1:EFF_BOARD_SIZE-1]:
        if list(map(lambda i: int(i>0), row)) == filled_row:
            rows_to_remove.append(row)

    for row in rows_to_remove:
        if row in board:
            board.remove(row)

    for i in range(len(rows_to_remove)):
        board.insert(0, empty_row)


def overlap_check(board, curr_piece, piece_pos):
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])
    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            if board[piece_pos[0]+i][piece_pos[1]+j] >= 1 and curr_piece[i][j] >= 1:
                return False    
    return True


def can_move_left(board, curr_piece, piece_pos, unit=1):
    piece_pos = get_left_move(piece_pos, unit)
    return overlap_check(board, curr_piece, piece_pos)


def can_move_right(board, curr_piece, piece_pos, unit=1):
    piece_pos = get_right_move(piece_pos, unit)
    return overlap_check(board, curr_piece, piece_pos)


def can_move_down(board, curr_piece, piece_pos, unit=1):
    piece_pos = get_down_move(piece_pos, unit)
    return overlap_check(board, curr_piece, piece_pos)


def can_rotate_anticlockwise(board, curr_piece, piece_pos):
    curr_piece = rotate_anticlockwise(curr_piece)
    return overlap_check(board, curr_piece, piece_pos)


def can_rotate_clockwise(board, curr_piece, piece_pos):
    curr_piece = rotate_clockwise(curr_piece)
    return overlap_check(board, curr_piece, piece_pos)


def soft_drop(board, curr_piece, piece_pos):
    if can_move_down(board, curr_piece, piece_pos):
        piece_pos = get_down_move(piece_pos)
    return piece_pos


def hard_drop(board, curr_piece, piece_pos):
    while can_move_down(board, curr_piece, piece_pos):
        piece_pos = get_down_move(piece_pos)
    return piece_pos

def ghost_piece(board, curr_piece, piece_pos):
    curr_copy = deepcopy(curr_piece)
    for i in range(len(curr_piece)):
        for j in range(len(curr_piece[0])):
            if curr_copy[i][j] != 0:
                curr_copy[i][j] = GHOST     

    return curr_copy, hard_drop(board, curr_piece, piece_pos)

def play_game():
    board = init_board()
    curr_piece = get_random_piece()
    piece_pos = get_random_position(curr_piece)
    print_board(
        board, 
        pieces=((curr_piece, piece_pos),)
    )

    print(f"{Fore.RESET}Quick play instructions:\n")
    print(f" {MOVE_LEFT}: move piece left")
    print(f" {MOVE_RIGHT}: move piece right")
    print(f" {ROTATE_ANTICLOCKWISE}: rotate piece counter clockwise")
    print(f" {ROTATE_CLOCKWISE}: rotate piece clockwise")
    print(f" {QUIT_GAME}: to quit the game anytime")
    input("\nPress 'enter' to start")

    vel = 0.2
    while (not is_game_over(board, curr_piece, piece_pos)):
    
        if is_pressed(MOVE_LEFT):
            if can_move_left(board, curr_piece, piece_pos):
                piece_pos = get_left_move(piece_pos)

        if is_pressed(MOVE_RIGHT):
            if can_move_right(board, curr_piece, piece_pos):
                piece_pos = get_right_move(piece_pos)

        if is_pressed(ROTATE_ANTICLOCKWISE):
            if can_rotate_anticlockwise(board, curr_piece, piece_pos):
                curr_piece = rotate_anticlockwise(curr_piece)

        if is_pressed(ROTATE_CLOCKWISE) or is_pressed('up'):
            if can_rotate_clockwise(board, curr_piece, piece_pos):
                curr_piece = rotate_clockwise(curr_piece)

        if is_pressed('space'):
            piece_pos = hard_drop(board, curr_piece, piece_pos)

        if is_pressed('down'):
            piece_pos = soft_drop(board, curr_piece, piece_pos)

        if is_pressed(QUIT_GAME):
            print("Bye. Thank you for playing!")
            return

        if can_move_down(board, curr_piece, piece_pos):
            piece_pos = get_down_move(piece_pos)
            start = time()

        else:
            if (time() - start) > DAS:
                merge_board_and_piece(board, curr_piece, piece_pos)
                remove_filled_rows(board)
                curr_piece = get_random_piece()
                piece_pos = get_random_position(curr_piece)
        
        curr_ghost, ghost_pos = ghost_piece(board, curr_piece, piece_pos)

        os.system('cls')
        print_board(
            board, 
            pieces=((curr_ghost, ghost_pos), (curr_piece, piece_pos))
        )

        vel = max(0.0001, vel-0.0001)
        sleep(vel)

    print("GAME OVER!")


if __name__ == "__main__":
    try:
        play_game()
    except (KeyboardInterrupt) as e:
        print(Fore.RESET, Style.RESET_ALL, e)
    print(Fore.RESET, Style.RESET_ALL)
