import os
from problems import Puzzle8, Node
from bfs import bfs
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(dir_path, 'logs', 'log.txt')

def main():
    initial_state = [[1,'o',2],
                     [6, 3 ,4],
                     [7, 5 ,8]]    
    queue = 'priority' # Puedes elegir entre 'lifo', 'fifo' ó 'priority'
    w = 0 # El peso para A* pesado.Poner `None` si la cola es fifo o lifo para eficiencia
    p = Puzzle8(initial_state)

    with open(log_file, 'w') as f:
        f.write(f'Inicia partida a las {datetime.now().strftime("%H:%M:%S")} del {datetime.now().strftime("%d/%m/%Y")}\n\n')
        f.write(f'Tablero inicial\n{p}\n\n')
        f.write(f'Tipo de cola: {queue}\n\n')
        if queue == 'priority':
            f.write(f'Peso: {w}\n\n')
        f.write(f'Movimientos\n')

    n, n_expandidos = bfs(p, queue=queue, w=w)
    
    n_movimientos = 0
    with open(log_file, 'a') as f:
        while n:
            f.write(f'{n}\n\n')
            n = n.parent
            n_movimientos += 1

        f.write(f'Finaliza partida a las {datetime.now().strftime("%H:%M:%S")}\n')
        f.write(f'Total de Movimientos: {n_movimientos}\n')
        f.write(f'Total de Nodos Expandidos: {n_expandidos}\n')

if __name__ == '__main__':
    main()