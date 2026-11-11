class Player:
    def __init__(self, player_id: str, name: str):
        self.player_id = player_id
        self.name = name
        self.score = 0
        self.inventory = {
            "hebras_negras": 0,
            "te_rojo": 0,
            "rooibos": 0,
            "manzanilla": 0,
            "frutos_rojos": 0,
            "canela": 0
        }
        self.ready_teas = []

    def add_ingredient(self, ingredient: str, amount: int):
        if ingredient not in self.inventory:
            raise ValueError(f"Ingrediente desconocido: {ingredient}")
        if amount <= 0:
            raise ValueError("La cantidad a añadir debe ser mayor a cero")
        
        self.inventory[ingredient] += amount

    def remove_ingredient(self, ingredient: str, amount: int):
        if ingredient not in self.inventory:
            raise ValueError(f"Ingrediente desconocido: {ingredient}")
        if self.inventory[ingredient] < amount:
            raise ValueError(f"Stock insuficiente de {ingredient}")
        
        self.inventory[ingredient] -= amount