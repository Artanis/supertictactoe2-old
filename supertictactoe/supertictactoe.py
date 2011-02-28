# System Modules
import json

# External Modules


# Local Modules

class SquareClaimed(ValueError):
    pass

class TicTacToe():
    def __init__(self, state=None):
        state = state or {}
        
        self.winner = state.get('winner', None)
        self.squares = list(state.get('squares',
            (None for x in range(9))))
        self.moves = [(str(p), sq) for p, sq in state.get('moves', [])]
    
    def move(self, player, square):
        if self.playable(square):
            self.squares[square] = player
            self.moves.append((player, square))
            
            if self.winner is None:
                if self.is_winner(player, square):
                    self.winner = player
                elif len(self.moves) >= 9:
                    self.winner = "cats"
                
        else:
            raise SquareClaimed("Square already played in.")
    
    def is_winner(self, player, square):
        """Determine if the given move will win the game.
        
        Or has won the game, if it was already played.
        
        """
        # Make a copy of the board and place the move into it to test
        # against.
        squares = self.squares[:]
        if squares[square] is None:
            squares[square] = player
        
        # Calculate the column and row the move was made on, and if it
        # was also on a diagonal.
        column = square % 3
        row = square - (square % 3)
        
        # Assemble the tests. List of generators that slice out the
        # interesting squares, and yield whether the square belongs to
        # the given player. No calculation is done yet.
        tests = [
            (sq == player for sq in squares[column:9:3]),
            (sq == player for sq in squares[row:row+3]),
            (sq == player for sq in squares[0:9:4]),
            (sq == player for sq in squares[2:8:2])]
        
        # If any of those tests has all the values True, then True.
        return any(all(test) for test in tests)
    
    def playable(self, square):
        return self.squares[square] is None
    
    def dump(self):
        return json.dumps({
            'winner': self.winner,
            'squares': self.squares,
            'moves': self.moves})
    
    @classmethod
    def load(cls, game_state_json):
        return cls(json.loads(game_state_json))
    
    def __eq__(self, other):
        return (self.winner == other.winner and
                self.squares == other.squares and
                self.moves == other.moves)
    
    def __repr__(self):
        return ("TicTacToe(dict(squares={0}, moves={1}, winner={2}))".
            format(self.squares, self.moves, self.winner))
    
    def __str__(self):
        return "[%s] winner: %s" % (
            "".join([cell or "." for cell in self.cells]),
            self.winner)

def main():
    pass

if __name__ == "__main__":
    main()
