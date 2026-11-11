import os
import random
from src.core.board import Board
from src.core.player import Player
from src.core.game import GameEngine
from src.core.recipe import Recipe
from src.actions.move import MoveAction

def find_player(board: Board, player_id: str):
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == player_id:
                return r, c
    return 0, 0

def place_randomly(board: Board, item: str):
    empty_cells = []
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == ".":
                empty_cells.append((r, c))
    
    if empty_cells:
        chosen_r, chosen_c = random.choice(empty_cells)
        board.place_item(chosen_r, chosen_c, item)

def main():
    board = Board(6, 6) # Tablero un poco más grande (6x6) para acomodar más ítems
    p1 = Player("P1", "Lucas")
    p2 = Player("P2", "Rival")
    game = GameEngine([p1, p2], board)
    
    recipes = [
        Recipe("Té Clásico", {"hebras_negras": 1}, 10),
        Recipe("Té Rojo Simple", {"te_rojo": 1}, 10),
        Recipe("Tisana de Manzanilla", {"manzanilla": 1}, 10),
        Recipe("Blend Relajante", {"manzanilla": 1, "rooibos": 1}, 25),
        Recipe("Rojo Frutal", {"te_rojo": 1, "frutos_rojos": 1}, 25),
        Recipe("Negro Especiado", {"hebras_negras": 1, "canela": 1}, 25),
        Recipe("Chai Imperial", {"hebras_negras": 1, "te_rojo": 1, "canela": 1}, 50),
        Recipe("Infusión Silvestre", {"rooibos": 1, "manzanilla": 1, "frutos_rojos": 1}, 50)
    ]
    
    # Pool de ítems iniciales (más bases, menos rarezas)
    initial_entities = ["P1", "P2", "N", "N", "N", "R", "R", "O", "O", "M", "M", "F", "C"]
    for entity in initial_entities:
        place_randomly(board, entity)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = game.get_current_player()
        
        print(f"\n=== TURNO DE {current_player.name.upper()} ({current_player.player_id}) - PUNTAJE: {current_player.score} ===")
        # Interfaz de inventario compacta
        inv = current_player.inventory
        print(f"Bolsa: Negras({inv['hebras_negras']}) | Rojo({inv['te_rojo']}) | Rooibos({inv['rooibos']}) | Manza({inv['manzanilla']}) | Frutos({inv['frutos_rojos']}) | Canela({inv['canela']})")
        
        print("\nRecetas disponibles:")
        for i, r in enumerate(recipes):
            print(f"  [{i+1}] {r.name} ({r.points} pts) -> Requiere: {r.required_ingredients}")
            
        board.display()
        
        print("Controles: W/A/S/D (Mover) | C (Cocinar) | Q (Salir)")
        move = input("Tu jugada: ").upper()
        
        if move == 'Q':
            print("\n¡Hasta la próxima, Maestro Mezclador!")
            break
            
        if move == 'C':
            print("¿Qué receta querés preparar? (Ingresá el número)")
            try:
                choice = int(input("> ")) - 1
                selected_recipe = recipes[choice]
                selected_recipe.craft(current_player)
                input(f"\n¡Éxito! Preparaste {selected_recipe.name} y ganaste {selected_recipe.points} puntos. (Enter para seguir...)")
                game.advance_turn()  
            except ValueError as e:
                input(f"\n[ERROR] {e} (Enter para seguir...)")
            except IndexError:
                input("\n[ERROR] Número de receta inexistente. (Enter para seguir...)")
            continue

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