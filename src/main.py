import os
import random
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

def place_randomly(board: Board, item: str):
    """Busca todas las celdas vacías y coloca el ítem en una al azar."""
    empty_cells = []
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == ".":
                empty_cells.append((r, c))
    
    if empty_cells:
        chosen_r, chosen_c = random.choice(empty_cells)
        board.place_item(chosen_r, chosen_c, item)

def spawn_ingredients(board: Board, amount: int):
    """Genera nuevos ingredientes usando un pool de probabilidades."""
    # Hay más N y R en la lista, por lo que tienen más chances de salir que F o C
    pool = ["N", "N", "N", "R", "R", "O", "M", "F", "C"]
    for _ in range(amount):
        place_randomly(board, random.choice(pool))

def main():
    board = Board(6, 6) 
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
    
    # Setup Inicial
    place_randomly(board, "P1")
    place_randomly(board, "P2")
    spawn_ingredients(board, 12) # Llenamos el tablero inicial
    
    turn_count = 0 # Contador global de turnos exitosos
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = game.get_current_player()
        
        print(f"\n=== TURNO DE {current_player.name.upper()} ({current_player.player_id}) - PUNTAJE: {current_player.score} ===")
        inv = current_player.inventory
        print(f"Bolsa: Negras({inv['hebras_negras']}) | Rojo({inv['te_rojo']}) | Rooibos({inv['rooibos']}) | Manza({inv['manzanilla']}) | Frutos({inv['frutos_rojos']}) | Canela({inv['canela']})")
        
        print("\nRecetas disponibles:")
        for i, r in enumerate(recipes):
            print(f"  [{i+1}] {r.name} ({r.points} pts) -> Requiere: {r.required_ingredients}")
            
        board.display()
        
        print("Controles: W/A/S/D (Mover) | C (Cocinar) | Q (Salir)")
        move = input("Tu jugada: ").upper()
        
        turn_successful = False # Bandera para saber si logró hacer algo válido
        
        if move == 'Q':
            print("\n¡Hasta la próxima, Maestro Mezclador!")
            break
            
        elif move == 'C':
            print("¿Qué receta querés preparar? (Ingresá el número)")
            try:
                choice = int(input("> ")) - 1
                selected_recipe = recipes[choice]
                selected_recipe.craft(current_player)
                input(f"\n¡Éxito! Preparaste {selected_recipe.name} y ganaste {selected_recipe.points} puntos. (Enter para seguir...)")
                game.advance_turn()  
                turn_successful = True
            except ValueError as e:
                input(f"\n[ERROR] {e} (Enter para seguir...)")
            except IndexError:
                input("\n[ERROR] Número de receta inexistente. (Enter para seguir...)")
                
        elif move in ['W', 'A', 'S', 'D']:
            curr_r, curr_c = find_player(board, current_player.player_id)
            target_r, target_c = curr_r, curr_c
            
            if move == 'W': target_r -= 1
            elif move == 'S': target_r += 1
            elif move == 'A': target_c -= 1
            elif move == 'D': target_c += 1
                
            try:
                action = MoveAction(curr_r, curr_c, target_r, target_c)
                game.process_action(action)
                turn_successful = True
            except Exception as e:
                input(f"\n[MOVIMIENTO INVÁLIDO] {e} (Presiona Enter para continuar...)")
        
        else:
            continue # Tecla equivocada, volvemos a pedir input sin gastar el turno
            
        # LÓGICA DE RESPAWN
        if turn_successful:
            turn_count += 1
            # Cada 4 turnos efectivos (2 rondas enteras de los 2 jugadores)
            if turn_count % 4 == 0:
                spawn_ingredients(board, 3) # Agregamos 3 ítems al mapa
                input("\n🌱 ¡Han brotado nuevos ingredientes en el mercado! (Presiona Enter para continuar...)")

if __name__ == "__main__":
    main()