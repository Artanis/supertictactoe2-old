# System Modules
import json
from itertools import cycle

# External Modules
from nose.tools import (assert_equal, with_setup, raises)

# Testing Modules
from supertictactoe.supertictactoe import TicTacToe, SquareClaimed

PLAYER_X = u"X"
PLAYER_O = u"O"

TICTACTOE_EMPTY_GAMESTATE = json.dumps({
    'winner': None,
    'squares': [None for x in range(9)],
    'moves': []})

TICTACTOE_TEST_GAMESTATE = json.dumps({
    'winner': None,
    'squares': [
        PLAYER_X, PLAYER_X, PLAYER_O,
        None,     PLAYER_O, None,
        PLAYER_X, PLAYER_O, PLAYER_X],
    'moves': [
        (PLAYER_X, 0), (PLAYER_O, 4), (PLAYER_X, 8),
        (PLAYER_O, 7), (PLAYER_X, 1), (PLAYER_O, 2),
        (PLAYER_X, 6)]})

TICTACTOE_FINISH_GAMESTATE = json.dumps({
    'winner': PLAYER_O,
    'squares': [
        PLAYER_X, PLAYER_X, PLAYER_O,
        PLAYER_O, PLAYER_O, PLAYER_O,
        PLAYER_X, PLAYER_X, None],
    'moves': [
        (PLAYER_X, 7), (PLAYER_O, 3), (PLAYER_X, 6), (PLAYER_O, 2),
        (PLAYER_X, 0), (PLAYER_O, 4), (PLAYER_X, 1), (PLAYER_O, 5)]})

def build_move_list(moves):
    """Zip together a move list and the player cycle."""
    return zip(cycle([PLAYER_X, PLAYER_O]), moves)

def test_tictactoe_dump():
    engine = TicTacToe()
    assert_equal(engine.dump(), TICTACTOE_EMPTY_GAMESTATE)

def test_tictactoe_load():
    engine = TicTacToe.load(TICTACTOE_FINISH_GAMESTATE)
    
    assert_equal(engine.winner, PLAYER_O)
    assert_equal(engine.squares, [
        PLAYER_X, PLAYER_X, PLAYER_O,
        PLAYER_O, PLAYER_O, PLAYER_O,
        PLAYER_X, PLAYER_X, None])
    
    assert_equal(engine.moves, [
        (PLAYER_X, 7), (PLAYER_O, 3), (PLAYER_X, 6), (PLAYER_O, 2),
        (PLAYER_X, 0), (PLAYER_O, 4), (PLAYER_X, 1), (PLAYER_O, 5)])

def test_tictactoe_eq():
    assert_equal(TicTacToe(), TicTacToe())

def test_tictactoe_repr():
    engine = TicTacToe()
    assert_equal(engine, eval(repr(engine)))

def test_tictactoe_playable():
    engine = TicTacToe.load(TICTACTOE_FINISH_GAMESTATE)
    assert_equal(engine.playable(8), True)

def test_tictactoe_unplayable():
    engine = TicTacToe.load(TICTACTOE_FINISH_GAMESTATE)
    assert_equal(engine.playable(0), False)

def test_tictactoe_move_into_unclaimed():
    engine = TicTacToe()
    engine.move(PLAYER_X, 0)
    
    assert_equal(engine.winner, None)
    assert_equal(engine.squares, [
        PLAYER_X, None, None,
        None,     None, None,
        None,     None, None])
    assert_equal(engine.moves, [
        (PLAYER_X, 0)])

@raises(SquareClaimed)
def test_tictactoe_move_into_claimed():
    engine = TicTacToe()
    engine.move(PLAYER_X, 0)
    engine.move(PLAYER_O, 0)

def test_tictactoe_is_winner():
    engine = TicTacToe()
    [engine.move(p, sq) for p, sq in build_move_list(
        [0, 4, 8, 6, 2])]
    
    assert_equal(engine.is_winner(PLAYER_X, 1), True)
    assert_equal(engine.is_winner(PLAYER_X, 7), False)

def test_tictactoe_move_wins():
    engine = TicTacToe()
    
    engine.move(PLAYER_X, 0)
    engine.move(PLAYER_O, 3)
    assert_equal(engine.winner, None)
    
    engine.move(PLAYER_X, 1)
    engine.move(PLAYER_O, 4)
    assert_equal(engine.winner, None)
    
    engine.move(PLAYER_X, 2)
    engine.move(PLAYER_O, 5)
    assert_equal(engine.winner, PLAYER_X)

def test_tictactoe_move_cats():
    engine = TicTacToe()
    [engine.move(p, sq) for p, sq in build_move_list(
        [0, 4, 8, 7, 1, 2, 6, 3, 5])]
    
    assert_equal(engine.winner, "cats")

