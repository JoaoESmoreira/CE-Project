
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


def mapping(individual) -> list[tuple[int, int]]:
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

def repeted_cells(path) -> int:
    path = path.copy()
    repeted = 0
    for cell in path:
        repeted += path.count(cell)
        path = list(filter((cell).__ne__, path))
    return repeted

def evaluate_individual(individual) -> int:
    path = mapping(individual)
    count = 0
    for i in range(len(path)):
        if mmap[path[i][0]][path[i][1]] == 'H':
            del individual[i:]
            del path[i:]
            break
    
    if len(path) == 0:
        return -1000000#path.append((0,0))
    #return 1/(1 + (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1)) + count ) ) * 10 

    #return (path[-1][0] + path[-1][1])*n - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) + is_feasible(individual)*200 - len(individual)
    #return (path[-1][0] + path[-1][1])*n - count*20 - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1)))*5 + is_feasible(individual)*200 - len(individual)
    #return (path[-1][0] + path[-1][1])*n - count*20 + is_feasible(individual)*400
    #return (path[-1][0]*2 + path[-1][1])*2 - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) - len(path)
    return (path[-1][0] + path[-1][1])*2 - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) - len(path)      # best fitness in general
    #return (path[-1][0] + path[-1][1])*n - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) + is_feasible(individual)*200 - len(individual)
    #return (path[-1][0] + path[-1][1])*2 - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) - len(path)
    #return (path[-1][0] + path[-1][1])*2 - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1)))

    fitness = 0
    if count == 0 and len(path) > 0:
        # fitness = len(individual)
        # fitness = (path[-1][0] + path[-1][1])*10 + len(individual)*3 - repeted_cells(path)*2
        fitness = path[-1][0] + path[-1][1] + len(individual)
        if path[-1] == (n-1, n-1):
            fitness = abs(fitness - len(individual)) * 10 - len(individual)
    else:
        fitness = -count
    return fitness

def is_feasible(individual) -> bool:
    path = mapping(individual)
    for step in path:
        if 0 <= step[0] < n and 0 <= step[1] < n:
            if mmap[step[0]][step[1]] == 'H':
                return False
    if path[-1] == (n-1, n-1):
        return True
    return False

def initialize_population() -> list[list[int]]:
    return [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(population_size)]

def select_parents(population, fitness_scores) -> list[list[int]]:
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
    elite_indices = sorted_indices[:elite_size]
    return [population[idx] for idx in elite_indices]

#def select_parents(population, fitness_scores, elite_percentage):
#    tournament_size = int(elite_percentage * len(population))
#    parents = []
#    while len(parents) < len(population):
#        tournament_indices = random.sample(range(len(population)), tournament_size)
#        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
#        winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
#        parents.append(population[winner_index])
#    print(parents)
#    return parents

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

def tow_point_crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    length = min(len(parent1), len(parent2))
    point1 = random.randint(0, length)
    point2 = random.randint(0, length)
    if point1 > point2:
        point1, point2 = point2, point1
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

def uniforme_crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    child1 = []
    child2 = []
    size = min(len(parent1), len(parent2))
    for i in range(size):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    if len(parent1) > len(parent2):
        child1.append(parent1[size-1:])
        child2.append(parent1[size-1:])
    else:
        child1.append(parent2[size-1:])
        child2.append(parent2[size-1:])
    return child1, child2

# def mutate(individual, mutation_rate) -> list[int]:
#     for i in range(len(individual)):
#         if random.random() < mutation_rate:
#             individual[i] = random.randint(0, 3)
#     #while random.random() < 0.5 and len(individual) < individual_size:
#     #    individual.append(random.randint(0, 3))
#     if random.random() < mutation_rate and len(individual) > 0:
#         #individual.pop(random.randint(0, len(individual)-1))
#         individual = individual[:int(len(individual)//2)]
#     if random.random() < 0.5 and len(individual) < individual_size:
#         path = mapping(individual)
#         if len(path) > 0:
#             number_steps = min(abs(path[-1][0] - n), abs(path[-1][1] - n))
#             for i in range(random.randint(1, number_steps)):
#                 individual.append(random.randint(0, 3))
#         else:
#             for i in range(n):
#                 individual.append(random.randint(0, 3))
#     return individual

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

## import matplotlib.pyplot as plt 
## import numpy as np
## def create_interactive_plot(title, xlabel, ylabel, lim_x, lim_y):
##     plt.ion()
##     # creating subplot and figure
##     fig = plt.figure()
##     ax = fig.add_subplot(111)
##     ax.set_ylim(*lim_y)
##     ax.set_xlim(*lim_x)
##     line1, = ax.plot([], [])
##     # setting labels
##     plt.xlabel(xlabel)
##     plt.ylabel(ylabel)
##     plt.title(title)
##     return line1, fig, ax
## 
## def update_graph(x, y, graph, fig, ax):
##     graph.set_xdata(np.append(graph.get_xdata(), x))
##     graph.set_ydata(np.append(graph.get_ydata(), y))
##     ax.draw_artist(ax.patch)
##     ax.draw_artist(graph)
##     fig.canvas.draw()
##     fig.canvas.flush_events()

from collections import defaultdict
def find_identical_sublists(list_of_lists):
    groups = defaultdict(list)

    for idx, sublist in enumerate(list_of_lists):
        sublist_tuple = tuple(sublist)
        groups[sublist_tuple].append(idx)
    identical_groups = {sublist_tuple: indexes for sublist_tuple, indexes in groups.items() if len(indexes) > 10}
    return identical_groups

def sea():
    #f1 = create_interactive_plot('Best fitness...', 'Iteration', 'Quality', (0, 1000), (-100, 100))
    #f2 = create_interactive_plot('Avg fitness...', 'Iteration', 'Quality', (0, 1000), (-100, 100))
    population = initialize_population()
    for generation in range(num_generations):
        fitness_scores = [evaluate_individual(individual) for individual in population]
        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]
        best_fitness = fitness_scores[best_individual_index]

        # identical_individuals = find_identical_sublists(population)
        # for sublist, indexes in identical_individuals.items():
        #     for i in indexes:
        #         if random.random() < mutation_rate:
        #             population[i] = mutate(population[i], mutation_rate)

        #update_graph(generation, best_fitness, *f1)
        #update_graph(generation, sum(fitness_scores) / len(fitness_scores), *f2)

        #parents = select_parents(population, fitness_scores, elite_percentage)
        #offspring = random.sample(population, elite_size)
        offspring = [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(10)]
        while len(offspring) < population_size:
            #parent1, parent2 = random.sample(parents, 2)
            parent1, parent2 = tornement_selection(population, fitness_scores)
            if random.random() < crossover_rate:
                child1, child2 = uniforme_crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            if random.random() < mutation_rate:
                child1 = mutate(child1, mutation_rate)
            if random.random() < mutation_rate:
                child2 = mutate(child2, mutation_rate)
            offspring.extend([child1, child2])
        population = offspring
    # Evaluate the best individual
    best_individual_fitness = evaluate_individual(best_individual)
    if is_feasible(best_individual):
        print("--- Feasible Individual Actions: {fitness}".format(fitness=best_individual_fitness), best_individual)
        return True
    else:
        print("Not Feasible Individual Actions: {fitness}".format(fitness=best_individual_fitness), best_individual)
        return False

def random_with_random_restart():
    best_fitness = -100000
    best_individual = None
    for _ in range(num_generations):
        population = initialize_population()
        fitness_scores = [evaluate_individual(individual) for individual in population]

        current_best_individual_index = fitness_scores.index(max(fitness_scores))
        current_best_individual = population[current_best_individual_index]
        current_best_fitness = fitness_scores[current_best_individual_index]

        if best_fitness < current_best_fitness:
            best_fitness = current_best_fitness
            best_individual = current_best_individual

    if is_feasible(best_individual):
        print("--- Feasible Individual Actions: {fitness}".format(fitness=best_fitness), best_individual)
        return True
    else:
        print("Not feasible Individual Actions: {fitness}".format(fitness=best_fitness), best_individual)
        return False
        
if __name__ == "__main__":
    # PATH_MAP = "./data/MAP_12_BY_12/input02.txt"
    # with open(PATH_MAP, "r") as f:
    #     n = int(f.readline())
    #     mmap = []
    #     for _ in range(n):
    #         mmap.append(f.readline()[:-1])
    # sea()

    count = 0
    PATH_MAP = "./data/MAP_12_BY_12/input03.txt"
    with open(PATH_MAP, "r") as f:
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])
    for i in range(60):
        if sea():
            count += 1
    print(count)
    
    # for i in range(10):
    #     PATH_MAP = "./data/MAP_12_BY_12/input0{i}.txt".format(i=i)
    #     print()
    #     print(PATH_MAP)
    #     print()
    #     with open(PATH_MAP, "r") as f:
    #         n = int(f.readline())
    #         mmap = []
    #         for _ in range(n):
    #             mmap.append(f.readline()[:-1])
    #     for _ in range(30):
    #         sea()
    