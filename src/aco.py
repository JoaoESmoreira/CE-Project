
import random



class ACO:
    def __init__(self, lake, num_ants=10, evaporation_rate=0.5, alpha=1.0, beta=2.0, max_iterations=100):
        self.lake = lake
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha
        self.beta = beta
        self.max_iterations = max_iterations
        self.pheromones = [[1.00 for _ in range(len(self.lake)**2)] for _ in range(len(self.lake)**2)]
        self.target = (len(lake)-1, len(lake[0])-1)
        self.lake_dimention = len(lake)
        self.best_ant = None
        self.best_objective = None

    def fit(self):
        for generation in range(self.max_iterations):
            ants_population = []
            for ant in range(self.num_ants):
                ants_population.append(self.generate_ant())
            for ant in ants_population:
                if self.is_feasible(ant):
                    objective_value = self.objective(ant)
                    self.update_pheromones(ant, objective_value)
                    if self.best_ant is None or objective_value < self.best_objective:
                        self.best_ant = ant
                        self.best_objective = objective_value
            #print("Generation: ", generation, " Best: ", self.best_ant)
            for i in range(len(self.pheromones)):
                for j in range(len(self.pheromones[i])):
                    if self.pheromones[i][j] > 0.0000000001:
                        self.pheromones[i][j] *= self.evaporation_rate

    def is_feasible(self, ant):
        for i in range(len(ant)):
            cell = (ant[i] // self.lake_dimention, ant[i] % self.lake_dimention)
            if self.lake[cell[0]][cell[1]] == 'H':
                del ant[i:]
                return True
        return True
    
    def objective(self, ant):
        return 1.0 / len(ant) * 4
    
    def update_pheromones(self, ant, objective):
        for i in range(len(ant)):
            cell = (ant[i] // self.lake_dimention, ant[i] % self.lake_dimention)
            self.pheromones[cell[0]][cell[1]] += objective
            self.pheromones[cell[1]][cell[0]] += objective

    def generate_ant(self):
        solution = []
        source = 0
        while True:
            components = list(self.make_moves(source))
            if len(components) == 0:
                break
            probabilities = self.calculate_probabilities(components, source)
            source = random.choices(components, weights=probabilities, k=1)[0]
            solution.append(source)
        return solution

    def make_moves(self, state):
        cell = (state // self.lake_dimention, state % self.lake_dimention)
        # actions = [(0,1), (1,0), (0,-1), (-1,0)]
        actions = [(0,1), (1,0)] # just move foward or down
        for action in actions:
            new_state = (cell[0] + action[0], cell[1] + action[1])
            if 0 <= new_state[0] < self.lake_dimention and 0 <= new_state[1] < self.lake_dimention:
                yield new_state[0] * self.lake_dimention + new_state[1]

    def calculate_probabilities(self, possible_states, current_state):
        """
        p_xy = (pheromones_xy**alpha * (1/distance_xy)**tau) / sum( pheromones_xy * 1/distance_xy )
        p_xy = (pheromones_xy) / sum( pheromones_xy )
        Note: the distance from any x to any adjecent cell is 1.
        """
        pheromones = [self.pheromones[current_state][state] for state in possible_states]
        #print(pheromones)
        total_pheromones = sum(pheromones)
        return [pheromone/(total_pheromones) for pheromone in pheromones]


if __name__ == "__main__":
    lake = [
        ['S', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H'],
        ['F', 'F', 'F', 'H'],
        ['H', 'F', 'F', 'G']
    ]
    PATH_MAP = "./data/MAP_12_BY_12/input02.txt"
    with open(PATH_MAP, "r") as f:
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])

    c = 0
    for _ in range(30):
        aco = ACO(mmap, num_ants=100, max_iterations=1000)
        aco.fit()
        if aco.best_ant[-1] == 143:
            c +=1
        print("Best ant: ", aco.best_ant)
    print(c)
    #aco = ACO(lake)
    #aco = ACO(lake, num_ants=100, max_iterations=200)
    #aco = ACO(mmap, num_ants=100, max_iterations=1000)
    # aco.fit()
    # print("Best ant: ", aco.best_ant)
    # print(aco.pheromones[13][14])
    #for nn in aco.pheromones:
    #    print(nn)
    #print()

    # lake = np.array([
    #     ['S', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'H'],
    #     ['F', 'F', 'F', 'F', 'F', 'H', 'H', 'F', 'F', 'H', 'F', 'H'],
    #     ['H', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    #     ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'H'],
    #     ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F', 'H', 'F'],
    #     ['H', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'H', 'F', 'F', 'F'],
    #     ['H', 'H', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'F', 'H', 'F'],
    #     ['H', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'H'],
    #     ['F', 'F', 'F', 'F', 'F', 'H', 'H', 'F', 'F', 'F', 'F', 'F'],
    #     ['H', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'H', 'F', 'F', 'H'],
    #     ['F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F', 'H', 'H', 'F'],
    #     ['F', 'F', 'F', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'F', 'G']
    # ])