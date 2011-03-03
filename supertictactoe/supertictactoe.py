# System Modules
import json

# External Modules


# Local Modules


class SquareClaimed(ValueError):
    pass


class MoveOutOfBounds(IndexError):
    pass


class IncorrectBoard(ValueError):
    pass


# =========================================== BEGIN CLASS TicTacToe ===
class TicTacToe():
    def __init__(self, state=None):
        state = state or {}
        
        self.winner = state.get('winner', None)
        self.squares = list(state.get('squares',
            (None for x in range(9))))
        self.moves = [(str(p), sq) for p, sq in state.get('moves', [])]
    
    def move(self, player, square):
        if square < 0 or square > 8:
            raise MoveOutOfBounds(
                "Square must be an integer between 0 and 8")
            return
        
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
        game_board = self.squares[:]
        if game_board[square] is None:
            game_board[square] = player
        
        # Calculate the column and row the move was made on, and if it
        # was also on a diagonal.
        column = square % 3
        row = square - (square % 3)
        
        # Assemble the tests.
        # List of generators that slice out the interesting squares,
        # and yield whether the square belongs to the given player.
        # Aside from the slices, no calculation is done yet.
        tests = [
            (sq == player for sq in game_board[column:9:3]),
            (sq == player for sq in game_board[row:row+3]),
            (sq == player for sq in game_board[0:9:4]),
            (sq == player for sq in game_board[2:8:2])]
        
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
        return ("{0}(dict(winner={1}, squares={2}, moves={3}))".
            format(
                self.__class__,
                self.winner, self.squares, self.moves))
    
    def __str__(self):
        return "[{0}] winner: {1}".format(
            "".join([sq or "." for sq in self.squares]),
            self.winner)
# ============================================= END CLASS TicTacToe ===


# ====================================== BEGIN CLASS SuperTicTacToe ===
class SuperTicTacToe(TicTacToe):
    def __init__(self, state=None):
        state = state or {}
        
        self.winner = state.get("winner", None)
        self.moves  = [(p, b, sq) for p, b, sq in
            state.get("moves", [])]
        
        # FIXME: repr() and load() use different styles.
        #  repr() dumps repr() of the TicTacToe boards, while dump()
        # json encodes the whole thing.
        self.squares = []
        for sq in state.get("squares", [None for x in range(9)]):
            if isinstance(sq, TicTacToe):
                self.squares.append(sq)
            else:
                self.squares.append(TicTacToe(sq))
    
    def playable(self, square):
        return (self.next_board is None or
            self.next_board == square)
    
    def move(self, player, board, square):
        if self.playable(board):
            self.squares[board].move(player, square)
            self.moves.append((player, board, square))
            
            if self.winner is None:
                if self.is_winner(player, board, square):
                    self.winner = player
                elif len(self.moves) >= 81:
                    self.winner = "cats"
        else:
            error = (
                "Expected a play in board {0}, got board {1}".format(
                self.next_board if self.next_board is not None else "1-8",
                board))
            raise IncorrectBoard(error)
    
    def is_winner(self, player, board, square):
        game_board = [b.winner for b in self.squares]
        
        if self.squares[board].is_winner(player, square):
            if game_board[board] is None:
                game_board[board] = player
        
        # Calculate the column and row the move was made on, and if it
        # was also on a diagonal.
        column = board % 3
        row = board - (board % 3)
        
        # Assemble the tests.
        # List of generators that slice out the interesting squares,
        # and yield whether the square belongs to the given player.
        # Aside from the slices, no calculation is done yet.
        tests = [
            (sq == player for sq in game_board[column:9:3]),
            (sq == player for sq in game_board[row:row+3]),
            (sq == player for sq in game_board[0:9:4]),
            (sq == player for sq in game_board[2:8:2])]
        
        # If any of those tests has all the values True, then True.
        return any(all(test) for test in tests)
    
    @property
    def next_board(self):
        """The next playable board by index, or None for any board.
        """
        if len(self.moves) >= 1:
            target = self.moves[-1][2]
            
            if len(self.squares[target].moves) < 9:
                # Proceed as normal
                return target
            else:
                # Targeted board is full, play anywhere.
                return None
        else:
            # No moves. First move plays anywhere.
            return None
    
    def dump(self):
        return json.dumps(dict(
            winner=self.winner, moves=self.moves,
            squares=[sq.__dict__ for sq in self.squares]))
    
    def __str__(self):
        result = []
        result.append("squares:  012345678  winner: %s" % self.winner)
        for i, sq in enumerate(self.squares):
            result.append("Board %d: %s" % (i, str(sq)))
        
        return "\n".join(result)
# ======================================== END CLASS SuperTicTacToe ===


# ======================================== EXCLUDED FROM UNIT TESTS ===
def main():
    from itertools import cycle
    from opponent import Monkey
    
    # Engine and machine player
    engine = SuperTicTacToe()
    opponent = Monkey()
    turn = cycle("XO")
    
    # Playball
    while engine.winner is None: # FIXME: Winner isn't being determined
        print engine, "\n"
        engine.move(turn.next(), *opponent.play(engine))
    print engine
    print engine.dump()

if __name__ == "__main__":
    main()

