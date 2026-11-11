import os
import random
from colorama import init, Fore, Back, Style
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

def render_board(board: Board):
    """Renderiza el tablero con colores usando Colorama para mejorar la UX de la terminal."""
    print("")
    for r in range(board.rows):
        row_str = ""
        for c in range(board.cols):
            item = board.get_item(r, c)
            if item == ".":
                row_str += Style.DIM + ".  " + Style.RESET_ALL
            elif item == "P1":
                row_str += Fore.CYAN + Style.BRIGHT + "P1 " + Style.RESET_ALL
            elif item == "P2":
                row_str += Fore.MAGENTA + Style.BRIGHT + "P2 " + Style.RESET_ALL
            elif item.startswith("C") and len(item) > 1:
                row_str += Back.WHITE + Fore.BLACK + f"{item:<2} " + Style.RESET_ALL
            else:
                # Colores para ingredientes
                color = Fore.YELLOW
                if item in ["R", "F"]: color = Fore.RED
                elif item == "N": color = Fore.LIGHTBLACK_EX
                elif item == "M": color = Fore.WHITE
                elif item == "C": color = Fore.GREEN
                
                row_str += color + f"{item}  " + Style.RESET_ALL
        print("  " + row_str)
    print("")

def main():
    # Inicializamos colorama para que limpie los colores automáticamente
    init(autoreset=True)
    
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
    client_counter = spawn_client(board, active_clients, recipes, client_counter)
    client_counter = spawn_client(board, active_clients, recipes, client_counter)
    
    turn_count = 0 
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_player = game.get_current_player()
        
        # Interfaz colorida
        header_color = Fore.CYAN if current_player.player_id == "P1" else Fore.MAGENTA
        print(header_color + Style.BRIGHT + f"\n=== TURNO DE {current_player.name.upper()} ({current_player.player_id}) - PUNTAJE: {current_player.score} ===")
        
        bandeja = ", ".join(current_player.ready_teas) if current_player.ready_teas else "Vacía"
        print(Fore.YELLOW + f"Bandeja de entrega: [{bandeja}]")
        
        inv = current_player.inventory
        print(Fore.WHITE + f"Bolsa: Negras({inv['hebras_negras']}) | Rojo({inv['te_rojo']}) | Rooibos({inv['rooibos']}) | Manza({inv['manzanilla']}) | Frutos({inv['frutos_rojos']}) | Canela({inv['canela']})")
        
        print(Style.BRIGHT + "\nClientes esperando:")
        for cid, client in active_clients.items():
            urgency = Fore.RED if client.patience <= 5 else Fore.GREEN
            print(f"  {Back.WHITE}{Fore.BLACK} {cid} {Style.RESET_ALL} Pide: {Fore.YELLOW}{client.order_name}{Style.RESET_ALL} | Paciencia: {urgency}{client.patience} turnos{Style.RESET_ALL} | Premio: {Fore.GREEN}{client.reward} pts")
            
        print("\nRecetas (Presiona C para cocinar):")
        for i, r in enumerate(recipes):
            print(f"  [{i+1}] {r.name} -> {r.required_ingredients}")
            
        # Llamamos al nuevo renderizador en vez de board.display()
        render_board(board)
        
        print(Style.DIM + "Controles: W/A/S/D (Mover) | C (Cocinar) | E (Entregar) | Q (Salir)")
        move = input("> Tu jugada: ").upper()
        
        turn_successful = False
        
        if move == 'Q':
            print(Fore.CYAN + "\n¡Hasta la próxima, Maestro Mezclador!")
            break
            
        elif move == 'C':
            print("¿Qué receta querés preparar? (Ingresá el número)")
            try:
                choice = int(input("> ")) - 1
                selected_recipe = recipes[choice]
                selected_recipe.craft(current_player)
                input(Fore.GREEN + f"\n¡Cocinando! Pusiste {selected_recipe.name} en tu bandeja. (Enter para seguir...)")
                game.advance_turn()  
                turn_successful = True
            except ValueError as e:
                input(Fore.RED + f"\n[ERROR] {e} (Enter para seguir...)")
            except IndexError:
                input(Fore.RED + "\n[ERROR] Número de receta inexistente. (Enter para seguir...)")
                
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
                            
                            input(Fore.GREEN + f"\n¡Éxito! Entregaste {client.order_name} a {target_item} y ganaste {client.reward} pts. (Enter para seguir...)")
                            game.advance_turn()
                            turn_successful = True
                            delivered = True
                            break
                        else:
                            input(Fore.RED + f"\n[{target_item} se enoja] No tenés '{client.order_name}' en tu bandeja. (Enter para seguir...)")
                            delivered = True
                            break
            
            if not delivered:
                input(Fore.RED + "\n[ERROR] No hay ningún cliente adyacente para entregarle. (Enter para seguir...)")
            continue
                
        elif move in ['W', 'A', 'S', 'D']:
            curr_r, curr_c = find_player(board, current_player.player_id)
            target_r, target_c = curr_r, curr_c
            
            if move == 'W': target_r -= 1
            elif move == 'S': target_r += 1
            elif move == 'A': target_c -= 1
            elif move == 'D': target_c += 1
                
            try:
                if 0 <= target_r < board.rows and 0 <= target_c < board.cols:
                    if board.get_item(target_r, target_c) in active_clients:
                        raise ValueError("¡No podés pisar a los clientes! Dales su espacio.")
                        
                action = MoveAction(curr_r, curr_c, target_r, target_c)
                game.process_action(action)
                turn_successful = True
            except Exception as e:
                input(Fore.RED + f"\n[MOVIMIENTO INVÁLIDO] {e} (Enter para continuar...)")
        else:
            continue
            
        if turn_successful:
            turn_count += 1
            
            clientes_enojados = []
            for cid, client in active_clients.items():
                client.tick() 
                if not client.is_active: 
                    clientes_enojados.append(cid)
            
            for cid in clientes_enojados:
                for r in range(board.rows):
                    for c in range(board.cols):
                        if board.get_item(r, c) == cid:
                            board.place_item(r, c, ".")
                del active_clients[cid] 
                print(Fore.RED + f"\n[!] El cliente {cid} se cansó de esperar y se fue dando un portazo.")
            
            if clientes_enojados:
                input(Style.DIM + "(Enter para continuar...)")
                
            if turn_count % 4 == 0:
                spawn_ingredients(board, 3) 
                input(Fore.GREEN + "\n🌱 ¡Han brotado nuevos ingredientes! (Enter para continuar...)")
                
            if len(active_clients) == 0 or (turn_count % 5 == 0 and len(active_clients) < 3):
                client_counter = spawn_client(board, active_clients, recipes, client_counter)
                input(Fore.YELLOW + "\n🔔 ¡Din don! Ha llegado un nuevo cliente. (Enter para continuar...)")
                
            if current_player.score >= 100:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.YELLOW + Style.BRIGHT + "\n" + "="*60)
                print(f"🏆 ¡EL JUEGO HA TERMINADO! 🏆")
                print(f"¡Felicidades, {current_player.name.upper()} ({current_player.player_id})!")
                print(f"Has superado los 100 puntos (Total: {current_player.score}) y")
                print("te coronas como el MAESTRO MEZCLADOR definitivo.")
                print("="*60 + "\n")
                break

if __name__ == "__main__":
    main()