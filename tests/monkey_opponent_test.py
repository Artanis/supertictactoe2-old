# System Modules


# External Modules
from nose.tools import (assert_equal, assert_true, assert_false, raises)

# Local Modules
from supertictactoe.opponent import Monkey, NoPlayableSquares
from supertictactoe.supertictactoe import SuperTicTacToe
from supertictactoe_tests import build_move_list

PLAYER_X = "X"
PLAYER_O = "O"

def test_playable_boards():
    engine = SuperTicTacToe()
    opponent = Monkey()
    
    assert_equal(opponent.playable_boards(engine), [0,1,2,3,4,5,6,7,8])
    
    moves = build_move_list([
        (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (0, 4), (4, 0),
        (0, 5), (5, 0), (0, 6), (6, 0), (0, 7), (7, 0), (0, 8), (8, 0),
        (0, 0)])
    [engine.move(p, b, sq) for p, b, sq in moves]
    
    assert_equal(opponent.playable_boards(engine), [1,2,3,4,5,6,7,8])

def test_playable_squares():
    engine = SuperTicTacToe()
    opponent = Monkey()
    
    assert_equal(opponent.playable_squares(engine, 0),
        [0,1,2,3,4,5,6,7,8])
    
    engine.move(PLAYER_X, 0, 0)
    
    assert_equal(opponent.playable_squares(engine, 0),
        [1,2,3,4,5,6,7,8])

def test_choose_board():
    engine = SuperTicTacToe()
    opponent = Monkey()
    
    
    for x in range(1000):
        assert_true(opponent.choose_board(engine) in [0,1,2,3,4,5,6,7,8])
    
    moves = build_move_list([
        (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (0, 4), (4, 0),
        (0, 5), (5, 0), (0, 6), (6, 0), (0, 7), (7, 0), (0, 8), (8, 0)])
    
    for player, board, square in moves:
        engine.move(player, board, square)
        assert_equal(opponent.choose_board(engine), square)

def test_choose_square():
    engine = SuperTicTacToe()
    opponent = Monkey()
    
    for x in range(1000):
        assert_true(opponent.choose_square(engine, 1) in [0,1,2,3,4,5,6,7,8])
    
    moves = build_move_list([
        (0, 0), (0, 3), (3, 6), (6, 3), (3, 5), (5, 1), (1, 3), (3, 4),
        (4, 2), (2, 5), (5, 2), (2, 6), (6, 4)])
    
    for player, board, square in moves:
        engine.move(player, board, square)
        
        possibilities = [i for i, sq in enumerate(
            engine.squares[square].squares) if sq is None]
        
        for x in range(1000):
            assert_true(opponent.choose_square(engine, square) in possibilities)

@raises(NoPlayableSquares)
def test_choose_board_from_full():
    engine = SuperTicTacToe()
    opponent = Monkey()
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
    
    opponent.choose_board(engine)

@raises(NoPlayableSquares)
def test_choose_square_from_full():
    engine = SuperTicTacToe()
    opponent = Monkey()
    moves = build_move_list([
        (0, 1), (1, 0), (0, 2), (2, 0), (0, 3), (3, 0), (0, 4), (4, 0),
        (0, 5), (5, 0), (0, 6), (6, 0), (0, 7), (7, 0), (0, 8), (8, 0),
        (0, 0)])
    [engine.move(p, b, sq) for p, b, sq in moves]
    
    opponent.choose_square(engine, 0)

@raises(NoPlayableSquares)
def test_play_on_full():
    engine = SuperTicTacToe()
    opponent = Monkey()
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
    
    opponent.play(engine)

def test_play():
    engine = SuperTicTacToe()
    opponent = Monkey()
    
    play = opponent.play(engine)
    assert_true(all(x is not None for x in play))

