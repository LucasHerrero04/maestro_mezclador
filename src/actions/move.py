from src.core.board import Board
from src.core.player import Player

class MoveAction:
    def __init__(self, current_row: int, current_col: int, target_row: int, target_col: int):
        self.current_row = current_row
        self.current_col = current_col
        self.target_row = target_row
        self.target_col = target_col
        
        # Diccionario para traducir la letra del tablero al ingrediente del inventario
        self.ingredient_map = {
            "H": "hebras_negras",
            "M": "manzanilla",
            "R": "rooibos",
            "E": "especias"
        }

    def is_valid(self, board: Board) -> bool:
        """Verifica límites, distancia y que la celda no esté ocupada por otro jugador."""
        # 1. Verificamos límites del mapa
        if (self.target_row < 0 or self.target_row >= board.rows or 
            self.target_col < 0 or self.target_col >= board.cols):
            return False
            
        # 2. Distancia Manhattan: debe ser exactamente 1
        row_diff = abs(self.target_row - self.current_row)
        col_diff = abs(self.target_col - self.current_col)
        
        if (row_diff + col_diff) != 1:
            return False

        # 3. DETECCIÓN DE COLISIONES: Evitar pisar a otro jugador
        target_item = board.get_item(self.target_row, self.target_col)
        # Si el ítem empieza con "P" (P1, P2, etc.), el movimiento es inválido
        if target_item.startswith("P"):
            return False
            
        return True

    def execute(self, board: Board, player: Player):
        """Ejecuta el movimiento y recolecta ingredientes si los pisa."""
        if not self.is_valid(board):
            raise ValueError("Movimiento inválido: salto ilegal o fuera del mapa.")

        # Miramos qué hay en la celda de destino antes de pisarla
        target_item = board.get_item(self.target_row, self.target_col)

        # Si hay un ingrediente (está en nuestro mapa de letras), lo sumamos al inventario
        if target_item in self.ingredient_map:
            ingredient_name = self.ingredient_map[target_item]
            player.add_ingredient(ingredient_name, 1)

        # Actualizamos el tablero visualmente
        board.remove_item(self.current_row, self.current_col)
        board.place_item(self.target_row, self.target_col, player.player_id)