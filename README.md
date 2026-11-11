# Maestro Mezclador - Tactical Board Game Engine 🍵

Un motor de juego de mesa táctico por turnos desarrollado en Python. Este proyecto aplica principios estrictos de Ingeniería de Software para gestionar físicas de grilla, NPCs y recolección dinámica de recursos.

## 🚀 Arquitectura y Tecnologías
- **State Machines (NPCs):** Sistema de "Clientes" que actúan como máquinas de estado con contadores temporales de paciencia y pedidos dinámicos.
- **Patrón Command:** Lógica de inputs aislada mediante clases de acción (ej. `MoveAction`), separando el motor central de la interacción del usuario.
- **Generación Procedimental:** Algoritmos de distribución espacial para inicializar el tablero y sistema de *respawn* automático de recursos para mantener la economía del juego.
- **QA Automation:** Suite de pruebas unitarias automatizadas con `pytest` para garantizar la integridad de inventarios, crafteo y límites espaciales (13 tests pasando).

## 🎮 Cómo jugar
El objetivo es moverte por el salón, recolectar ingredientes, preparar tés específicos en tu bandeja y entregarlos a los clientes que esperan en los bordes del tablero antes de que se agote su paciencia.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/LucasHerrero04/maestro_mezclador.git
   ```

2. Crear entorno virtual e instalar dependencias (si las hubiera):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Ejecutar el juego:
   ```bash
   python -m src.main
   ```

## 🧪 Testing Automatizado
Para ejecutar la suite de control de calidad:
```bash
pytest
```