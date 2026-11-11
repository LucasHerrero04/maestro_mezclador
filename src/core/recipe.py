from src.core.player import Player

class Recipe:
    def __init__(self, name: str, required_ingredients: dict, points: int):
        self.name = name
        self.required_ingredients = required_ingredients
        self.points = points

    def can_be_crafted_by(self, player: Player) -> bool:
        """Verifica si el jugador tiene los ingredientes necesarios."""
        for ingredient, amount in self.required_ingredients.items():
            if player.inventory.get(ingredient, 0) < amount:
                return False
        return True

    def craft(self, player):
        if self.can_be_crafted_by(player):
            # Consumimos los ingredientes
            for ingredient, amount in self.required_ingredients.items():
                player.inventory[ingredient] -= amount
            
            # NUEVO: En vez de dar puntos, ponemos el té en la bandeja del jugador
            player.ready_teas.append(self.name)
        else:
            raise ValueError(f"No tienes los ingredientes para {self.name}")