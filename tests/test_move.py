import pytest
from src.core.board import Board
from src.core.player import Player
from src.actions.move import MoveAction

def test_valid_move_and_collect():
    board = Board(3, 3)
    player = Player("P1", "Lucas")
    
    # Setup: Jugador en (0,0) y Hebras en (0,1)
    board.place_item(0, 0, "P1")
    board.place_item(0, 1, "N")  
    
    # Acción: moverse una celda a la derecha
    action = MoveAction(0, 0, 0, 1)
    
    assert action.is_valid(board) is True
    action.execute(board, player)
    
    # QA: Validamos el cambio en el tablero
    assert board.get_item(0, 0) == "."
    assert board.get_item(0, 1) == "P1"
    
    # QA: Validamos que recolectó
    assert player.inventory["hebras_negras"] == 1

def test_invalid_move_diagonal():
    board = Board(3, 3)
    # Intento de mover de (0,0) a (1,1)
    action = MoveAction(0, 0, 1, 1)
    assert action.is_valid(board) is False