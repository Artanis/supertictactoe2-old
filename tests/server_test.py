# System Modules
import json
from collections import Sequence

# External Modules
from nose.tools import (assert_equal, assert_true)

# Local Modules
from supertictactoe.supertictactoe import SuperTicTacToe, TicTacToe
from supertictactoe.server.wsgi_server import app



def test_get_games_list():
    response = json.loads(app.handle('/games', method="GET"))
    
    assert_true("games" in response)
    assert_true(isinstance(response['games'], Sequence))

def test_get_game_by_id():
    response = json.loads(app.handle('/games/1337', method='GET'))
    
    assert_true("winner" in response)
    assert_true("moves" in response)
    assert_true("squares" in response)
    assert_true(isinstance(response['moves'], Sequence))
    assert_true(isinstance(response['squares'], Sequence))
    assert_equal(len(response['squares']), 9)
    
    for sq in response['squares']:
        assert_true("winner" in sq)
        assert_true("moves" in sq)
        assert_true("squares" in sq)
        assert_true(isinstance(sq['moves'], Sequence))
        assert_true(isinstance(sq['squares'], Sequence))
        assert_equal(len(sq['squares']), 9)

def test_get_game_winner():
    response = json.loads(app.handle('/games/1337/winner',
        method='GET'))
    
    assert_true("winner" in response)
