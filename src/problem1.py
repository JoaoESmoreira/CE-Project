
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
    def __init__(self, problem: Problem,
                    used: list[Component],
                    unused: set[Component],
                    total_moves: int,
                    source: tuple[int, int],
                    target: tuple[int, int],
                    path: list[Component]
                    ) -> None:
        self.problem = problem
        self.used = used
        self.unused = unused
        self.total_moves = total_moves
        self.position = source
        self.target = target
        self.path = path

    def output(self) -> str:
        """
        Generate the output string for this solution
        """
        return " ".join(list(map(str, self.used))) + "\n"

    def copy(self) -> Solution:
        """
        Return a copy of this solution.

        Note: changes to the copy must not affect the original
        solution. However, this does not need to be a deepcopy.
        """
        return Solution(problem=self.problem,
                        used=self.used.copy(),
                        unused=self.unused.copy(),
                        total_moves=self.total_moves,
                        source=self.position,
                        target=self.target,
                        path=self.path.copy()
                        )
    def _mapping(self) -> None:
        last_position = (0, 0)
        self.path = []
        for component in self.used:
            if component == 0:
                last_position = (last_position[0], last_position[1]-1)
            elif component == 1:
                last_position = (last_position[0]+1, last_position[1])
            elif component == 2:
                last_position = (last_position[0], last_position[1]+1)
            elif component == 3:
                last_position = (last_position[0]-1, last_position[1])
            self.path.append(last_position)
            self.position = last_position

    def is_feasible(self) -> bool:
        """
        Return whether the solution is feasible or not
        """
        if len(self.path) == 0:
            self._mapping()
        if self.position == self.target and not self.problem.get_lake(self.path):
            return True
        return None

    def fitness(self) -> Optional[Objective]:
        """
        Return the fitness value for this solution if defined, otherwise
        should return None
        """
        feasible = -3
        if self.is_feasible():
            feasible = self.target[0]**2 - len(self.used)
        return -len(self.used) + self.target[0]*2 + feasible #* (len(self.used))
        # if self.is_feasible():
        # return None

    def random_moves(self) -> Iterable[Component]:
        """
        Return an iterable (generator, iterator, or iterable object)
        over all components that can be added to the solution
        """
        self.total_moves -= 1
        #if self.total_moves > 0 and self.position != self.target:
        if self.position != self.target:
            unused = self.unused.copy()
            if self.position[0] == 0:
                unused.remove(3)
            if self.position[1] == 0:
                unused.remove(0)
            if self.position[0] == self.target[0]:
                unused.remove(1)
            if self.position[1] == self.target[1]:
                unused.remove(2)
            for move in unused:
                yield Component(i=move)

    def add_move(self, component: Component) -> None:
        """
        Add a component to the solution.
        """
        i = component.i
        if i == 0:
            self.position = (self.position[0], self.position[1]-1)
        elif i == 1:
            self.position = (self.position[0]+1, self.position[1])
        elif i == 2:
            self.position = (self.position[0], self.position[1]+1)
        elif i == 3:
            self.position = (self.position[0]-1, self.position[1])
        self.used.append(i)
        self.path.append(self.position)

    def get_genotype(self) -> Optional[set[Component]]:
        """
        Return the components of this solution if defined, otherwise
        should return None
        """
        return self.used

    def _crossover1(self, parent: Optional[Colection]) -> None:
        self.path = []
        cut_point = random.randint(0, min(len(self.used), len(parent)))
        if random.randint(0, 1) > 0:
            self.used = self.used[:cut_point] + parent[cut_point:]
        else:
            self.used = parent[:cut_point] + self.used[cut_point:]

    def crossover(self, parent: Optional[Colection]) -> None:
        self.path = []
        crossover_points = sorted(random.sample(range(1, min(len(self.used), len(parent))), 2))
        self.used = self.used[:crossover_points[0]] + parent[crossover_points[0]:crossover_points[1]] + self.used[crossover_points[1]:]

    def mutate(self) -> None:
        self.path = []
        for i in range(len(self.used)):
            if random.randint(0, 1) == 1:
                self.used[i] = random.randint(0, 3)

class Problem:
    def __init__(self, n: int,
                 mmap: tuple[str]) -> None:
        self.n = n
        self.mmap = mmap
        self.sourse = (0, 0)
        self.target = (n-1, n-1)

    def get_lake(self, path: list[tuple[int, int]]) -> None:
        for step in path:
            for i in step:
                if i < 0 or i == self.n:
                    return True
        for step in path:
            if self.mmap[step[0]][step[1]] == 'H':
                return True
        return False

    @classmethod
    def from_textio(cls, f: TextIO) -> Problem:
        """
        Create a problem from a text I/O source `f`
        """
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])
        return cls(n=n, mmap=tuple(mmap))

    def empty_solution(self) -> Solution:
        """
        Create an empty solution (i.e. with no components).
        """
        return Solution(problem=self,
                        used=[],
                        unused=set(range(4)),
                        total_moves=random.randint(1, self.n**2),
                        source=self.sourse,
                        target=self.target,
                        path=[]
                        )


if __name__ == '__main__':
    from cli import cli
    cli(Problem)
