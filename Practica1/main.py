from problems import Puzzle8
from bfs import bfs
from datetime import datetime

def main():
    log_file = 'C:\\Users\\allda\\OneDrive\\Documentos\\Universidad\\Inteligencia-Artificial\\Practica1\\logs\\log.txt'

    initial_state = [[1,'o',2],
                     [6,3,4],
                     [7,5,8]]
    
    queue = 'fifo'
    p = Puzzle8(initial_state)
    with open(log_file, 'w') as f:
        f.write(f'Inicia partida a las {datetime.now().strftime("%H:%M:%S")} del {datetime.now().strftime("%d/%m/%Y")}\n\n')
        f.write(f'Tablero inicial\n{p}\n\n')
        f.write(f'Tipo de cola: {queue}\n\n')
        f.write(f'Movimientos\n')

    n, n_expandidos = bfs(p, queue=queue)

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

if __name__ == '__main__':
    main()