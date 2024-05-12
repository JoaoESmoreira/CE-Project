# Copyright (C) 2024 João ES Moreira
#                                        _                 
#   __ _ _   _ _ __ ___  _ __   __ _ ___(_)_   _ _ __ ___  
#  / _` | | | | '_ ` _ \| '_ \ / _` / __| | | | | '_ ` _ \ 
# | (_| | |_| | | | | | | | | | (_| \__ \ | |_| | | | | | |
#  \__, |\__, |_| |_| |_|_| |_|\__,_|___/_|\__,_|_| |_| |_|
#  |___/ |___/                                             


from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from math import sqrt

class MaxIterations:
    MAX_ITERATIONS_4_by_4 = 100
    MAX_ITERATIONS_8_by_8 = 200
    MAX_ITERATIONS_12_by_12 = 500

SEED = 40

def write_maps() -> None:
    for i in range(10):
        PATH_MAP_4_BY_4 = "./data/MAP_4_BY_4/input0{i}.txt".format(i=i)
        PATH_MAP_8_BY_8 = "./data/MAP_8_BY_8/input0{i}.txt".format(i=i)
        PATH_MAP_12_BY_12 = "./data/MAP_12_BY_12/input0{i}.txt".format(i=i)

        map_4_by_4   = "\n".join(generate_random_map(size=4,  seed=SEED+i)) + "\n"
        map_8_by_8   = "\n".join(generate_random_map(size=8,  seed=SEED+i)) + "\n"
        map_12_by_12 = "\n".join(generate_random_map(size=12, seed=SEED+i)) + "\n"

        files = [PATH_MAP_4_BY_4, PATH_MAP_8_BY_8, PATH_MAP_12_BY_12]
        maps = [map_4_by_4, map_8_by_8, map_12_by_12]
        sizes = [4, 8, 12]
        for i in range(len(files)):
            with open(files[i], 'w') as f:
                f.write(str(sizes[i]) + "\n")
                f.write(maps[i])

def write_maps_22() -> None:
    PATH_MAP_22_BY_22 = "./data/MAP_22_by_22input0{i}.txt".format(i=2)
    map_22_by_22 = "\n".join(generate_random_map(size=12, seed=2)) + "\n"

    with open(PATH_MAP_22_BY_22, 'w') as f:
        f.write(str(22) + "\n")
        f.write(map_22_by_22)

if __name__ == "__main__":
    write_maps_22()