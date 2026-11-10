class Board:
    def __init__(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise ValueError("El tablero debe tener dimensiones positivas")
        self.rows = rows
        self.cols = cols
        # Inicializamos una matriz 2D llena de espacios vacíos representados por "."
        self.grid = [["." for _ in range(cols)] for _ in range(rows)]

    def place_item(self, row: int, col: int, item: str):
        """Coloca un ingrediente o jugador en una coordenada específica."""
        self._validate_coordinates(row, col)
        self.grid[row][col] = item

    def get_item(self, row: int, col: int) -> str:
        """Devuelve lo que hay en una coordenada."""
        self._validate_coordinates(row, col)
        return self.grid[row][col]
        
    def remove_item(self, row: int, col: int):
        """Vacía una celda específica."""
        self._validate_coordinates(row, col)
        self.grid[row][col] = "."

    def _validate_coordinates(self, row: int, col: int):
        """Uso interno: verifica que las coordenadas no se salgan del mapa."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Coordenadas fuera de los límites del tablero")

    def display(self):
        """Imprime el tablero en la terminal para que sea VISIBLE."""
        print("\n--- MERCADO DE INGREDIENTES ---")
        for row in self.grid:
            # Une cada elemento de la fila con corchetes para que parezca un casillero
            row_display = " ".join([f"[{cell}]" for cell in row])
            print(row_display)
        print("-------------------------------\n")