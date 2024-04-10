import random
def generate_ant(self):
    # path = [0]
    # current_cell = (0, 0)
    # current_state = 0
    # while current_cell != self.target:
    #     possible_cells = list(self.make_moves(current_cell))
    #     if not possible_cells:
    #         print("here")
    #         break
    #     possible_states = [move[0]*(self.target[0]) + move[1] for move in possible_cells]
    #     probabilities = self.calculate_probabilities(possible_states, current_state)
    #     index_next_  = random.choices(range(len(possible_states)), weights=probabilities, k=1)[0]
    #     next_state   = possible_states[index_next_]
    #     current_cell = possible_cells[index_next_]
    #     path.append(next_state)
    #     current_state = next_state
    # return path
    solution = []
    source = 0
    while True:
        components = list(self.make_moves(source))
        print(components)
        if len(components) == 0:
            break
        source = random.choice(components)
        solution.append(source)
    return solution