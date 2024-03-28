
from __future__ import annotations

from typing import TypeVar, Optional, Protocol
from .random_construction import random_construction
import random


Objective = TypeVar('Objective')
Component = TypeVar('Component')

class SolutionProtocol(Protocol[Objective, Component]):
    def fitness(self) -> Optional[Objective]: ...
    def output(self) -> str: ...
    def get_genotype(self) -> Optional[set[Component]]: ...
    def crossover(self, parent: Optional[set[Component]]) -> None: ...
    def copy(self) -> Solution:...
    def mutate(self) -> None: ...

Solution = TypeVar('Solution', bound=SolutionProtocol)

class ProblemProtocol:
    def empty_solution(self) -> Solution: ...

Problem = TypeVar('Problem', bound=ProblemProtocol)


PROB_CROSSOVER = 0.9
PROB_MUTATION = 0.05
POPULATION_SIZE = 50
ELITISM_SIZE = 5
TOURNAMENT_SIZE = 5


def parent_selection(population) -> Solution:
    pool = list(random.sample(population, TOURNAMENT_SIZE))
    return max(pool, key=lambda x: x[0], default=None)[1]

def select_survivors(population) -> list[Solution]:
    #for elem in population[0:ELITISM_SIZE]:
    #    print(elem[1].fitness())
    return [indiv[1] for indiv in population[0:ELITISM_SIZE]]

def sea(problem:Problem, budget: int) -> Optional[Solution]:
    init_population = list(random_construction(problem.empty_solution()) for _ in range(POPULATION_SIZE))     # init population
    population = list((individual.fitness(), individual) for individual in init_population)                   # evaluate population

    for _ in range(budget):
        population.sort(key=lambda x: x[0], reverse=True)
        offspring = select_survivors(population)
        while len(offspring) < POPULATION_SIZE:
            if random.random() < PROB_CROSSOVER:
                # select parerents
                parent1 = parent_selection(population)
                parent2 = parent_selection(population)
                # recombine parents
                new_individual = parent1.copy()
                new_individual.crossover(parent2.get_genotype())
            else:
                new_individual = parent_selection(population).copy()
            # mutate
            if random.random() < PROB_MUTATION:
                new_individual.mutate()
            offspring.append(new_individual)
        population = list((individual.fitness(), individual) for individual in offspring)      # evaluate population
        
    best = max(population, key=lambda x: x[0], default=None)[1]
    return best
