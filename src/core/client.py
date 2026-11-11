class Client:
    def __init__(self, client_id: str, order_name: str, patience: int, reward: int):
        self.client_id = client_id      # Ej: "C1", "C2" (para mostrar en el tablero)
        self.order_name = order_name    # Ej: "Té Clásico"
        self.patience = patience        # Cantidad de turnos antes de irse enojado
        self.reward = reward            # Puntos que te da al entregarle el pedido
        self.is_active = True

    def tick(self):
        """Reduce la paciencia cada turno. Si llega a 0, el cliente se va."""
        if self.is_active:
            self.patience -= 1
            if self.patience <= 0:
                self.is_active = False