
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import random

map_4_by_4 = generate_random_map(size=4, seed=42)
map_8_by_8 = generate_random_map(size=8, seed=41)
map_12_by_12 = generate_random_map(size=12, seed=41)

MAX_ITERATIONS_4_by_4 = 100
MAX_ITERATIONS_8_by_8 = 200
MAX_ITERATIONS_12_by_12 = 500

if __name__ == "__main__":
    fenotype =  [2, 1, 1, 2, 1, 2]
    my_map = generate_random_map(size=4, seed=47)

    RENDER_MODE = 'human'
    env = gym.make('FrozenLake-v1', desc=my_map, is_slippery=False, render_mode=RENDER_MODE)
    observation, info = env.reset(seed=42)
    if RENDER_MODE is not None:
        env.render()

    for action in fenotype:
        observation, reward, terminated, truncated, info = env.step(action)
        print(action, observation, reward, terminated, truncated, info)
        #print(action, observation, reward, terminated, truncated, info)
        if RENDER_MODE is not None:
            env.render()
        if terminated:
            break
