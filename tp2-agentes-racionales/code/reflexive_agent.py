import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent

class reflexiveAgent(BaseAgent):
    def __init__(self, server_url="http://localhost:5000", **kwargs):
        super().__init__(server_url, "reflexiveAgent", **kwargs)
        
        self.action_map = {
            0: self.up,
            1: self.down,
            2: self.left,
            3: self.right,
        }
    
    def get_strategy_description(self):
        return "If the current spot is dirty, clean it. Otherwise, move in a random direction."
    
    def think(self):
        if not self.is_connected():
            return False
        
        perception = self.get_perception()
        if not perception or perception.get('is_finished', True):
            return False
        
        if perception.get('is_dirty', False):
            return self.suck()
        else:
            random_key = random.randint(0, 3)
            action_to_perform = self.action_map[random_key]
            return action_to_perform()

if __name__ == "__main__":
    agent = reflexiveAgent(enable_ui=True, live_stats=True)
    
    if agent.connect_to_environment(sizeX=8, sizeY=8, dirt_rate=0.3):
        performance = agent.run_simulation(verbose=True)
        print(f"Final performance: {performance}")
        agent.disconnect()