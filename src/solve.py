
import random
import csv


class SEA:
    def __init__(self, lake, 
                 #elite_percentage=0.1, 
                 pool_percentage=0.1,
                 mutation_rate=0.1, 
                 crossover_rate=0.8, 
                 population_size=100, 
                 individual_size=500,
                 num_generations=1000 
                 ) -> None:
        self.lake = lake
        self.population_size = population_size
        #self.elite_percentage = elite_percentage
        self.pool_percentage = pool_percentage
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.individual_size = individual_size
        #self.elite_size = max(int(self.elite_percentage * self.population_size), 1)
        self.pool_size = max(int(self.pool_percentage * self.population_size), 1)
        self.lake_dimention = len(self.lake)

    def fit(self):
        #f1 = create_interactive_plot('Best fitness...', 'Iteration', 'Quality', (0, 1000), (-100, 100))
        #f2 = create_interactive_plot('Avg fitness...', 'Iteration', 'Quality', (0, 1000), (-100, 100))
        population = self.initialize_population()
        for generation in range(self.num_generations):
            fitness_scores = [self.evaluate_individual(individual) for individual in population]
            #update_graph(generation, best_fitness, *f1)
            #update_graph(generation, sum(fitness_scores) / len(fitness_scores), *f2)

            #offspring = [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(10)]
            best_individual_index = fitness_scores.index(max(fitness_scores))
            best_individual = population[best_individual_index]
            offspring = [best_individual]
            while len(offspring) < self.population_size:
                #parent1, parent2 = random.sample(parents, 2)
                parent1, parent2 = self.tornement_selection(population, fitness_scores)
                if random.random() < self.crossover_rate:
                    child1, child2 = self.two_point_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2
                if random.random() < self.mutation_rate:
                    child1 = self.mutate(child1, self.mutation_rate)
                if random.random() < self.mutation_rate:
                    child2 = self.mutate(child2, self.mutation_rate)
                offspring.extend([child1, child2])
            population = offspring
        # find the best individual
        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]
        #best_fitness = fitness_scores[best_individual_index]
        return len(best_individual), self.is_feasible(best_individual), self.population_diversity(population), tuple(best_individual)
    
    def mapping(self, individual) -> list[tuple[int, int]]:
        last_position = (0, 0)
        path = []
        for component in individual:
            if component == 0:
                if last_position[1] != 0:
                    last_position = (last_position[0], last_position[1]-1)
            elif component == 1:
                if last_position[0] != n-1:
                    last_position = (last_position[0]+1, last_position[1])
            elif component == 2:
                if last_position[1] != n-1:
                    last_position = (last_position[0], last_position[1]+1)
            elif component == 3:
                if last_position[0] != 0:
                    last_position = (last_position[0]-1, last_position[1])
            path.append(last_position)
        return path

    def evaluate_individual(self, individual) -> int:
        path = self.mapping(individual)
        for i in range(len(path)):
            if self.lake[path[i][0]][path[i][1]] == 'H':
                del individual[i:]
                del path[i:]
                break
        
        if len(path) == 0:
            return -1000000
        if not self.is_feasible(path):
            return (path[-1][0] + path[-1][1])*2 
        else:
            return (path[-1][0] + path[-1][1])*2 - (abs(path[-1][0] - (self.lake_dimention+1)) + abs(path[-1][1] - (self.lake_dimention+1))) - len(path) + self.is_feasible(individual)*40     # best fitness in general

    def is_feasible(self, individual) -> bool:
        path = self.mapping(individual)
        for step in path:
            if 0 <= step[0] < n and 0 <= step[1] < n:
                if self.lake[step[0]][step[1]] == 'H':
                    return False
        if path[-1] == (self.lake_dimention-1, self.lake_dimention-1):
            return True
        return False

    def initialize_population(self) -> list[list[int]]:
        return [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(self.population_size)]

    def tornement_selection(self, population, fitness_scores) -> list[list[int]]:
        pop_fit = [(population[i], fitness_scores[i]) for i in range(len(population))]
        pool = random.sample(pop_fit, self.pool_size)
        pool.sort(key=lambda element: element[1], reverse=True)
        return [pool[0][0], pool[1][0]]

    def one_point_crossover(self, parent1, parent2) -> tuple[list[int], list[int]]:
        crossover_point = random.randint(0, min(len(parent1), len(parent2)))
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def two_point_crossover(self, parent1, parent2) -> tuple[list[int], list[int]]:
        length = min(len(parent1), len(parent2))
        point1 = random.randint(0, length)
        point2 = random.randint(0, length)
        if point1 > point2:
            point1, point2 = point2, point1
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2

    def mutate(self, individual, mutation_rate) -> list[int]:
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.randint(0, 3)
        if random.random() < 0.8 and len(individual) < self.individual_size:
            path = self.mapping(individual)
            if len(path) > 0:
                number_steps = min(abs(path[-1][0] - n), abs(path[-1][1] - self.lake_dimention))*10
                for _ in range(random.randint(1, number_steps)):
                    individual.append(random.randint(0, 3))
            else:
                for _ in range(n):
                    individual.append(random.randint(0, 3))
        return individual

    def final_evaluation(self, individual):
        return len(individual), self.is_feasible(individual)

    def hamming_distance(self, individual1, individual2):
        min_len = min(len(individual1), len(individual2))
        max_len = max(len(individual1), len(individual2))
        
        distance = max_len - min_len
        for i in range(min_len):
            distance += abs(individual1[i] - individual2[i])
        return distance

    def population_diversity(self, population):
        total_distance = 0
        num_pairs = 0
        for i in range(len(population)):
            for j in range(i+1, len(population)):
                total_distance += self.hamming_distance(population[i], population[j])
                num_pairs += 1
        return int(total_distance / num_pairs)
    

if __name__ == "__main__":
    pool_percentages = [0.05, 0.1, 0.15, 0.2]
    mutation_rates = [0.01, 0.05, 0.1, 0.15]
    crossover_rates = [0.7, 0.8, 0.9]
    individual_size = [100, 200, 500]
    dimentions = [4, 8, 12]
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
                    for _ in range(30):
                        sea = SEA(mmap, pool_percentage=pool, mutation_rate=mutation, crossover_rate=crossover, individual_size=individual_size[i])
                        results.append(sea.fit())

                    OUTPUT_PATH = f"./output/sea/dim{dimentions[i]}/map_0{m}_pool_{pool}_cross_{crossover}_mut_{mutation}.csv"
                    print(OUTPUT_PATH)
                    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',')
                        spamwriter.writerow(("fitness", "finished", "diversity", "individual"))
                        for result in results:
                            spamwriter.writerow((result[0], result[1], result[2], result[3]))

