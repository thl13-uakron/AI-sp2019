#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:54:45 2019

@author: C.-C. Chan
"""

"""
A python implementation of the tic-tac-toe game from David Tourezky's Lisp version


"""

"""
Program modified by Thomas Li on 12 Sep 2019

"""

import random


def make_board():
    return ['board', 0, 0, 0, 0, 0, 0, 0, 0, 0]

_computer = 10
_opponent = 1
_triplets = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]

def convert_to_letter(v):
    if v == 1:
        return 'O'
    elif v == 10:
        return 'X'
    else:
        return ' '
    
def print_row(x, y, z):
    print('\t {0:3} | {1:3} | {2:3} '.format(convert_to_letter(x), convert_to_letter(y), 
          convert_to_letter(z)))
    
#need to fix print board layout    
def print_board(board):
    print_row(board[1], board[2], board[3])
    print('\t-----------------'.center(10))
    print_row(board[4], board[5], board[6])
    print('\t-----------------'.center(10))
    print_row(board[7], board[8], board[9])

def make_move(player, pos, board):
    global state_space
    state_space = update_state_space(player, pos, state_space)
    board[pos] = player
    return board

def sum_triplet(board, triplet):
    return board[triplet[0]] + board[triplet[1]] + board[triplet[2]]

def compute_sums (board):
    return [sum_triplet(board, triplet) for triplet in _triplets]
  

def winner_p (board):
    sums = compute_sums(board)
    return 3 * _computer in sums or 3 * _opponent in sums

def opponent_move(board):
#    print('in opponent:')
#    print(board)
    pos = read_a_legal_move(board)
    new_board = make_move(_opponent, pos, board)
    print_board(new_board)
    if winner_p(new_board):
        print('You win!')
    elif board_full_p(new_board):
        print('Tie game.')
    else:
        computer_move(new_board)

def read_a_legal_move(board):
    pos = int(input('Your move: (enter a number between 1 and 9) '))
    if not (type(pos) == int and (pos >= 1 and pos <=9)):
        print('Invalid input.')
        return read_a_legal_move(board)
    elif board[pos] != 0:
        print('That space is already occupied.')
        return read_a_legal_move(board)
    else:
        return pos

def board_full_p(board):
    return not 0 in board

def computer_move(board):
#    print('In computer move:')
#    print(board)
    best_move = choose_best_move(board)
    pos = best_move[0]
    strategy = best_move[1]
    new_board = make_move(_computer, pos, board)
    print('My move: {} '.format(pos))
    print('My strategy: {} '.format(strategy))
    print_board(new_board)
    if winner_p(new_board):
        print('I win!')
    elif board_full_p(new_board):
        print('Tie game.')
    else:
        return opponent_move(new_board)

def choose_best_move(board):
#    print('choose move: ')
#    print(board)
    return state_space_strategy(_computer, board, state_space)

def random_move_strategy(board):
    pos = pick_random_empty_position(board)
#    print('value of pos in random move strategy: ' + repr(pos))
    return [pos, 'random move']

    
def pick_random_empty_position(board):
    pos = random.choice(list(range(9))) + 1
    if board[pos] == 0:
        return pos
    else:
        return pick_random_empty_position(board)

"""
"Smart" AI strategy using state space:

- Compile a list of available winning states for both side in terms
  of the positions needed to occupy to obtain that state
  
- Upon a side occupying a position:
    - Winning states containing the position on that side are updated
      to only include the remaining required positions
    - Winning states containing the position on the other side are
      removed from consideration

- The computer will pick a position with the goal of making as much
  progress as possible towards getting all required positions for any
  winning state while preventing the player from doing the same

- Moves will be made in the following priority:
    1) Occupying the last position needed for a computer winning state.
    2) Occupying the last position needed for a human winning state.
    3) Occupying the open position that covers the most states with
       two remaining positions required.
    4) Occupying the open position that covers the most states with
       three remaining positions required.
    5) Randomly choosing an open position.

- States available to both sides will be counted equally for now
"""

# input: none
# output: return dict containing the initial list of available winning states for both players
#         each state is expressed as a tuple of the positions the player needs to occupy to win
def init_state_space():
    return {
        _opponent: _triplets,
        _computer: _triplets
        }

# input: identifier of player making move, position of move made, current list of states
# output: return updated state space where moving player has winning state requirements updated
#         and defending player has unavailable winning states removed from consideration
def update_state_space(player, position, state_space):
    return {
        pl : new_space
        for pl in state_space
        for old_space in [state_space[pl]]
        for new_space in
        [[state for state in old_space if position not in state] if pl is not player
          else [tuple([pos for pos in state if pos is not position]) for state in old_space]]
        }

state_space = init_state_space()

# input: identifier of player making move, board, current list of states
# output: return move position selected through analysis of current winning requirements
def state_space_strategy(player, board, state_space):
    strategy_name = "win-state analysis"
    
    # get dict of open positions and winning states that include them
    available_moves = {
        pos : pos_states
        for pos in range(len(board)) if board[pos] == 0
        for pos_states in
        [{pl : pl_states
          for pl in state_space
          for pl_states in
          [[state for state in state_space[pl] if pos in state]]}]
        }

    # get dict of open positions and the number of selection criteria they meet
    # criteria will be checked in order of priority as listed earlier
    # lower-priority criteria will be checked if no single move can be selected from higher priority criteria

    def get_move_priorities(get_score):
        return {
            pos : pos_score
            for pos in available_moves
            for pos_score in
            [get_score(pos)]
            }
    move_priorities = get_move_priorities(lambda pos : 0)

    # 1)
    move_priorities = get_move_priorities(lambda pos : len([states for states in available_moves[pos][player]
                                          if len(states) == 1]))
    selected_moves = [pos for pos in move_priorities if move_priorities[pos] > 0]
    if len(selected_moves) > 0:
        return [selected_moves[0], strategy_name]

    # 2)
    move_priorities = get_move_priorities(lambda pos : sum([len([states for pl in state_space
                                          if pl is not player
                                          for states in available_moves[pos][pl]
                                          if len(states) == 1])]))
    selected_moves = [pos for pos in move_priorities if move_priorities[pos] > 0]
    if len(selected_moves) > 0:
        return [selected_moves[0], strategy_name]

    
    # 3)
    move_priorities = get_move_priorities(lambda pos : sum([len([states for pl in state_space
                                          for states in available_moves[pos][pl]
                                          if len(states) == 2])]))
    selected_moves = [pos for pos in move_priorities if move_priorities[pos] > 0]
    if len(selected_moves) > 0:
        selected_moves = sorted(selected_moves, key = lambda pos : move_priorities[pos], reverse = True)
        selected_moves = [pos for pos in selected_moves
                          if move_priorities[pos] >= move_priorities[selected_moves[0]]]
        # account for ties
    if len(selected_moves) == 1:
        return [selected_moves[0], strategy_name]

    # 4)
    move_priorities = get_move_priorities(lambda pos : move_priorities[pos] +
                                          sum([len([states for pl in state_space
                                          for states in available_moves[pos][pl]
                                          if len(states) == 3])]))
    selected_moves = [pos for pos in move_priorities if move_priorities[pos] > 0]
    if len(selected_moves) > 0:
        selected_moves = sorted(selected_moves, key = lambda pos : move_priorities[pos], reverse = True)
        selected_moves = [pos for pos in selected_moves
                          if move_priorities[pos] >= move_priorities[selected_moves[0]]]
        # account for ties
    if len(selected_moves) == 1:
        return [selected_moves[0], strategy_name]
    
    
    # 5)
    if len(selected_moves) > 0:
        return [random.choice([m for m in selected_moves]), strategy_name]
    return [random.choice([m for m in available_moves]), strategy_name]

def play_one_game():
    global state_space
    state_space = init_state_space()
    choice = input('Would you like to go first? (y/n)')
    if choice == 'y':
        opponent_move(make_board())
    else:
        computer_move(make_board())




    










    
  
    
