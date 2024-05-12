# Copyright (C) 2024 João ES Moreira
#
#   __ _  ___ ___  
#  / _` |/ __/ _ \ 
# | (_| | (_| (_) |
#  \__,_|\___\___/ 


import random
import csv


def hamming_distance(individual1, individual2):
    min_len = min(len(individual1), len(individual2))
    max_len = max(len(individual1), len(individual2))

    distance = max_len - min_len
    for i in range(min_len):
        distance += abs(individual1[i] - individual2[i])
    return distance

def population_diversity(population):
    total_distance = 0
    num_pairs = 0
    for i in range(len(population)):
        for j in range(i+1, len(population)):
            total_distance += hamming_distance(population[i], population[j])
            num_pairs += 1
    return int(total_distance / num_pairs)


class ACO:
    def __init__(self, lake, num_ants=100, evaporation_rate=0.9, alpha=1.0, max_iterations=500, individual_size=500):
        self.lake = lake
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.individual_size = individual_size
        self.pheromones = [[1.00 for _ in range(4)] for _ in range(len(self.lake)**2)]
        self.target = (len(lake)-1, len(lake[0])-1)
        self.lake_dimention = len(lake)
        self.best_ant = None
        self.best_objective = None
        self.best_path = None

    def fit(self):
        for generation in range(self.max_iterations):
            ants_population = [self.generate_ant() for _ in range(self.num_ants)]
            path_population = [self.mapping(ant) for ant in ants_population]
            obje_population = [self.objective(ant) for ant in path_population]

            for i in range(len(ants_population)):
                ant = ants_population[i]
                obj = obje_population[i]
                path = path_population[i]
                self.update_pheromones(ant, path, obj)
                if self.best_ant is None or self.best_objective < obj:
                    self.best_ant = ant
                    self.best_objective = obj
                    self.best_path = path
            self.evaporate()
        if self.is_feasible(self.best_path):
            return (self.individual_size * (self.best_path[-1][0] + self.best_path[-1][1])) / len(self.best_path), True, population_diversity(ants_population), tuple(self.best_ant)
        return (self.best_path[-1][0] + self.best_path[-1][1]) / len(self.best_path), False, population_diversity(ants_population), tuple(self.best_ant)

        return len(self.best_ant), self.is_feasible(self.best_path), population_diversity(ants_population), tuple(self.best_ant)
        # if self.is_feasible(self.best_path):
        #     print("--- feasible: ", self.best_objective, " ", self.best_ant)
        # else:
        #     print("Not feasible: ", self.best_objective, " ", self.best_ant)

    # For visualization of pheromones
    def visualization(self):
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        from matplotlib.colors import Normalize
        import numpy as np
        min_val = np.min(self.pheromones)
        max_val = np.max(self.pheromones)
        #normalized_pheromones = (self.pheromones - min_val) / (max_val - min_val)
        normalized_pheromones = 2 * (self.pheromones - min_val) / (max_val - min_val) - 1


        self.pheromones = normalized_pheromones
        self.pheromones = -self.pheromones

        fig, ax = plt.subplots()
        #colormap = cm.ScalarMappable(cmap='viridis')
        #colormap.set_clim(np.min(-self.pheromones), np.max(-self.pheromones))
        colormap = cm.ScalarMappable(cmap='viridis', norm=Normalize(vmin=-1, vmax=1))
        colormap.set_clim(-1, 1)


        for i in range(self.lake_dimention-1):
            for j in range(self.lake_dimention):
                x = [i, i+1]
                y = [j-0.1, j-0.1]
                intensity = self.pheromones[i*self.lake_dimention + j][1]
                color = colormap.to_rgba(intensity)
                ax.plot(x, y, color=color)
        for i in range(self.lake_dimention):
            for j in range(self.lake_dimention-1):
                x = [i-0.1, i-0.1]
                y = [j, j+1]
                intensity = self.pheromones[i*self.lake_dimention + j][2]
                color = colormap.to_rgba(intensity)
                ax.plot(x, y, color=color)

        for i in range(self.lake_dimention-1):
            for j in range(self.lake_dimention):
                x = [i, i+1]
                y = [j+0.1, j+0.1]
                intensity = self.pheromones[i*self.lake_dimention + j][3]
                color = colormap.to_rgba(intensity)
                ax.plot(x, y, color=color)
        for i in range(self.lake_dimention):
            for j in range(self.lake_dimention-1):
                x = [i+0.1, i+0.1]
                y = [j, j+1]
                intensity = self.pheromones[i*self.lake_dimention + j][0]
                color = colormap.to_rgba(intensity)
                ax.plot(x, y, color=color)
        
        for i in range(self.lake_dimention):
            for j in range(self.lake_dimention):
                ax.scatter(i, j, color='red', zorder=10)

        ax.set_xlim(-0.5, self.lake_dimention)
        ax.set_ylim(-0.5, self.lake_dimention)
        ax.set_aspect('equal')
        ax.set_xticks(np.arange(self.lake_dimention))
        ax.set_yticks(np.arange(self.lake_dimention))
        ax.grid(True, linestyle='--', alpha=0.5)

        colormap = cm.ScalarMappable(cmap='viridis')
        colormap.set_clim(np.min(-self.pheromones), np.max(-self.pheromones))
        cbar = plt.colorbar(colormap, ax=ax)
        cbar.ax.invert_yaxis()
        cbar.ax.set_yticklabels(['1', '0.75', '0.5', '0.25', '0', '-0.25', '-0.5', '-0.75', '-1'])
        cbar.set_label('Intencidade da feromona')
        plt.show()

    def select_parents(self, population, fitness_scores):
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
        elite_indices = sorted_indices[:1]
        return elite_indices

    def mapping(self, individual) -> list[tuple[int, int]]:
        last_position = (0, 0)
        path = []
        for component in individual:
            if component == 0:
                last_position = (last_position[0], last_position[1]-1)
            elif component == 1:
                last_position = (last_position[0]+1, last_position[1])
            elif component == 2:
                last_position = (last_position[0], last_position[1]+1)
            elif component == 3:
                last_position = (last_position[0]-1, last_position[1])
            path.append(last_position)
        return path

    def is_feasible(self, ant):
        return ant[-1] == self.target
    
    def objective(self, ant):
        if len(ant) == 0:
            return 0
        return abs(ant[-1][0] + ant[-1][1])/len(ant) + self.is_feasible(ant)*10    #/ self.num_ants #+ self.is_feasible(ant)*10
    
    def update_pheromones(self, ant, path, objective):
        if len(path) == 0:
            return
        self.pheromones[0][ant[0]] += objective
        for i in range(len(path)-1):
            s = path[i][0] * self.lake_dimention + path[i][1]
            a = ant[i+1]
            self.pheromones[s][a] += objective

    def evaporate(self):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                if self.pheromones[i][j] > 1:
                    self.pheromones[i][j] *= self.evaporation_rate
                #if self.pheromones[i][j] > 1:
                #    self.pheromones[i][j] = 1

    def generate_ant(self):
        solution = []
        current_state = (0,0)
        previous_component = -10
        while True:
            components = list(self.make_moves(current_state, previous_component))
            if len(solution) >= self.individual_size or len(components) == 0:
                break
            
            probabilities = self.calculate_probabilities(components, current_state)
            action = random.choices(components, weights=probabilities, k=1)[0]
            previous_component = action
            current_state = self._component_plus_state(action, current_state)

            if self.lake[current_state[0]][current_state[1]] == 'H':
                break
            if current_state == self.target:
                solution.append(action)
                break
            solution.append(action)
        return solution
    
    def _component_plus_state(self, component, state):
        if component == 0:
            return (state[0], state[1] - 1)
        if component == 1:
            return (state[0] + 1, state[1])
        if component == 2:
            return (state[0], state[1] + 1)
        if component == 3:
            return (state[0] - 1, state[1])

    def make_moves(self, state, previous_component):
        unused = set(range(0,4))
        if state[0] == 0:
            unused.remove(3)
        if state[1] == 0:
            unused.remove(0)
        if state[0] == self.target[0]:
            unused.remove(1)
        if state[1] == self.target[1]:
            unused.remove(2)
        for move in unused:
            if abs(move - previous_component) != 2:
                yield move

    def calculate_probabilities(self, possible_states, current_state):
        """
        p_xy = (pheromones_xy**alpha * (1/distance_xy)**tau) / sum( pheromones_xy * 1/distance_xy )
        p_xy = (pheromones_xy) / sum( pheromones_xy )
        Note: the distance from any x to any adjecent cell is 1.
        """
        cell_state = current_state[0] * len(self.lake) + current_state[1]
        pheromones = [self.pheromones[cell_state][action]**self.alpha for action in possible_states]
        total_pheromones = sum(pheromones)
        return [pheromone/(total_pheromones) for pheromone in pheromones]


if __name__ == "__main__":

    PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=22, i=2)
    with open(PATH_MAP, "r", encoding='utf-8') as f:
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])

    aco = ACO(mmap, alpha=0.9, evaporation_rate=0.8, individual_size=500)
    print(aco.fit())
    #for i in range(10):
    #    PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=12, i=i)
    #    with open(PATH_MAP, "r", encoding='utf-8') as f:
    #        n = int(f.readline())
    #        mmap = []
    #        for _ in range(n):
    #            mmap.append(f.readline()[:-1])

    #    aco = ACO(mmap, alpha=0.9, evaporation_rate=0.8, individual_size=500)
    #    print(aco.fit())

    # PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=22, i=2)
    # with open(PATH_MAP, "r", encoding='utf-8') as f:
    #     n = int(f.readline())
    #     mmap = []
    #     for _ in range(n):
    #         mmap.append(f.readline()[:-1])
    # count = 0
    # for i in range(30):
    #     aco = ACO(mmap, alpha=0.9, evaporation_rate=0.8, individual_size=500)
    #     out = aco.fit()
    #     print(out)
    #     if out[1]:
    #         count += 1
    # print("total: ", count)

    # m = 2
    # dimentions = [4, 8, 12]
    # individual_size = [100, 200, 500]
    # seeds = [7123, 1287, 6372, 2651, 199, 9147, 6836, 9289, 8469, 4572, 2977, 7939, 3336, 6871, 182, 7840, 7325, 6427, 3349, 7321, 2930, 9756, 8457, 5584, 4797, 4613, 7269, 7247, 8908, 4259]

    # for i in range(len(dimentions)):
    #     PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=dimentions[i], i=m)
    #     with open(PATH_MAP, "r", encoding='utf-8') as f:
    #         n = int(f.readline())
    #         mmap = []
    #         for _ in range(n):
    #             mmap.append(f.readline()[:-1])

    #     evapuration_rates = [0.8, 0.9, 1]
    #     alpha_rates = [0.8, 0.9, 1]
    #     for evapuration in evapuration_rates:
    #         for alpha in alpha_rates:

    #             results = []
    #             for seed in seeds:
    #                 random.seed(seed)
    #                 aco = ACO(mmap, alpha=alpha, evaporation_rate=evapuration, individual_size=individual_size[i])
    #                 results.append(aco.fit())

    #             OUTPUT_PATH = f"./output/aco/dim{dimentions[i]}/map_0{m}_alpha_{alpha}_evap{evapuration}.csv"
    #             print(OUTPUT_PATH)
    #             with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    #                 spamwriter = csv.writer(csvfile, delimiter=',')
    #                 spamwriter.writerow(("fitness", "finished", "diversity", "individual"))
    #                 for result in results:
    #                     spamwriter.writerow((result[0], result[1], result[2], result[3]))
