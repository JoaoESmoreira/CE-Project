
from __future__ import annotations

from typing import TypeVar, Optional, Any
from .random_construction import random_construction

Objective = Any

class SolutionProtocol:
    def fitness(self) -> Optional[Objective]: ...
Solution = TypeVar('Solution', bound=SolutionProtocol)

class ProblemProtocol:
    def empty_solution(self) -> Solution: ...
Problem = TypeVar('Problem', bound=ProblemProtocol)


def random_restart(problem:Problem, budget: int) -> Solution:
    init_population = [random_construction(problem.empty_solution()) for _ in range(budget)]     # init population
    population = set((individual.fitness(), individual) for individual in init_population)       # evaluate population
    best = max(population, key=lambda x: x[0], default=None)
    return best[1]
    if best is not None:
        return best[1]
    return None
