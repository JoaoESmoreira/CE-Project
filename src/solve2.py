

import random
import csv


class SEA:
    def __init__(self, lake, population_size=100,
                 #elite_percentage=0.1,
                 pool_percentage=0.1,
                 mutation_rate=0.1,
                 crossover_rate=0.8,
                 individual_size=500,
                 num_generations=1000
                 ) -> None:
        self.lake = lake
        self.population_size = population_size
        #self.elite_precentage = elite_percentage
        self.pool_percentage=pool_percentage
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.individual_size = individual_size
        #self.elite_size = int(self.elite_precentage * self.population_size)
        self.pool_size = max(int(self.pool_percentage * self.population_size), 1)
        self.lake_dimention = len(self.lake)

    def fit(self):
        population = self.initialize_population()

        for generation in range(self.num_generations):
            paths          = [self.mapping(individual) for individual in population]
            fitness_scores = [self.evaluate_individual(path) for path in paths]

            best_individual_index = fitness_scores.index(max(fitness_scores))
            best_individual = population[best_individual_index]

            offspring = [best_individual]
            while len(offspring) < self.population_size:
                parent1, parent2 = self.tornement_selection(population, fitness_scores)
                if random.random() < self.crossover_rate:
                    child1, child2 = self.uniform_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                if random.random() < self.mutation_rate:
                    child1 = self.mutate(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.mutate(child2)
                offspring.extend([child1, child2])
            population = offspring

        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_map              = paths[best_individual_index]
        population_fenotype   = [self.fenotype(individual) for individual in paths]
        return len(best_map), self.is_feasible(best_map), self.population_diversity(population), tuple(population_fenotype[best_individual_index])

    def fenotype(self, path):
        individual = []
        position = (0, 0)
        actions = {(0, -1):0, (1, 0):1, (0,1):2, (-1,0):3}
        for step in path:
            action = (step[0] - position[0], step[1] - position[1])
            if action in actions:
                individual.append(actions[action])
            #else:
            #    print("Hit the wall")
            position = step
        return individual

    def mapping(self, grid) -> list[tuple[int, int]]:
        individual = []
        visited = set()
        position = (0,0)
        while True:
            if grid[position[0]][position[1]] == 0:
                if position[1] != 0:
                    position = (position[0], position[1]-1)
            elif grid[position[0]][position[1]] == 1:
                if position[0] != n-1:
                    position = (position[0]+1, position[1])
            elif grid[position[0]][position[1]] == 2:
                if position[1] != n-1:
                    position = (position[0], position[1]+1)
            elif grid[position[0]][position[1]] == 3:
                if position[0] != 0:
                    position = (position[0]-1, position[1])
            if position == (n-1, n-1) or position in visited:
                individual.append(position)
                break
            # pay attention, if the agent hit the wall you will append the position twice anyway
            visited.add(position)
            individual.append(position)
        return individual

    def evaluate_individual(self, path) -> int:
        for i in range(len(path)):
            if mmap[path[i][0]][path[i][1]] == 'H':
                del path[i:]
                break

        if len(path) == 0:
            return -1000000
        return (path[-1][0] + path[-1][1])*2 \
           - (abs(path[-1][0] - (self.lake_dimention+1)) + \
           abs(path[-1][1] - (self.lake_dimention+1))) - \
           len(path) + self.is_feasible(path) * 40

    def is_feasible(self, path) -> bool:
        for step in path:
            if 0 <= step[0] < self.lake_dimention and 0 <= step[1] < self.lake_dimention:
                if mmap[step[0]][step[1]] == 'H':
                    return False
        if path[-1] != (self.lake_dimention-1, self.lake_dimention-1):
            return False
        return True

    def make_moves(self, cell):
        actions = [(0, -1), (1, 0), (0,1), (-1,0)]
        for i in range(len(actions)):
            new_state = (cell[0] + actions[i][0], cell[1] + actions[i][1])
            if 0 <= new_state[0] < self.lake_dimention and 0 <= new_state[1] < self.lake_dimention:
                yield i

    def init_solution(self) -> list[list[int]]:
        return [[random.choice(list(self.make_moves((i, j)))) for j in range(self.lake_dimention)] for i in range(self.lake_dimention)]

    def initialize_population(self) -> list[list[int]]:
        return [self.init_solution() for _ in range(self.population_size)]

    def select_survivors(self, population, fitness_scores) -> list[list[int]]:
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
        elite_indices = sorted_indices[:self.elite_size]
        return [population[idx] for idx in elite_indices]

    def tornement_selection(self, population, fitness_scores) -> list[list[int]]:
        pop_fit = [(population[i], fitness_scores[i]) for i in range(len(population))]
        parents = random.sample(pop_fit, self.pool_size)
        parents.sort(key=lambda element: element[1], reverse=True)
        return [parents[0][0], parents[1][0]]

    def uniform_crossover(self, parent1, parent2) -> tuple[list[list[int]], list[list[int]]]:
        child1 = [[0 for _ in range(self.lake_dimention)] for _ in range(self.lake_dimention)]
        child2 = [[0 for _ in range(self.lake_dimention)] for _ in range(self.lake_dimention)]
        for i in range(self.lake_dimention):
            for j in range(self.lake_dimention):
                if random.random() < 0.5:
                    child1[i][j] = parent1[i][j]
                    child2[i][j] = parent2[i][j]
                else:
                    child1[i][j] = parent2[i][j]
                    child2[i][j] = parent1[i][j]
        return child1, child2

    def mutate(self, individual) -> list[int]:
        for i in range(self.lake_dimention):
            for j in range(self.lake_dimention):
                if random.random() < self.mutation_rate:
                    #individual[i][j] = random.choice(list(self.make_moves((i, j))))
                    individual[i][j] = random.randint(0,3)
        return individual

    def hamming_distance(self, individual1, individual2):
        distance = 0
        for i in range(len(individual1)):
            for j in range(len(individual1)):
                distance += abs(individual1[i][j] - individual2[i][j])
        return distance
        return sum(abs(cell1 - cell2) for row1, row2 in zip(individual1, individual2) for cell1, cell2 in zip(row1, row2))

    def population_diversity(self, population):
        total_distance = 0
        num_pairs = 0
        for i in range(len(population)):
            for j in range(i+1, len(population)):
                total_distance += self.hamming_distance(population[i], population[j])
                num_pairs += 1
        return int(total_distance / num_pairs)


if __name__ == "__main__":
    seeds = [7123, 1287, 6372, 2651, 199, 9147, 6836, 9289, 8469, 4572, 2977, 7939, 3336, 6871, 182, 7840, 7325, 6427, 3349, 7321, 2930, 9756, 8457, 5584, 4797, 4613, 7269, 7247, 8908, 4259]
    pool_percentages = [0.05, 0.1, 0.15, 0.2]
    mutation_rates = [0.01, 0.05, 0.1, 0.15]
    crossover_rates = [0.7, 0.8, 0.9]
    dimentions = [4, 8, 12]
    individual_size = [100, 200, 500]
    m = 2

    for i in range(len(dimentions)):
        PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=dimentions[i], i=m)
        with open(PATH_MAP, "r", encoding='utf-8') as f:
            n = int(f.readline())
            mmap = []
            for _ in range(n):
                mmap.append(f.readline()[:-1])

        for pool in pool_percentages:
            for mutation in mutation_rates:
                for crossover in crossover_rates:

                    results = []
                    for seed in seeds:
                        random.seed(seed)
                        sea = SEA(mmap, pool_percentage=pool, mutation_rate=mutation, crossover_rate=crossover, individual_size=individual_size[i])
                        results.append(sea.fit())

                    OUTPUT_PATH = f"./output/qtable/dim{dimentions[i]}/map_0{m}_pool_{pool}_cross_{crossover}_mut_{mutation}.csv"
                    print(OUTPUT_PATH)
                    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',')
                        spamwriter.writerow(("fitness", "finished", "diversity", "individual"))
                        for result in results:
                            spamwriter.writerow((result[0], result[1], result[2], result[3]))
