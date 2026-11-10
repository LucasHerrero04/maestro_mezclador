# Maestro Mezclador - Board Game Engine 🍵

Un motor de juego de mesa por turnos desarrollado en Python, con un enfoque estricto en la Ingeniería de Software, Programación Orientada a Objetos (POO) y control de calidad mediante pruebas automatizadas.

## 🚀 Arquitectura y Tecnologías
- **Patrón Command:** La lógica de movimiento y recolección está encapsulada en clases de acción (ej. `MoveAction`), separando las reglas del juego de los inputs del usuario.
- **Detección de Colisiones:** Sistema de validación espacial en una matriz 2D.
- **QA Automation:** Suite de 13 pruebas automatizadas construida con `pytest` para garantizar la integridad de la lógica de negocio (inventarios, turnos y límites del tablero).
- **Entorno aislado:** Gestión de dependencias nativa y control de versiones progresivo con Git.

## 🎮 Cómo jugar
El juego se ejecuta directamente en la terminal. El objetivo es recolectar hebras de té y especias para preparar recetas y ganar puntos de victoria.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/LucasHerrero04/maestro_mezclador.git
   ```
2. Crear y activar el entorno virtual, e instalar dependencias:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecutar el juego:
   ```bash
   python -m src.main
   ```

## 🧪 Testing
Para correr la suite de pruebas automatizadas, simplemente ejecuta:
```bash
pytest
```