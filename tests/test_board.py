import pytest
from src.core.board import Board

def test_board_initialization():
    board = Board(3, 3)
    assert board.rows == 3
    assert board.cols == 3
    assert board.get_item(0, 0) == "."

def test_place_and_get_item():
    board = Board(5, 5)
    board.place_item(2, 2, "H")  # H = Hebras negras
    assert board.get_item(2, 2) == "H"

def test_out_of_bounds_coordinates():
    board = Board(4, 4)
    # Intentamos acceder a la fila 5 en un tablero de 4x4 (índices 0 al 3)
    with pytest.raises(IndexError, match="Coordenadas fuera de los límites"):
        board.place_item(5, 0, "X")