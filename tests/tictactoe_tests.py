# System Modules
import json
from itertools import cycle

# External Modules
from nose.tools import (assert_equal, raises)

# Testing Modules
import supertictactoe.supertictactoe
from supertictactoe.supertictactoe import (TicTacToe, SquareClaimed,
    MoveOutOfBounds)

PLAYER_X = u"X"
PLAYER_O = u"O"

EMPTY_GAMESTATE = json.dumps({
    'winner': None,
    'squares': [None for x in range(9)],
    'moves': []})

TEST_GAMESTATE = json.dumps({
    'winner': None,
    'squares': [
        PLAYER_X, PLAYER_X, PLAYER_O,
        None,     PLAYER_O, None,
        PLAYER_X, PLAYER_O, PLAYER_X],
    'moves': [
        (PLAYER_X, 0), (PLAYER_O, 4), (PLAYER_X, 8),
        (PLAYER_O, 7), (PLAYER_X, 1), (PLAYER_O, 2),
        (PLAYER_X, 6)]})

FINISH_GAMESTATE = json.dumps({
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

def test_dump():
    engine = TicTacToe()
    assert_equal(engine.dump(), EMPTY_GAMESTATE)

def test_load():
    engine = TicTacToe.load(FINISH_GAMESTATE)
    
    assert_equal(engine.winner, PLAYER_O)
    assert_equal(engine.squares, [
        PLAYER_X, PLAYER_X, PLAYER_O,
        PLAYER_O, PLAYER_O, PLAYER_O,
        PLAYER_X, PLAYER_X, None])
    
    assert_equal(engine.moves, [
        (PLAYER_X, 7), (PLAYER_O, 3), (PLAYER_X, 6), (PLAYER_O, 2),
        (PLAYER_X, 0), (PLAYER_O, 4), (PLAYER_X, 1), (PLAYER_O, 5)])

def test_eq():
    assert_equal(TicTacToe(), TicTacToe())

def test_repr():
    engine = TicTacToe()
    assert_equal(engine, eval(repr(engine)))

def test_playable():
    engine = TicTacToe.load(FINISH_GAMESTATE)
    assert_equal(engine.playable(8), True)

def test_unplayable():
    engine = TicTacToe.load(FINISH_GAMESTATE)
    assert_equal(engine.playable(0), False)

def test_move_into_unclaimed():
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
def test_move_into_claimed():
    engine = TicTacToe()
    engine.move(PLAYER_X, 0)
    engine.move(PLAYER_O, 0)

@raises(MoveOutOfBounds)
def test_move_out_of_bounds():
    engine = TicTacToe()
    engine.move(PLAYER_X, 9)

def test_is_winner():
    engine = TicTacToe()
    [engine.move(p, sq) for p, sq in build_move_list(
        [0, 4, 8, 6, 2])]
    
    assert_equal(engine.is_winner(PLAYER_X, 1), True)

def test_not_winner():
    engine = TicTacToe()
    [engine.move(p, sq) for p, sq in build_move_list(
        [0, 4, 8, 6, 2])]
    
    assert_equal(engine.is_winner(PLAYER_X, 7), False)

def test_move_wins():
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

def test_move_cats():
    engine = TicTacToe()
    [engine.move(p, sq) for p, sq in build_move_list(
        [0, 4, 8, 7, 1, 2, 6, 3, 5])]
    
    assert_equal(engine.winner, "cats")

