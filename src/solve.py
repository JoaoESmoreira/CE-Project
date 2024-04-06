
import random


mmap = []
n = None
with open("./data/MAP_4_BY_4/input09.txt", "r") as f:
    n = int(f.readline())
    for _ in range(n):
        mmap.append(f.readline()[:-1])
num_actions = list(range(4))


population_size = 100
num_generations = 1000
elite_percentage = 0.2
mutation_rate = 0.1
individual_size = 100


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
    for step in path:
        for i in step:
            if i < 0 or i == n:
                count += 1
    for step in path:
        if 0 <= step[0] < n and 0 <= step[1] < n and mmap[step[0]][step[1]] == 'H':
            count += 1
    if len(path) == 0:
        return -count*n - n*2
    return (path[-1][0] + path[-1][1])*2 - count*n - (abs(path[-1][0] - (n+1)) + abs(path[-1][1] - (n+1))) - len(path)
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

def select_parents(population, fitness_scores, elite_percentage) -> list[list[int]]:
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
    elite_size = int(elite_percentage * len(population))
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

def tornement_selection(population, fitness_scores, elite_percentage) -> list[list[int]]:
    pop_fit = [(population[i], fitness_scores[i]) for i in range(len(population))]
    elite_size = int(elite_percentage * len(population))
    parents = random.sample(pop_fit, elite_size)
    parents.sort(key=lambda element: element[1], reverse=True)
    parents = [parents[0][0], parents[1][0]]
    return parents

def crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    crossover_point = random.randint(0, min(len(parent1), len(parent2)))
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate) -> list[int]:
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, 3)
    #while random.random() < 0.5 and len(individual) < individual_size:
    #    individual.append(random.randint(0, 3))
    if random.random() < 0.5 and len(individual) < individual_size:
        path = mapping(individual)
        if len(path) > 0:
            for i in range(min(abs(path[-1][0] - n), abs(path[-1][1] - n))):
                individual.append(random.randint(0, 3))
        else:
            for i in range(n):
                individual.append(random.randint(0, 3))
    if random.random() < mutation_rate and len(individual) > 0:
        individual.pop(random.randint(0, len(individual)-1))
    return individual

# import matplotlib.pyplot as plt 
# import numpy as np
# def create_interactive_plot(title, xlabel, ylabel, lim_x, lim_y):
#     plt.ion()
#     # creating subplot and figure
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.set_ylim(*lim_y)
#     ax.set_xlim(*lim_x)
#     line1, = ax.plot([], [])
#     # setting labels
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     return line1, fig, ax
# 
# def update_graph(x, y, graph, fig, ax):
#     graph.set_xdata(np.append(graph.get_xdata(), x))
#     graph.set_ydata(np.append(graph.get_ydata(), y))
#     ax.draw_artist(ax.patch)
#     ax.draw_artist(graph)
#     fig.canvas.draw()
#     fig.canvas.flush_events()

def sea():
    # f = create_interactive_plot('Evolving...', 'Iteration', 'Quality', (0, 1000), (-2, 200))

    population = initialize_population()
    for generation in range(num_generations):
        fitness_scores = [evaluate_individual(individual) for individual in population]

        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]
        best_fitness = fitness_scores[best_individual_index]

        # print(f"Generation {generation+1}, Best Fitness: {best_fitness}", best_individual)
        #print("Avg fitness: ", sum(fitness_scores) / len(fitness_scores))
        # update_graph(generation, best_fitness, *f)

        parents = select_parents(population, fitness_scores, elite_percentage)
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            # parent1, parent2 = tornement_selection(population, fitness_scores, elite_percentage)
            child1, child2 = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child1 = mutate(child1, mutation_rate)
            if random.random() < mutation_rate:
                child2 = mutate(child2, mutation_rate)
            offspring.extend([child1, child2])
        population = offspring
    # Evaluate the best individual
    best_individual_fitness = evaluate_individual(best_individual)
    if is_feasible(best_individual):
        print("Feasible Individual Actions:", best_individual)
        print("Fitness:", best_individual_fitness)
    else:
        print("Not feasible Individual Actions:", best_individual)
        print("Fitness:", best_individual_fitness)

if __name__ == "__main__":
    sea()
    for _ in range(20):
        sea()
