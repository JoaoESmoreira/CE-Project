
import random


mmap = []
n = None
num_actions = list(range(4))


population_size = 100
num_generations = 1000
elite_percentage = 0.1
mutation_rate = 0.1
crossover_rate = 0.8
individual_size = 200
elite_size = int(elite_percentage * population_size)


def fenotype(grid) -> list[int]:
    individual = []
    visited = set()
    position = (0,0)
    component = None
    while True:
        if grid[position[0]][position[1]] == 0:
            if position[1] != 0:
                position = (position[0], position[1]-1)
                component = 0
        elif grid[position[0]][position[1]] == 1:
            if position[0] != n-1:
                position = (position[0]+1, position[1])
                component = 1
        elif grid[position[0]][position[1]] == 2:
            if position[1] != n-1:
                position = (position[0], position[1]+1)
                component = 2
        elif grid[position[0]][position[1]] == 3:
            if position[0] != 0:
                position = (position[0]-1, position[1])
                component = 3
        if position == (n-1, n-1) or position in visited:
            break
        visited.add(position)
        individual.append(component)
    return individual

def mapping(grid):
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
            break
        visited.add(position)
        individual.append(position)
    return individual

def evaluate_individual(path) -> int:
    for i in range(len(path)):
        if mmap[path[i][0]][path[i][1]] == 'H':
            del path[i:]
            break
    
    if len(path) == 0:
        return -1000000
    return (path[-1][0] + path[-1][1])*2 - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) - len(path)

def is_feasible(path) -> bool:
    for step in path:
        if 0 <= step[0] < n and 0 <= step[1] < n:
            if mmap[step[0]][step[1]] == 'H':
                return False
    if path[-1] != (n-1, n-1):
        return False
    return True

def make_moves(cell):
    actions = [(0, -1), (1, 0), (0,1), (-1,0)]
    for i in range(len(actions)):
        new_state = (cell[0] + actions[i][0], cell[1] + actions[i][1])
        if 0 <= new_state[0] < n and 0 <= new_state[1] < n:
            yield i

def init_solution() -> list[list[int]]:
    return [[random.choice(list(make_moves((i, j)))) for j in range(n)] for i in range(n)]

def initialize_population() -> list[list[int]]:
    return [init_solution() for _ in range(population_size)]

def select_parents(population, fitness_scores) -> list[list[int]]:
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
    elite_indices = sorted_indices[:elite_size]
    return [population[idx] for idx in elite_indices]

def tornement_selection(population, fitness_scores) -> list[list[int]]:
    pop_fit = [(population[i], fitness_scores[i]) for i in range(len(population))]
    parents = random.sample(pop_fit, elite_size)
    parents.sort(key=lambda element: element[1], reverse=True)
    return [parents[0][0], parents[1][0]]

def crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    crossover_point = random.randint(0, min(len(parent1), len(parent2)))
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def two_point_crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    length = min(len(parent1), len(parent2))
    point1 = random.randint(0, length)
    point2 = random.randint(0, length)
    if point1 > point2:
        point1, point2 = point2, point1
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

def mutate(individual, mutation_rate) -> list[int]:
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(1, 2)
    if random.random() < 0.8 and len(individual) < individual_size:
        path = mapping(individual)
        if len(path) > 0:
            number_steps = min(abs(path[-1][0] - n), abs(path[-1][1] - n))
            for i in range(random.randint(1, number_steps)):
                individual.append(random.randint(1, 2))
        else:
            for i in range(n):
                individual.append(random.randint(1, 2))
    return individual

def sea():
    population = initialize_population()
    fitness_scores = [evaluate_individual(individual) for individual in population]
    best_individual_index = fitness_scores.index(max(fitness_scores))
    best_individual = fenotype(population[best_individual_index])
    best_fitness = fitness_scores[best_individual_index]

    print(fitness_scores)
    print(best_individual)
    print(best_fitness)
    #for generation in range(num_generations):
    #    fitness_scores = [evaluate_individual(individual) for individual in population]
    #    best_individual_index = fitness_scores.index(max(fitness_scores))
    #    best_individual = population[best_individual_index]
    #    best_fitness = fitness_scores[best_individual_index]

    #    offspring = [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(10)]
    #    while len(offspring) < population_size:
    #        parent1, parent2 = tornement_selection(population, fitness_scores)
    #        if random.random() < crossover_rate:
    #            child1, child2 = tow_point_crossover(parent1, parent2)
    #        else:
    #            child1, child2 = parent1, parent2
    #        if random.random() < mutation_rate:
    #            child1 = mutate(child1, mutation_rate)
    #        if random.random() < mutation_rate:
    #            child2 = mutate(child2, mutation_rate)
    #        offspring.extend([child1, child2])
    #    population = offspring
    #best_individual_fitness = evaluate_individual(best_individual)
    #if is_feasible(best_individual):
    #    print("--- Feasible Individual Actions: {fitness}".format(fitness=best_individual_fitness), best_individual)
    #    return True
    #else:
    #    print("Not Feasible Individual Actions: {fitness}".format(fitness=best_individual_fitness), best_individual)
    #    return False

def random_with_random_restart():
    best_fitness = -100000
    best_individual = None
    best_map = None

    for _ in range(num_generations):
        population     = initialize_population()
        paths          = [mapping(individual) for individual in population]
        fitness_scores = [evaluate_individual(path) for path in paths]

        current_best_individual_index = fitness_scores.index(max(fitness_scores))
        current_best_individual       = population[current_best_individual_index]
        current_best_fitness          = fitness_scores[current_best_individual_index]
        current_best_path             = paths[current_best_individual_index]

        if best_individual is None or best_fitness < current_best_fitness:
            best_map        = current_best_path
            best_fitness    = current_best_fitness
            best_individual = current_best_individual

    if is_feasible(best_map):
        print("--- Feasible Individual Actions: {fitness}".format(fitness=best_fitness), fenotype(best_individual))
        return True
    else:
        print("Not feasible Individual Actions: {fitness}".format(fitness=best_fitness), fenotype(best_individual))
        return False


if __name__ == "__main__":
    PATH_MAP = "./data/MAP_4_BY_4/input02.txt"
    with open(PATH_MAP, "r") as f:
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])
    random_with_random_restart()
