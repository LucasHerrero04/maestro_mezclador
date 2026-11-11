import os
import random
from src.core.board import Board
from src.core.player import Player
from src.core.game import GameEngine
from src.core.recipe import Recipe
from src.actions.move import MoveAction
from src.core.client import Client

def find_player(board: Board, player_id: str):
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == player_id:
                return r, c
    return 0, 0

def place_randomly(board: Board, item: str):
    empty_cells = [(r, c) for r in range(board.rows) for c in range(board.cols) if board.get_item(r, c) == "."]
    if empty_cells:
        chosen_r, chosen_c = random.choice(empty_cells)
        board.place_item(chosen_r, chosen_c, item)

def spawn_ingredients(board: Board, amount: int):
    pool = ["N", "N", "N", "R", "R", "O", "M", "F", "C"]
    for _ in range(amount):
        place_randomly(board, random.choice(pool))

def get_empty_edge_cells(board: Board):
    edges = []
    for r in range(board.rows):
        for c in range(board.cols):
            if board.get_item(r, c) == ".":
                if r == 0 or r == board.rows - 1 or c == 0 or c == board.cols - 1:
                    edges.append((r, c))
    return edges

def spawn_client(board: Board, active_clients: dict, recipes: list, counter: int):
    edges = get_empty_edge_cells(board)
    if edges:
        r, c = random.choice(edges)
        client_id = f"C{counter}"
        recipe = random.choice(recipes)
        new_client = Client(client_id, recipe.name, random.randint(15, 20), recipe.points)
        active_clients[client_id] = new_client
        board.place_item(r, c, client_id)
        return counter + 1
    return counter

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
    
    place_randomly(board, "P1")
    place_randomly(board, "P2")
    spawn_ingredients(board, 12)
    
    active_clients = {}
    client_counter = 1
    
    # Aparecen 2 clientes al inicio
    client_counter = spawn_client(board, active_clients, recipes, client_counter)
    client_counter = spawn_client(board, active_clients, recipes, client_counter)
    
    turn_count = 0 
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = game.get_current_player()
        
        print(f"\n=== TURNO DE {current_player.name.upper()} ({current_player.player_id}) - PUNTAJE: {current_player.score} ===")
        
        bandeja = ", ".join(current_player.ready_teas) if current_player.ready_teas else "Vacía"
        print(f"Bandeja de entrega: [{bandeja}]")
        
        inv = current_player.inventory
        print(f"Bolsa: Negras({inv['hebras_negras']}) | Rojo({inv['te_rojo']}) | Rooibos({inv['rooibos']}) | Manza({inv['manzanilla']}) | Frutos({inv['frutos_rojos']}) | Canela({inv['canela']})")
        
        print("\nClientes esperando en los bordes:")
        for cid, client in active_clients.items():
            print(f"  [{cid}] Pide: {client.order_name} | Paciencia: {client.patience} turnos | Recompensa: {client.reward} pts")
            
        print("\nRecetas disponibles para cocinar (C):")
        for i, r in enumerate(recipes):
            print(f"  [{i+1}] {r.name} -> Requiere: {r.required_ingredients}")
            
        board.display()
        
        # ACÁ ESTÁ EL MENÚ CORREGIDO CON LA OPCIÓN 'E'
        print("Controles: W/A/S/D (Mover) | C (Cocinar) | E (Entregar) | Q (Salir)")
        move = input("Tu jugada: ").upper()
        
        turn_successful = False
        
        if move == 'Q':
            print("\n¡Hasta la próxima, Maestro Mezclador!")
            break
            
        elif move == 'C':
            print("¿Qué receta querés preparar? (Ingresá el número)")
            try:
                choice = int(input("> ")) - 1
                selected_recipe = recipes[choice]
                selected_recipe.craft(current_player)
                input(f"\n¡Cocinando! Pusiste {selected_recipe.name} en tu bandeja. Ahora llevalo al cliente. (Enter para seguir...)")
                game.advance_turn()  
                turn_successful = True
            except ValueError as e:
                input(f"\n[ERROR] {e} (Enter para seguir...)")
            except IndexError:
                input("\n[ERROR] Número de receta inexistente. (Enter para seguir...)")

        # ACÁ ESTÁ LA LÓGICA DE LA TECLA 'E' PERFECTAMENTE ALINEADA
        elif move == 'E':
            curr_r, curr_c = find_player(board, current_player.player_id)
            adjacents = [(curr_r-1, curr_c), (curr_r+1, curr_c), (curr_r, curr_c-1), (curr_r, curr_c+1)]
            delivered = False
            
            for r, c in adjacents:
                if 0 <= r < board.rows and 0 <= c < board.cols:
                    target_item = board.get_item(r, c)
                    if target_item in active_clients:
                        client = active_clients[target_item]
                        if client.order_name in current_player.ready_teas:
                            current_player.ready_teas.remove(client.order_name)
                            current_player.score += client.reward
                            board.place_item(r, c, ".")
                            del active_clients[target_item]
                            
                            input(f"\n¡Éxito! Entregaste {client.order_name} a {target_item} y ganaste {client.reward} puntos. (Enter para seguir...)")
                            game.advance_turn()
                            turn_successful = True
                            delivered = True
                            break
                        else:
                            input(f"\n[{target_item} se enoja] No tenés un '{client.order_name}' en tu bandeja. (Enter para seguir...)")
                            delivered = True
                            break
            
            if not delivered:
                input("\n[ERROR] No hay ningún cliente adyacente para entregarle nada. (Enter para seguir...)")
            continue
                
        elif move in ['W', 'A', 'S', 'D']:
            curr_r, curr_c = find_player(board, current_player.player_id)
            target_r, target_c = curr_r, curr_c
            
            if move == 'W': target_r -= 1
            elif move == 'S': target_r += 1
            elif move == 'A': target_c -= 1
            elif move == 'D': target_c += 1
                
            try:
                # FIX: Motor de colisiones para NPCs
                # Verificamos que el destino esté dentro del mapa antes de chequear qué hay
                if 0 <= target_r < board.rows and 0 <= target_c < board.cols:
                    celda_destino = board.get_item(target_r, target_c)
                    if celda_destino in active_clients:
                        raise ValueError("¡No podés pisar a los clientes! Dales su espacio.")
                        
                action = MoveAction(curr_r, curr_c, target_r, target_c)
                game.process_action(action)
                turn_successful = True
            except Exception as e:
                input(f"\n[MOVIMIENTO INVÁLIDO] {e} (Presiona Enter para continuar...)")
        else:
            continue
            
        if turn_successful:
            turn_count += 1
            if turn_count % 4 == 0:
                spawn_ingredients(board, 3) 
                input("\n🌱 ¡Han brotado nuevos ingredientes! (Enter para continuar...)")

if __name__ == "__main__":
    main()