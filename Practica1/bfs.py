from problems import Problem, Node
from queue import Queue, LifoQueue, PriorityQueue

def bfs(problem, goal_test='early', queue='priority'):
    """Best First Search"""
    if not isinstance(problem, Problem):
        print('Sólo se puede aplicar BFS a instancias de la clase @Problem')
        return
    
    initial_state = problem.state
    goals = problem.goals

    explorados = [initial_state]
    
    if goal_test == 'early' and initial_state in goals:
        return explorados
    
    if   queue == 'fifo':
        frontier = Queue()
    elif queue == 'lifo':
        frontier = LifoQueue()
    elif queue == 'priority':
        frontier = PriorityQueue()
    else:
        print(f'Elige un tipo de pila válida: "fifo", "lifo", "priority"')
        return
    frontier.put(Node(problem))
    
    c = 0
    while not frontier.empty():
        actual = frontier.get()

        if goal_test == 'late' and actual.state in goals:
            return actual
        
        for child, action in actual.expand():
            c += 1
            if goal_test == 'early' and child.state in goals:
                return Node(child, actual, action), c
            if child.state not in explorados:
                explorados.append(child.state)
                frontier.put(Node(child, actual, action))
    
    print('No se encontró la meta')
                



    

    
