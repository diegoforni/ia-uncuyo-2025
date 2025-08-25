"""Exploración básica del entorno FrozenLake."""

import gymnasium as gym


def main() -> None:
    env = gym.make("FrozenLake-v1", render_mode="human")
    state, _ = env.reset()
    print("Posición inicial del agente:", state)
    done = False
    truncated = False
    while not (done or truncated):
        action = env.action_space.sample()
        next_state, reward, done, truncated, _ = env.step(action)
        print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
        if reward != 1.0:
            print(f"¿Ganó? (encontró el objetivo): False")
            print(f"¿Perdió? (se cayó): {done}")
            print(f"¿Frenó? (alcanzó el máximo de pasos posible): {truncated}\n")
        else:
            print(f"¿Ganó? (encontró el objetivo): {done}")
        state = next_state


if __name__ == "__main__":
    main()
