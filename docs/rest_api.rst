REST API for SuperTicTacToe
===========================

A list of resources and methods that can be performed on them.

Collection Structures
=====================
* Game
    * id
    * Winner - The winner of the game
    * Moves - The moves made during the course of the game
    * Boards - The individual components of the game board
        * Winner
        * Moves
        * Squares
* User
    * id/nickname
    * email address

Methods
=======
\/games
    :GET: Games listing, lobby
    :POST: Create new game

\/games/(uuid)
    :GET: Retrieve the game state for the game.
    :DELETE: Delete the game. Cannot undo. Admin only.

\/games/(user)
    :GET: List of games played by user.

\/games/(id)/winner
    :GET: The winner of the game.

\/games/(id)/moves
    :GET: Retrieve a list of moves in the game.

\/games/(id)/boards
    :GET: Retrieve a representation of the game board.

\/games/(id)/boards/(index)
    :GET: Retrieve an individual board.

\/games/(id)/boards/(index)/winner
    :GET: Retrieve the winner of the board.

\/games/(id)/boards/(index)/moves
    :GET: Retrieve the list of moves made in this board.

\/games/(id)/boards/(index)/squares
    :GET: Retrieve the squares composing the board.

