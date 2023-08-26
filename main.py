import problems

def main():
    a = problems.Puzzle8([[1,2,3],[5,'o',6],[7,8,4]])
    print(a)
    a.accion('D')
    print(a)

if __name__ == '__main__':
    main()