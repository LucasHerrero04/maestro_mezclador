import pytest
from src.core.player import Player

def test_player_initialization():
    player = Player("p1", "TestPlayer")
    assert player.name == "TestPlayer"
    assert player.score == 0
    assert player.inventory["rooibos"] == 0

def test_add_ingredient():
    player = Player("p2", "TestPlayer")
    player.add_ingredient("manzanilla", 3)
    assert player.inventory["manzanilla"] == 3

def test_remove_ingredient_insufficient_stock():
    player = Player("p3", "TestPlayer")
    player.add_ingredient("hebras_negras", 1)
    
    # Validamos que el sistema frene un movimiento ilegal
    with pytest.raises(ValueError, match="Stock insuficiente de hebras_negras"):
        player.remove_ingredient("hebras_negras", 2)