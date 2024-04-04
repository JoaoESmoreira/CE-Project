
import random


mmap = []
n = None
with open("./data/MAP_12_BY_12/input01.txt", "r") as f:
    n = int(f.readline())
    for _ in range(n):
        mmap.append(f.readline()[:-1])
num_actions = list(range(4))


population_size = 100
num_generations = 1000
elite_percentage = 0.2
mutation_rate = 0.1
individual_size = 500


def mapping(individual) -> list[tuple[int, int]]:
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

    fitness = 0
    if count == 0 and len(path) > 0:
        fitness = len(individual)
        fitness = (path[-1][0] + path[-1][1])*10 + len(individual)*3 - repeted_cells(path)*2
        fitness = (path[-1][0] + path[-1][1])# + len(individual)
        if path[-1] == (n-1, n-1):
            print("here")
            fitness *= 10
    else:
        fitness = -count
    return fitness

def initialize_population() -> list[list[int]]:
    return [[random.randint(0, 3) for _ in range(random.randint(1, 100))] for _ in range(population_size)]

def select_parents(population, fitness_scores, elite_percentage) -> list[list[int]]:
    sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
    elite_size = int(elite_percentage * len(population))
    elite_indices = sorted_indices[:elite_size]
    
    return [population[idx] for idx in elite_indices]

def crossover(parent1, parent2) -> tuple[list[int], list[int]]:
    crossover_point = random.randint(0, min(len(parent1), len(parent2)))
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate) -> list[int]:
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, 3)
    if random.random() < mutation_rate and len(individual) < individual_size:
        individual.append(random.randint(0, 3))
    if random.random() < mutation_rate and len(individual) > 0:
        individual.pop(random.randint(0, len(individual)-1))
    return individual

def sea():
    population = initialize_population()
    for generation in range(num_generations):
        fitness_scores = [evaluate_individual(individual) for individual in population]

        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]
        best_fitness = fitness_scores[best_individual_index]

        print(f"Generation {generation+1}, Best Fitness: {best_fitness}", best_individual)

        parents = select_parents(population, fitness_scores, elite_percentage)
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child1 = mutate(child1, mutation_rate)
            if random.random() < mutation_rate:
                child2 = mutate(child2, mutation_rate)
            offspring.extend([child1, child2])
        population = offspring
    # Evaluate the best individual
    best_individual_fitness = evaluate_individual(best_individual)
    print("Best Individual Actions:", best_individual)
    print("Best Individual Fitness:", best_individual_fitness)

if __name__ == "__main__":
    sea()
