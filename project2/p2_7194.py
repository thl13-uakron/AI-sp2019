"""
Program written by Thomas Li <thl13@zips.uakron.edu> on 20 Sep 2019
"""

import random

# player ids
_empty = 0
_p1 = 1
_p2 = 10

# game mode ids
_pvp = 0
_beginner = 1
_expert = 2

# helper functions
def get_opponent(player):
    return _p1 if player == _p2 else _p2 if player == _p1 else None

def get_marker(player):
    return "X" if player == _p2 else "O" if player == _p1 else " "

# board functions
def make_board(num_rows):
    return ["board"] + [0 for i in range(num_rows ** 2)]

def get_num_rows(board):
    return int(len(board) ** 0.5)

def get_rows(board):
    num_rows = get_num_rows(board)
    return [tuple([j for j in range(i, i + num_rows, 1)]) for i in range(1, len(board), num_rows)]

def get_columns(board):
    num_rows = get_num_rows(board)
    return [tuple([j for j in range(i, len(board), num_rows)]) for i in range(1, num_rows + 1, 1)]

def get_diagonals(board):
    num_rows = get_num_rows(board)
    return [tuple([j for j in range(1, len(board), num_rows + 1)]),
            tuple([k for k in range(num_rows, len(board) - 1, num_rows - 1)])]

def print_row(board, row):
    output = "|"
    for pos in row:
        output = output + " " + get_marker(board[pos]) + " |"
    print(output)
    
def print_board(board):
    num_rows = get_num_rows(board)
    divider = "-" * (num_rows * 5 - (num_rows - 1))
    print(divider)
    [[print_row(board, r), print(divider)] for r in get_rows(board)]

# state space
def get_available_moves(board):
    return [i for i in range(len(board)) if board[i] == _empty]

def get_win_states(board):
    # combinations of positions that will result in winning if occupied by any single player
    return get_rows(board) + get_columns(board) + get_diagonals(board)

def get_win_paths(player, board):
    # combinations of open postions that the current player would need to occupy to reach a win state
    # given the current state of the game
    paths = get_win_states(board)
    paths = [path for path in paths if get_opponent(player) not in [board[pos] for pos in path]]
    paths = [tuple([pos for pos in path if board[pos] is _empty]) for path in paths]
    return paths

# end game
def get_winner(board):
    # return player id if player meets winning condition
    # return none if neither player wins
    num_rows = get_num_rows(board)
    win_states = get_win_states(board)
    state_scores = [sum([board[pos] for pos in state]) for state in win_states]
    return _p1 if num_rows * _p1 in state_scores else _p2 if num_rows * _p2 in state_scores else None

# moving
def choose_player_move(player, board):
    pos = input("\nChoose a position to occupy: ")
    
    try:
        pos = int(pos)
    except ValueError:
        print("Invalid position. Please try again.")
    
    if pos in get_available_moves(board):
        return (pos, "player move")
                    
    if pos in range(1, len(board)):
        print("Position occupied. Please try again.")
    else:
        print("Invalid position. Please try again.")
        
    return choose_player_move(player, board)

def choose_beginner_move(player, board):
    # pick move randomly
    return (random.choice(get_available_moves(board)), "random move")

def choose_expert_move(player, board):
    # heuristic search for best move
    # all open positions start with score zero
    # each win path on either side that includes the position increases its score
    # shorter win paths are checked first, longer paths are only checked if there is a tie
    win_paths = get_win_paths(player, board) + get_win_paths(get_opponent(player), board)
    pos = p for p in path for path in win_paths in len(path) == 1
    if not pos:
        pos = random.choice(get_available_moves(board))
    return (pos, "heuristic-based move")

def choose_p2_move(player, board, mode):
    if mode is _pvp:
        return choose_player_move(player, board)
    if mode is _beginner:
        return choose_beginner_move(player, board)
    else:
        return choose_expert_move(player, board)

def make_move(player, board, pos):
    if pos in get_available_moves(board):
        board[pos] = player

def play_turn(player, board, mode):
    (pos, strat) = choose_player_move(player, board) if player is _p1 else choose_p2_move(player, board, mode)
    make_move(player, board, pos)

    print("\n" + get_marker(player) + " occupies position " + str(pos))
    print("Method: " + strat)
    print_board(board)

    winner = get_winner(board)
    if len(get_available_moves(board)) > 0 and not winner:
        play_turn(get_opponent(player), board, mode)
    else:
        print(get_marker(winner) + " Wins" if winner else
              "Tie Game!")
        if input("\nPlay Again? (y/n) ").lower() == "y":
            menu()

# menu
def start_game(starting_player, board, mode):
    play_turn(starting_player, board, mode)

def menu():
    num_rows = 3
    starting_player = _p1
    mode = _expert
    
    print("\nTic-Tac-Toe")
    print("(1) Player vs Computer")
    print("(2) Player vs Player")
    print("(3) 4-by-4 Grid")
    print("(4) Quit")
    
    choice = input("Select an option: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid selection. Please try again.")
        menu()
        return

    if choice not in range(1, 5):
        print("Selection out of range. Please try again")
        menu()
        return

    if choice == 1:
        print("\nPlayer vs Computer")
        print("(1) Beginner")
        print("(2) Expert")
        print("(3) [Go Back]")

        choice_2 = input("Select a difficulty: ")
        try:
            choice_2 = int(choice_2)
        except ValueError:
            menu()
            return
            
        if choice_2 not in range(1, 3):
            menu()
            return
        mode = _beginner if choice_2 == 1 else _expert

        if input("Go first? (y/n) ").lower == "y":
            starting_player = _p1
        else:
            starting_player = _p2
    elif choice == 2:
        mode = _pvp
    elif choice == 3:
        num_rows = 4
    elif choice == 4:
        return

    start_game(starting_player, make_board(num_rows), mode)

menu()
        
