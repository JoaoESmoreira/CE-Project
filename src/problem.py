
from __future__ import annotations

from typing import TextIO, Optional, Any, Union
from collections.abc import Iterable, Hashable
from dataclasses import dataclass
import random


Objective = Any

@dataclass
class Component:
    i: int


Colection = Union[set[Component], list[Component], tuple[Component]]

class Solution:
    def output(self) -> str:
        """
        Generate the output string for this solution
        """
        raise NotImplementedError

    def copy(self) -> Solution:
        """
        Return a copy of this solution.

        Note: changes to the copy must not affect the original
        solution. However, this does not need to be a deepcopy.
        """
        raise NotImplementedError

    def is_feasible(self) -> bool:
        """
        Return whether the solution is feasible or not
        """
        raise NotImplementedError

    def fitness(self) -> Optional[Objective]:
        """
        Return the fitness value for this solution if defined, otherwise
        should return None
        """
        raise NotImplementedError

    def random_moves(self) -> Iterable[Component]:
        """
        Return an iterable (generator, iterator, or iterable object)
        over all components that can be added to the solution
        """
        raise NotImplementedError

    def add_move(self, component: Component) -> None:
        """
        Add a component to the solution.
        """
        raise NotImplementedError

    def get_genotype(self) -> Optional[set[Component]]:
        """
        Return the components of this solution if defined, otherwise
        should return None
        """
        raise NotImplementedError

    def crossover(self, parent: Optional[Colection]) -> None:
        """
        Share the information of another solution to this solution
        """
        raise NotImplementedError

    def mutate(self) -> None:
        """
        Apply a local move to this solution.
        """
        raise NotImplementedError

class Problem:
    @classmethod
    def from_textio(cls, f: TextIO) -> Problem:
        """
        Create a problem from a text I/O source `f`
        """
        raise NotImplementedError
        # return cls(n=n, mmap=tuple(mmap))

    def empty_solution(self) -> Solution:
        """
        Create an empty solution (i.e. with no components).
        """
        raise NotImplementedError


if __name__ == '__main__':
    from cli import cli
    cli(Problem)
