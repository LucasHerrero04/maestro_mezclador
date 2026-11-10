from src.core.board import Board
from src.core.player import Player

class GameEngine:
    def __init__(self, players: list[Player], board: Board):
        if not players:
            raise ValueError("Se necesitan jugadores para iniciar la partida")
        self.players = players
        self.board = board
        self.current_turn_index = 0
        self.is_active = True

    def get_current_player(self) -> Player:
        """Devuelve el jugador que tiene el turno actual."""
        return self.players[self.current_turn_index]

    def advance_turn(self):
        """Pasa el turno al siguiente jugador de forma circular."""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    def process_action(self, action):
        """Ejecuta una acción verificando las reglas de turno."""
        if not self.is_active:
            raise ValueError("El juego ya ha terminado")
            
        current_player = self.get_current_player()
        
        # Ejecutamos la acción pasándole el estado central del juego
        action.execute(self.board, current_player)
        
        # Si la acción no lanzó ningún error, avanzamos el turno
        self.advance_turn()