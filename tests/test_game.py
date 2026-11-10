import pytest
from src.core.player import Player
from src.core.board import Board
from src.core.game import GameEngine
from src.actions.move import MoveAction

def test_game_initialization():
    players = [Player("p1", "Lucas"), Player("p2", "Rival")]
    board = Board(3, 3)
    game = GameEngine(players, board)
    
    assert game.get_current_player().name == "Lucas"
    assert game.is_active is True

def test_turn_advancement():
    players = [Player("p1", "Lucas"), Player("p2", "Rival")]
    board = Board(3, 3)
    game = GameEngine(players, board)
    
    game.advance_turn()
    assert game.get_current_player().name == "Rival"
    
    game.advance_turn()
    assert game.get_current_player().name == "Lucas"  # Vuelve al inicio gracias al módulo (%)

def test_process_action_changes_turn():
    players = [Player("p1", "Lucas"), Player("p2", "Rival")]
    board = Board(3, 3)
    board.place_item(0, 0, "P1")
    
    game = GameEngine(players, board)
    
    # Lucas mueve su ficha a la derecha
    action = MoveAction(0, 0, 0, 1)
    game.process_action(action)
    
    # QA: Validamos que el turno pasó correctamente al rival tras el movimiento
    assert game.get_current_player().name == "Rival"