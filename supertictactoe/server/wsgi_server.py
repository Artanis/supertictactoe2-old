# System Modules
import json

# External Modules
import bottle
from bottle import (route)

# Local Modules
from ..supertictactoe import SuperTicTacToe

bottle.debug(True)

@route('/')
def index():
    return "Hello NoseTests"

@route('/games')
def get_games_list():
    return json.dumps({"games":[]})

@route('/games/:game_id')
def get_game_by_id(game_id):
    engine = SuperTicTacToe()
    return engine.dump()

@route('/games/:game_id/winner')
def get_game_winner(game_id):
    return json.dumps({"winner":None})

app = bottle.app()

def main():
    bottle.run(app=app)

if __name__ == "__main__":
    main()
