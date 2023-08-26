class Perro:
    def __init__(self, color):
        self.color = color

    @property
    def color(self):
        return self._color
 
    @color.setter
    def color(self, color):
        self._color = color

    def metodo_1(self):
        perro_aux = Perro(self.color.copy())
        perro_aux.color[0] = 'negro'
        return perro_aux

def main():
    perro = Perro(['café'])
    print(perro.color)
    perro.metodo_1()
    print(perro.color)

if __name__ == '__main__':
    main()