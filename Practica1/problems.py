from abc import ABC, abstractmethod
import copy

class Problem(ABC):

    actions = set()

    goals = []

    @property
    @abstractmethod
    def state(self):
        ...

    @abstractmethod
    def __str__():
        ...

    @abstractmethod
    def action(self, action):
        ...

    def expand(self):
        return [child
                for child in (self.action(action) for action in self.actions)
                if child]

class Node:

    def __init__(self, problem, parent=None, action=None, cost=0):
        self.state = problem
        self.parent = parent
        self.action = action
        self.cost = cost
    
    @property
    def state(self):
        return self._state.state
    
    @state.setter
    def state(self, problem):
        self._state = problem
 
    def expand(self):
        return self._state.expand()
    
    def __str__(self):
        return str(self._state)

class Puzzle8(Problem):

    actions = set('RLUD')

    goals = [[[1, 2, 3 ],
              [4, 5, 6 ],
              [7, 8,'o']]]

    def __init__(self, board):
        self.state = board

    @property
    def state(self):
        return self._state
 
    @state.setter
    def state(self, board):
        digits_in_board = set()
        if type(board) is list and len(board) == 3:
            for row in board:
                if type(row) is list and len(row) == 3:
                    for i in row:
                        digits_in_board.add(i)
            if digits_in_board == {1,2,3,4,5,6,7,8,'o'}:
                self._state = board
        else:
            print('Sólo puedes asignar un tablero de 3x3 válido como estado.')
            print('Sólo se puede asignar una sóla vez cada dígito del 1-8 y el caracter "o"')
            x = 'x'
            self._state = [[x,x,x],[x,x,x],[x,x,x]]
    
    def __str__(self):
        str = ''
        for row in self._state:
            str += f'{row}\n'
        return str[:-1]
    
    def get_hole_coords(self):
        for row in self.state:
            for i in row:
                if i == 'o':
                    return row.index(i), self.state.index(row)
        return -1, -1

    def action(self, action):
        x, y = self.get_hole_coords()
        if x == -1:
            print('tablero vacío')
            return

        if   action == 'R' and x != 2:
            new_x, new_y = x+1, y
        elif action == 'L' and x != 0:
            new_x, new_y = x-1, y
        elif action == 'U' and y != 0:
            new_x, new_y = x, y-1
        elif action == 'D' and y != 2:
            new_x, new_y = x, y+1
        else:
            # print('Movimiento inválido')
            return
        
        child = Puzzle8(copy.deepcopy(self.state))
        child.state[y][x] = child.state[new_y][new_x]
        child.state[new_y][new_x] = 'o'
        return child, action
    
    def test(self):
        ...