
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from math import sqrt

class MaxIterations:
    MAX_ITERATIONS_4_by_4 = 100
    MAX_ITERATIONS_8_by_8 = 200
    MAX_ITERATIONS_12_by_12 = 500

SEED = 42

PATH_MAP_4_BY_4 = "./data/MAP_4_BY_4/input01.txt"
PATH_MAP_8_BY_8 = "./data/MAP_8_BY_8/input01.txt"
PATH_MAP_12_BY_12 = "./data/MAP_12_BY_12/input01.txt"

def write_maps() -> None:
    map_4_by_4   = "\n".join(generate_random_map(size=4,  seed=SEED)) + "\n"
    map_8_by_8   = "\n".join(generate_random_map(size=8,  seed=SEED)) + "\n"
    map_12_by_12 = "\n".join(generate_random_map(size=12, seed=SEED)) + "\n"

    files = [PATH_MAP_4_BY_4, PATH_MAP_8_BY_8, PATH_MAP_12_BY_12]
    maps = [map_4_by_4, map_8_by_8, map_12_by_12]
    sizes = [4, 8, 12]
    for i in range(len(files)):
        with open(files[i], 'w') as f:
            f.write(str(sizes[i]) + "\n")
            f.write(maps[i])
