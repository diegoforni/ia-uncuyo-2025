import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent

class RandomAgent(BaseAgent):
    """
    Agente que ejecuta acciones completamente aleatorias.
    
    Este agente elige una acción al azar entre todas las posibles
    en cada paso de la simulación.
    """
    
    def __init__(self, server_url="http://localhost:5000", **kwargs):
        super().__init__(server_url, "RandomAgent", **kwargs)  
    
    def get_strategy_description(self) -> str:
        """
        Descripción de la estrategia del agente aleatorio.
        """
        return "Random action selection - chooses actions completely at random"
    
    def think(self) -> bool:
        """
        Selecciona y ejecuta una acción completamente aleatoria.
        """

        if not self.is_connected():
            return False
            
        perception = self.get_perception()
        
        if not perception or perception.get('is_finished', True):  # Add 'not perception' check
            return False
        
        all_actions = [self.up, self.down, self.left, self.right, self.suck, self.idle]
        random_action = random.choice(all_actions)
        return random_action()


# Ejemplo de uso
if __name__ == "__main__":
    agent = RandomAgent(enable_ui=True, live_stats=True)
    
    if agent.connect_to_environment(sizeX=8, sizeY=8, dirt_rate=0.3):
        performance = agent.run_simulation(verbose=True)
        print(f"Final performance: {performance}")
        agent.disconnect()