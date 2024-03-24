
from __future__ import annotations

from typing import Protocol, TypeVar
from collections.abc import Iterable

import random

class ObjectiveProtocol(Protocol):
    def __lt__(self, other) -> bool: ...

Objective = TypeVar('Objective', bound=ObjectiveProtocol, covariant=True)
Component = TypeVar('Component')

class SolutionProtocol(Protocol[Objective, Component]):
    def random_moves(self) -> Iterable[Component]: ...
    def add_move(self, component: Component) -> None: ...

Solution = TypeVar('Solution', bound=SolutionProtocol)

def random_construction(solution: Solution) -> Solution:
    while True:
        components = list(solution.random_moves())
        if len(components) == 0:
            break
        c = random.choice(components)
        solution.add_move(c)
    return solution

