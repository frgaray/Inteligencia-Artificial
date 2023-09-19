from abc import ABC, abstractmethod
import copy
from dataclasses import dataclass, field
from typing import Any

class Problem(ABC):
    """Clase abstracta para problemas.
    
    Todos los problemas deben tener un conjunto de posibles acciones, una lista de estados-meta 
    y un estado inicial.
    """

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
        """Aplica la acción indicada al estado actual del problema."""
        ...
    
    @abstractmethod
    def h(self):
        ...

    def expand(self):
        """
        Regresa una lista con todos los posibles estados siguientes a partir del estado actual (@state).

        Returns
        -------
        Una lista con todos los posibles estados siguientes (instancias de @Problem) a partir del estado
        actual.
        """
        return [child
                for child in (self.action(action) for action in self.actions)
                if child]

@dataclass(order=True)
class Node:
    """Clase que representa una tupla para @Problem.
    
    Todo nodo tiene una instancia de @Problem, un nodo padre, una acción que lo originó y un costo.
    """

    priority: int
    item: Any=field(compare=False)

    def __init__(self, problem, parent=None, action=None, cost=1, w=None):
        self.state        = problem
        self.parent       = parent
        self.action       = action
        self.cost         = cost
        if w or w == 0:
            self.priority = self.f(w)
    
    @property
    def state(self):
        return self._state.state
    
    @state.setter
    def state(self, problem):
        if isinstance(problem, Problem):
            self._state = problem
        else:
            print('Un Nodo necesita tener un objeto de clase Problem como estado.')
 
    def expand(self):
        """Regresa una lista con todos los posibles estados siguientes a partir del estado actual 
        del problema.
        """
        return self._state.expand()
    
    def f(self, w):
        return self.cost + w*self._state.h()
    
    def __str__(self):
        return str(self._state)

class Puzzle8(Problem):
    """Problema del Puzzle del tablero 3x3 con 8 dígitos
    
    Tiene los dígitos del 1 al 8 (sin repetir) y una casilla vacía como caracteres.
    Tiene un caracter diferente asignado a cada casilla.
    """

    actions = set('RLUD')
    """Acciones: Derecha(R), Izquierda(L), Arriba(U), Abajo(D).

    Se considera como movimiento el movimiento de la casilla vacía.
    Por ejemplo:
    [[1,  2,  3],    L    [[ 1,  2, 3],
     [4, 'o', 6],   -->    ['o', 4, 6],
     [7,  8,  5]]          [ 7,  8, 5]]
    """

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
        """Setter que sólo permite tableros sin dígitos repetidos"""
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

    def h(self):
        return self.manhattan()
    
    def __str__(self):
        str = ''
        for row in self._state:
            str += f'{row}\n'
        return str[:-1]
    
    def get_piece_coords(self, piece):
        """Regresa las coordenadas de la pieza brindada"""
        for row in self.state:
            for i in row:
                if i == piece:
                    return row.index(i), self.state.index(row)
        return -1, -1

    def action(self, action):
        x, y = self.get_piece_coords(piece='o')
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
    
    def manhattan(self):
        c = 0
        for piece in {1,2,3,4,5,6,7,8,'o'}:
            c += self.manhattan_piece(piece=piece)
        return c
    
    def manhattan_piece(self, piece):
        bad_x, bad_y    = self.get_piece_coords(piece)

        if piece == 'o':
            piece = 9
        good_x, good_y  = (piece - 1)  % 3, (piece - 1) // 3

        return abs(bad_y - good_y) + abs(bad_x - good_x)