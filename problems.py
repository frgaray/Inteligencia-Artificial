class Puzzle8(object):
    def __init__(self, board):
        self.board = board

    @property
    def board(self):
        return self._board
 
    @board.setter
    def board(self, board):
        digits_in_board = set()
        if type(board) is list and len(board) == 3:
            for row in board:
                if type(row) is list and len(row) == 3:
                    for i in row:
                        digits_in_board.add(i)
            if digits_in_board == {1,2,3,4,5,6,7,8,'o'}:
                self._board = board
        else:
            print('Sólo puedes asignar un tablero de 3x3 válido como estado.')
            print('Sólo se puede asignar una sóla vez cada dígito del 1-8 y el caracter "o"')
            x = 'x'
            self._board = [[x,x,x],[x,x,x],[x,x,x]]
    
    def __str__(self):
        str = ''
        for row in self._board:
            str += f'{row}\n'
        return str
    
    def get_hole_coords(self):
        for row in self.board:
            for i in row:
                if i == 'o':
                    return row.index(i), self.board.index(row)
        return -1, -1

    def expande(self):
        return [hijo
                for hijo in (self.accion(accion) for accion in ['R','L','U','D'])
                if hijo]

    def accion(self, accion):
        x, y = self.get_hole_coords()
        if x == -1:
            print('tablero vacío')
            return

        if   accion == 'R' and x != 2:
            new_x, new_y = x+1, y
        elif accion == 'L' and x != 0:
            new_x, new_y = x-1, y
        elif accion == 'U' and y != 0:
            new_x, new_y = x, y-1
        elif accion == 'D' and y != 2:
            new_x, new_y = x, y+1
        else:
            print('Movimiento inválido')
            return
        
        child = Puzzle8(self.board.copy())
        print(child.board == self.board) # Aquí deberían ser iguales
        child.board[y][x] = child.board[new_y][new_x]
        child.board[new_y][new_x] = 'o'
        print(child.board == self.board) # Aquí ya deberían ser diferentes :s En qué momento se modifica self._board?
        return child