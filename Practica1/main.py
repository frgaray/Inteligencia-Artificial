import os
from problems import Puzzle8, Node
from bfs import bfs
from datetime import datetime

from queue import PriorityQueue

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(dir_path, 'logs', 'log.txt')

    initial_state = [[1,'o',2],
                     [6, 3 ,4],
                     [7, 5 ,8]]    
    queue = 'priority'
    w = 0.8
    p = Puzzle8(initial_state)

    with open(log_file, 'w') as f:
        f.write(f'Inicia partida a las {datetime.now().strftime("%H:%M:%S")} del {datetime.now().strftime("%d/%m/%Y")}\n\n')
        f.write(f'Tablero inicial\n{p}\n\n')
        f.write(f'Tipo de cola: {queue}\n\n')
        if queue == 'priority':
            f.write(f'Peso: {w}\n\n')
        f.write(f'Movimientos\n')

    n, n_expandidos = bfs(p, queue=queue, w=w)
    
    c = 0
    while n:
        with open(log_file, 'a') as f:
            f.write(f'{n}\n\n')
        n = n.parent
        c += 1

    with open(log_file, 'a') as f:
            f.write(f'Finaliza partida a las {datetime.now().strftime("%H:%M:%S")}\n')
            f.write(f'Total de Movimientos: {c}\n')
            f.write(f'Total de Nodos Expandidos: {n_expandidos}\n')

def test_pqueue():
    s1 = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 'o']] 
    
    s2 = [[1, 2, 3],
          [4, 5, 6],
          [7, 'o',8]] 
    
    p1 = Puzzle8(s1)
    p2 = Puzzle8(s2)

    q = PriorityQueue()
    q.put(Node(p1))
    q.put(Node(p2))

    print(q.get())

if __name__ == '__main__':
    main()
    # test_pqueue()