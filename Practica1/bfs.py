from problems import Problem, Node
from queue import Queue, LifoQueue, PriorityQueue

def bfs(problem, goal_test='early', queue='priority', w=None):
    """Best-First Search
    
    Implementación del algoritmo de Best First Search.

    Params
    ------
    problem: Problem
        El problema al cual se le quiere aplicar el algoritmo. Ver @Problem.
    goal_test: str
        Bandera para indicar cómo verificar los estados meta.
        - 'early' para Early Goal Test
        - 'late'  para Late  Goal Test
    queue: str
        Bandera para indicar el tipo de cola/pila a utilizar. Según el tipo de
        cola/pila cambia la forma de búsqueda.
        - 'fifo'  para Breadth-First Search
        - 'lifo'  para   Depth-First Search
        - 'priority' para Best-First Search
    """
    if not isinstance(problem, Problem):
        print('Sólo se puede aplicar BFS a instancias de la clase @Problem')
        return
    
    initial_state = problem.state
    goals = problem.goals
    problem = Node(problem)

    explorados = [initial_state]
    n_expandidos = 0
    
    if goal_test == 'early' and initial_state in goals:
        return problem, n_expandidos
    
    frontier = get_frontier(queue)
    frontier.put(problem)
    
    while not frontier.empty():
        actual = frontier.get()

        if goal_test == 'late' and actual.state in goals:
            return actual, n_expandidos
        
        for child, action in actual.expand():
            n_expandidos += 1
            child = Node(child, actual, action, actual.cost + 1, w)
            if goal_test == 'early' and child.state in goals:
                return child, n_expandidos
            if child.state not in explorados:
                explorados.append(child.state)
                frontier.put(child)
    
    return None, n_expandidos                

def get_frontier(queue):
    if   queue == 'fifo':
        return Queue()
    elif queue == 'lifo':
        return LifoQueue()
    elif queue == 'priority':
        return PriorityQueue()
    else:
        exit(f'Elige un tipo de pila válida: "fifo", "lifo", "priority"')


    

    
