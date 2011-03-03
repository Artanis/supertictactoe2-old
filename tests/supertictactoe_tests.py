# System Modules
import os
import json
from itertools import cycle
from random import choice, randint

# External Modules
from nose.tools import (assert_equal, with_setup, raises, assert_false, assert_true)

# Local Modules
import supertictactoe.supertictactoe
from supertictactoe.supertictactoe import (TicTacToe, SuperTicTacToe,
    SquareClaimed, MoveOutOfBounds, IncorrectBoard)

PLAYER_X = "X"
PLAYER_O = "O"

def build_move_list(moves):
    p = cycle([PLAYER_X, PLAYER_O])
    for b, sq in moves:
        yield p.next(), b, sq

def test_repr():
    engine = SuperTicTacToe()
    assert_equal(engine, eval(repr(engine)))

def test_move():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 8)

@raises(IncorrectBoard)
def test_move_into_wrong_board():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 0)
    engine.move(PLAYER_O, 1, 0)

@raises(SquareClaimed)
def test_move_into_claimed():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 0)
    engine.move(PLAYER_O, 0, 0)

def test_move_into_claimed_no_record():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 0)
    try:
        engine.move(PLAYER_O, 0, 0)
    except SquareClaimed:
        pass
    assert_equal(len(engine.moves), 1)

def test_next_board_empty():
    engine = SuperTicTacToe()
    assert_equal(engine.next_board, None)

def test_next_board_one():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 1)
    assert_equal(engine.next_board, 1)

def test_next_board_full():
    engine = SuperTicTacToe()
    moves = build_move_list([
        (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (0, 4), (4, 0),
        (0, 5), (5, 0), (0, 6), (6, 0), (0, 7), (7, 0), (0, 8), (8, 0),
        (0, 0)])
    [engine.move(p, b, sq) for p, b, sq in moves]
    
    assert_equal(engine.next_board, None)

def test_playable():
    engine = SuperTicTacToe()
    assert_equal(engine.playable(0), True)

def test_unplayable():
    engine = SuperTicTacToe()
    engine.move(PLAYER_X, 0, 0)
    assert_equal(engine.playable(1), False)

def test_is_not_winner():
    engine = SuperTicTacToe()
    
    assert_false(engine.is_winner(PLAYER_X, 1, 4))

def test_is_winner():
    engine = SuperTicTacToe()
    moves = build_move_list([
        (0, 6), (6, 0), (0, 4), (4, 0), (0, 2), (2, 1), (1, 7), (7, 1),
        (1, 4), (4, 1), (1, 1), (1, 2), (2, 3), (3, 2), (2, 4), (4, 2)])
    
    for player, board, square in moves:
        engine.move(player, board, square)
    
    assert_false(engine.is_winner(PLAYER_X, 2, 0))
    assert_true(engine.is_winner(PLAYER_X, 2, 5))

def test_move_wins():
    engine = SuperTicTacToe()
    moves = build_move_list([
        (0, 6), (6, 0), (0, 4), (4, 0), (0, 2), (2, 1), (1, 7), (7, 1),
        (1, 4), (4, 1), (1, 1), (1, 2), (2, 3), (3, 2), (2, 4), (4, 2),
        (2, 5)])
    
    for player, board, square in moves:
        assert_equal(engine.winner, None)
        engine.move(player, board, square)
    
    assert_equal(engine.winner, PLAYER_X)

def test_move_cats():
    engine = SuperTicTacToe()

def test_empty_dump():
    empty_gamestate = json.dumps(dict(winner=None, moves=[],
        squares=[t3.__dict__ for t3 in (TicTacToe() for x in range(9))]))
    
    engine = SuperTicTacToe()
    assert_equal(engine.dump(), empty_gamestate)

def test_normal_dump():
    engine = SuperTicTacToe()
    moves = build_move_list([
        (0, 8), (8, 6), (6, 3), (3, 2), (2, 0), (0, 2), (2, 6), (6, 5),
        (5, 4), (4, 4), (4, 5), (5, 3), (3, 8), (8, 8), (8, 4), (4, 2),
        (2, 2), (2, 4), (4, 3), (3, 0), (0, 3), (3, 7), (7, 7), (7, 6),
        (6, 6), (6, 1), (1, 5), (5, 1), (1, 8), (8, 0), (0, 6), (6, 8),
        (8, 5), (5, 8), (8, 3), (3, 4), (4, 0), (0, 0), (0, 7), (7, 2),
        (2, 8), (8, 7), (7, 4), (4, 6), (6, 2), (2, 5), (5, 2), (2, 3),
        (3, 1), (1, 4), (4, 7), (7, 1), (1, 2), (2, 7), (7, 5), (5, 5),
        (5, 7), (7, 8), (8, 2), (2, 1), (1, 3), (3, 5), (5, 0), (0, 5),
        (5, 6), (6, 7), (7, 0), (0, 1), (1, 7), (7, 3), (3, 6), (6, 0),
        (0, 4), (4, 8), (8, 1), (1, 6), (6, 4), (4, 1), (1, 1), (1, 0),
        (3, 3)])
    [engine.move(p, b, sq) for p, b, sq in moves]
    
    expected = json.dumps(dict(winner=engine.winner, moves=engine.moves,
        squares=[sq.__dict__ for sq in engine.squares]))
    
    assert_equal(engine.dump(), expected)

def test_load():
    src_engine = SuperTicTacToe()
    [src_engine.move(p, b, sq) for p, b, sq in build_move_list([
        (0, 8), (8, 6), (6, 3), (3, 2), (2, 0), (0, 2), (2, 6), (6, 5),
        (5, 4), (4, 4), (4, 5), (5, 3), (3, 8), (8, 8), (8, 4), (4, 2),
        (2, 2), (2, 4), (4, 3), (3, 0), (0, 3), (3, 7), (7, 7), (7, 6),
        (6, 6), (6, 1), (1, 5), (5, 1), (1, 8), (8, 0), (0, 6), (6, 8),
        (8, 5), (5, 8), (8, 3), (3, 4), (4, 0), (0, 0), (0, 7), (7, 2),
        (2, 8), (8, 7), (7, 4), (4, 6), (6, 2), (2, 5), (5, 2), (2, 3),
        (3, 1), (1, 4), (4, 7), (7, 1), (1, 2), (2, 7), (7, 5), (5, 5),
        (5, 7), (7, 8), (8, 2), (2, 1), (1, 3), (3, 5), (5, 0), (0, 5),
        (5, 6), (6, 7), (7, 0), (0, 1), (1, 7), (7, 3), (3, 6), (6, 0),
        (0, 4), (4, 8), (8, 1), (1, 6), (6, 4), (4, 1), (1, 1), (1, 0),
        (3, 3)])]
        
    engine = SuperTicTacToe.load(src_engine.dump())
    
    assert_equal(engine, src_engine)

