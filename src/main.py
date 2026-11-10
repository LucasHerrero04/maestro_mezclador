import os
from src.core.board import Board
from src.core.player import Player
from src.core.game import GameEngine
from src.core.recipe import Recipe
from src.actions.move import MoveAction

def find_player(board: Board, player_id: str):
    """Busca las coordenadas actuales del jugador en la matriz."""
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == player_id:
                return r, c
    return 0, 0

def main():
    # 1. Preparación del juego (Setup)
    board = Board(5, 5)
    p1 = Player("P1", "Lucas")
    p2 = Player("P2", "Rival")
    game = GameEngine([p1, p2], board)
    
    # 2. Catálogo de Recetas
    recipes = [
        Recipe("Té Clásico", {"hebras_negras": 1}, 10),
        Recipe("Blend Relajante", {"manzanilla": 1, "rooibos": 1}, 25)
    ]
    
    # 3. Ubicar fichas e ingredientes iniciales
    board.place_item(0, 0, "P1")
    board.place_item(4, 4, "P2")
    board.place_item(0, 2, "H")
    board.place_item(2, 2, "M")
    board.place_item(3, 1, "R")
    board.place_item(1, 4, "H")
    
    # 4. Game Loop
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = game.get_current_player()
        
        print(f"\n=== TURNO DE {current_player.name.upper()} ({current_player.player_id}) - PUNTAJE: {current_player.score} ===")
        print(f"Inventario: Hebras({current_player.inventory['hebras_negras']}) | Manzanilla({current_player.inventory['manzanilla']}) | Rooibos({current_player.inventory['rooibos']})")
        
        print("\nRecetas disponibles:")
        for i, r in enumerate(recipes):
            print(f"  [{i+1}] {r.name} ({r.points} pts) -> Requiere: {r.required_ingredients}")
            
        board.display()
        
        print("Controles: W/A/S/D (Mover) | C (Cocinar) | Q (Salir)")
        move = input("Tu jugada: ").upper()
        
        if move == 'Q':
            print("\nJuego terminado por el usuario. ¡Hasta la próxima!")
            break
            
        # Lógica de Canje / Crafteo
        if move == 'C':
            print("¿Qué receta querés preparar? (Ingresá el número 1 o 2)")
            try:
                choice = int(input("> ")) - 1
                selected_recipe = recipes[choice]
                
                # Intentamos craftear
                selected_recipe.craft(current_player)
                input(f"\n¡Éxito! Preparaste {selected_recipe.name} y ganaste {selected_recipe.points} puntos. (Enter para seguir...)")
                game.advance_turn()  # Cocinar consume el turno
            except ValueError as e:
                # Atrapa si no tiene los ingredientes o si pone una letra en vez de número
                input(f"\n[ERROR] {e} (Enter para seguir...)")
            except IndexError:
                input("\n[ERROR] Número de receta inexistente. (Enter para seguir...)")
            continue

        # Lógica de Movimiento
        curr_r, curr_c = find_player(board, current_player.player_id)
        target_r, target_c = curr_r, curr_c
        
        if move == 'W': target_r -= 1
        elif move == 'S': target_r += 1
        elif move == 'A': target_c -= 1
        elif move == 'D': target_c += 1
        else: continue
            
        try:
            action = MoveAction(curr_r, curr_c, target_r, target_c)
            game.process_action(action)
        except Exception as e:
            input(f"\n[MOVIMIENTO INVÁLIDO] {e} (Presiona Enter para continuar...)")

if __name__ == "__main__":
    main()