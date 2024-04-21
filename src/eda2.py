
import random
from collections import defaultdict


class EDA:
    def __init__(self, lake, learn_rate=0.9, individual_size=100, population_size=10, generations=100) -> None:
        self.lake = lake
        self.individual_size = individual_size
        self.population_size = population_size
        self.generations = generations

        self.dimentions = len(self.lake)
        self.target = (self.dimentions-1, self.dimentions-1)

        self.learn_rate = learn_rate
        self.PDM = [0.25 for _ in range(self.dimentions**2)] # probability distribution model

    def _init_pdm(self):
        self.PDM = [{} for _ in range(self.dimentions**2)]
        for i in range(self.dimentions**2):
            c = set(self._make_moves(i, -1))
            for j in c:
                self.PDM[i][j] = 1/len(c)

    def fit(self):
        population = [self._create_individual() for _ in range(self.population_size)]
        fitness = [self._evaluate(individual) for individual in population]
        self._update_PDM(population, fitness)
        print(self.PDM)

    def _update_PDM(self, population, fitness):
        print(population)
        print(fitness)
        PDM = [0 for _ in range(len(self.PDM))]
        for i in range(len(population)):
            for state in population[i]:
                PDM[state] += fitness[i]
        self.PDM = PDM

    def _make_moves(self, state, previous_state):
        cell = (state // self.dimentions, state % self.dimentions)
        previous_cell = (previous_state // self.dimentions, previous_state % self.dimentions)
        actions = [(0,-1), (1, 0), (0,1), (-1,0)]
        for i in range(len(actions)):
            new_state = (cell[0] + actions[i][0], cell[1] + actions[i][1])
            if 0 <= new_state[0] < n and 0 <= new_state[1] < n and new_state != previous_cell:
                yield new_state[0]*self.dimentions + new_state[1]

    def _evaluate(self, individual):
        last_cell = (individual[-1] // self.dimentions, individual[-1] % self.dimentions)
        return last_cell[0] + last_cell[1]

    def _create_individual(self):
        solution = []
        current_state = 0
        previous_state = 0
        while True:
            components = list(self._make_moves(current_state, previous_state))
            if len(solution) >= self.individual_size or len(components) == 0:
                break
            
            previous_state = current_state
            p = self._calculate_probabilities(components, current_state)
            current_state = random.choices(components, weights=p, k=1)[0]
            cell = (current_state // self.dimentions, current_state % self.dimentions)

            if self.lake[cell[0]][cell[1]] == 'H':
                break
            elif cell == self.target:
                solution.append(current_state)
                break
            solution.append(current_state)
        return solution

    def _calculate_probabilities(self, components, current_state):
        p = []
        for c in components:
            p.append(self.PDM[c])
        return p

if __name__ == "__main__":
    PATH_MAP = "./data/MAP_{d}_BY_{d}/input0{i}.txt".format(d=4, i=2)
    with open(PATH_MAP, "r") as f:
        n = int(f.readline())
        mmap = []
        for _ in range(n):
            mmap.append(f.readline()[:-1])

    eda = EDA(mmap)
    eda.fit()