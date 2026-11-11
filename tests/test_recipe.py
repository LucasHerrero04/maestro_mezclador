import pytest
from src.core.player import Player
from src.core.recipe import Recipe

def test_recipe_crafting_success():
    player = Player("p1", "Lucas")
    player.add_ingredient("hebras_negras", 2)
    player.add_ingredient("canela", 1)
    
    chai_recipe = Recipe("Chai Tea", {"hebras_negras": 2, "canela": 1}, 10)
    
    assert chai_recipe.can_be_crafted_by(player) == True
    chai_recipe.craft(player)
    
    assert player.inventory["hebras_negras"] == 0
    assert player.inventory["canela"] == 0
    # FIX: Ahora verificamos que el té se haya guardado en la bandeja, no en el puntaje
    assert "Chai Tea" in player.ready_teas
    assert player.score == 0

def test_recipe_crafting_insufficient_ingredients():
    player = Player("p2", "Rival")
    player.add_ingredient("rooibos", 1)
    
    rooibos_vainilla = Recipe("Rooibos Vainilla", {"rooibos": 2}, 5)
    
    assert rooibos_vainilla.can_be_crafted_by(player) == False
    
    # FIX: Se corrigió la mayúscula del mensaje ("No tienes..." en vez de "no tiene...")
    with pytest.raises(ValueError, match="No tienes los ingredientes para Rooibos Vainilla"):
        rooibos_vainilla.craft(player)