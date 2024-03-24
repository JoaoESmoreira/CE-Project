
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
    best = None
    best_fitness = None
    for _ in range(budget):
        s :Solution = problem.empty_solution()
        s :Solution = random_construction(s)
        s_fitness = s.fitness()
        if best is None:
            best = s
            best_fitness = s_fitness
        elif best_fitness < s_fitness:
            best = s
            best_fitness = s_fitness

    return best
