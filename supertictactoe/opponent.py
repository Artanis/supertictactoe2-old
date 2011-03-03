# System Modules
from random import choice

# External Modules


# Local Modules

class NoPlayableSquares(Exception):
    pass

class Monkey(object):
    """A simple opponent that makes moves at random.
    """
    def play(self, engine):
        """Composes a play. Returns a 2-tuple containing the desired
        board to play in and the desired square.
        
        Allows exceptions that the choose_board() and choose_square()
        raise in the event either cannot pick one to pass through.
        
        """
        board = self.choose_board(engine)
        square = self.choose_square(engine, board)
        
        return (board, square)
    
    def choose_board(self, engine):
        """Chooses a board to play in. If the engine specifies the next
        board, chooses that one, otherwise, chooses at random from the
        playable boards.
        
        Raises NoPlayableSquares if it can't pick a board (i.e.: all of
        them are full).
        
        """
        if engine.next_board is not None:
            return engine.next_board
        else:
            try:
                return choice(self.playable_boards(engine))
            except IndexError:
                raise NoPlayableSquares(
                    "Cannot pick a board to play in, " +
                    "no remaining plays.")
    
    def choose_square(self, engine, board):
        """Chooses a square at random to play in.
        
        Raises NoPlayableSquares if there are no un-claimed squares to
        pick.
        
        """
        try:
            return choice(self.playable_squares(engine, board))
        except IndexError:
            raise NoPlayableSquares(
                "Cannot pick a square to play in. Board is full.")
    
    def playable_boards(self, engine):
        """Builds a list of boards that can be played on.
        """
        return [i for i, sq in enumerate(
            engine.squares) if len(sq.moves) < 9]
    
    def playable_squares(self, engine, board):
        """Builds a list of squares in the given board that can be
        played on.
        """
        return [i for i, sq in enumerate(
            engine.squares[board].squares) if sq is None]

def main():
    pass

if __name__ == "__main__":
    main()
