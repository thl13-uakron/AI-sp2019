#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:54:45 2019

@author: C.-C. Chan
"""

"""
A python implementation of the tic-tac-toe game from David Tourezky's Lisp version


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
        read_a_legal_move(board)
    elif board[pos] != 0:
        print('That space is already occupied.')
        read_a_legal_move(board)
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
    return random_move_strategy(board)

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


def play_one_game():
    choice = input('Would you like to go first? (y/n)')
    if choice == 'y':
        opponent_move(make_board())
    else:
        computer_move(make_board())





    










    
  
    