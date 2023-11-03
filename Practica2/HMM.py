import itertools
import numpy  as np
import pandas as pd

class FrequentistHMM():

    prior_counts = pd.Series()
    """Conteos de apariciones generales de las y_is"""

    priors = pd.Series()
    """Probabilidades a priori de las y_is"""

    trans_counts = pd.DataFrame(dtype=int)
    """Conteo de transiciones para cada (y_i | y_j)"""

    trans_matrix = pd.DataFrame()
    """Probabilidades frecuentistas de transiciones para cada (y_i | y_j)"""

    sensor_counts = pd.DataFrame(dtype=int)
    """Conteo de apariciones de observaciones, es decir para cada (x_i | y_j)"""

    sensor_matrix = pd.DataFrame()
    """Probabilidades frecuentistas de observaciones, es decir para cada (x_i | x_j)"""

    def __init__(self, data):
        """Constructor de FrequentistHMM
        
        Inicializa las matrices de probabilidades. Según la notación del curso:
            - Matriz  `A`  =  `trans_matrix`
            - Matriz  `B`  = `sensor_matrix`
            - Vector `\Pi` =    `priors`

        Params:
            - data: pandas.DataFrame
                El dataset con observaciones (X) y categorías correspondientes (y).
                Se asume que la columna con índice 0 son las X's y la columna con índice 1 las y's
        """
        if not isinstance(data, pd.DataFrame):
            raise Exception('Un HMM necesita un pd.DataFrame como entrada con sólo dos columnas. La primera X y la segunda Y.')
        y = data.iloc[ : , 1]

        self.set_trans_counts(y)
        self.set_sensor_counts(data)
        self.set_priors()
        self.set_trans_matrix()
        self.set_sensor_matrix()

    def set_trans_counts(self, y):
        """Auxiliar de constructor.
        
        Inicializa la matriz de conteos.
        """
        y.apply(self.count_transition_frequencies)

    def count_transition_frequencies(self, y_i):
        """Método Auxiliar de `set_trans_counts`.
        Se pobla una matriz de conteo de las frecuencia de las transiciones de los valores de interés
        (@trans_counts).
        Además se pobla un vector de conteo sobre frecuencias de las apariciones generales de los
        valores de interés (@prior_counts).
        """
        for first, second in itertools.pairwise(y_i.split()): # Inciso II) Parte: 2/3
            if first in self.prior_counts.index:
                self.prior_counts.loc[first] += 1
            else:
                self.prior_counts.loc[first] = 1
            
            index   = self.trans_counts.index
            columns = self.trans_counts.columns

            if first in index and second in columns:
                self.trans_counts.loc[first, second] += 1
            else:
                self.trans_counts.loc[first, second] = 1

    def set_sensor_counts(self, data):
        """Auxiliar de constructor.
        Se pobla una matriz de conteo de las apariciones de un valor de interés dada una
        observación (@sensor_counts).
        """
        for index, row in data.iterrows():
            x_i = row[0].split() # Inciso II) Parte: 3/3
            y_i = row[1].split()

            if len(x_i) != len(y_i):
                print(f'La fila con índice="{index}" no tiene entradas válidas.\nSe ignorará')
                continue

            for input, output in zip(x_i, y_i):
                index   = self.sensor_counts.index
                columns = self.sensor_counts.columns

                if input in index and output in columns:
                    self.sensor_counts.loc[input, output] += 1
                else:
                    self.sensor_counts.loc[input, output] = 1

    def set_priors(self):
        """Auxiliar de constructor.
        Normaliza el vector de conteos a priori
        (es decir, normaliza @prior_counts y lo convierte en @priors).
        """
        self._priors = self.prior_counts.apply(lambda x: x / self.prior_counts.sum())

    def set_trans_matrix(self):
        """Auxiliar de constructor.
        
        Inicializa la matriz de probabilidades de transición.
        """
        self._trans_matrix = self.get_probs_matrix(self.trans_counts)

    def set_sensor_matrix(self):
        """Auxiliar de constructor.
        
        Inicializa la matriz de probabilidades de los sensores.
        """
        self._sensor_matrix = self.get_probs_matrix(self.sensor_counts)

    def get_probs_matrix(self, count_matrix):
        """Auxiliar para `set_trans_matrix` y `set_sensor_matrix`.
        Pobla la matriz de probabilidades según la matriz de conteo dada.
        Se hizo especialmente para las matrices de conteo `trans_counts` y `sensor_counts`.

        La manera de lidiar con observaciones que no se observaron en @count_matrix es usando la
        fórmula:

             (count(x_i, y_j) + 1)
           -------------------------
           sum(x_i, y_j, over=j) + n    

        La `n` de la fórmula se calcula con el método auxiliar `get_penalizer` (la cantidad de categorías diferentes de y's)
        La `sum(x_i, y_j, over=j)` se calcula para cada x_i con el método auziliar `total_ocurrences`
        """
        input_keys  = count_matrix.index
        output_keys = count_matrix.columns
        prob_matrix = pd.DataFrame()

        totals = self.total_ocurrences(count_matrix)
        penalizer = self.get_penalizer(count_matrix)
        for input in input_keys:
            for output in output_keys:
                numerator = count_matrix.loc[input, output]
                if pd.isna(numerator):
                    numerator = 0
                prob_matrix.loc[input, output] = (numerator + 1) / (totals[input] + penalizer)
        return prob_matrix

    
    def total_ocurrences(self, count_matrix):
        """Auxiliar de `get_probs_matrix`
        
        Ver documentación de `get_probs_matrix`
        """
        return count_matrix.apply(np.sum, axis=1) 
    
    def get_penalizer(self, count_matrix):
        """Auxiliar de `get_probs_matrix`
        
        Ver documentación de `get_probs_matrix`
        """
        return len(count_matrix.columns)
    
    @property
    def trans_matrix(self):
        return self._trans_matrix
    
    @property
    def sensor_matrix(self):
        return self._sensor_matrix
    
    @property
    def priors(self):
        return self._priors
    
    def viterbi_predict(self, X):
        """Algoritmo de Viterbi para predecir categorías de nuevas observaciones.
        
        Está totalmente mal optimizado, ayuda.
        """
        predict = []
        for index, item in X.items():
            predict.append(self.viterbi(item))
        return [item for sublist in predict for item in sublist]


    def viterbi(self, x):
        """Método auxiliar para `viterbi_predict`.
        
        Está totalmente mal optimizado, ayuda.
        """
        x = x.split()
        x_1 = x.pop(0)
        deltas = 1 * pd.DataFrame(self.priors) # Inciso V) Parte: 2/2
        if x_1 in self.sensor_matrix.index:
            deltas = pd.DataFrame(self.sensor_matrix.loc[x_1, :] * self.priors)

        phis = pd.DataFrame()
        for index, x_i in enumerate(x):
            for j in deltas.index:
                best_prev = None
                p_aux = 0
                b = 1
                if x_i in self.sensor_matrix.index:
                    b = self.sensor_matrix.loc[x_i, j]

                for i in deltas.index:
                    a = self.trans_matrix.loc[i, j]
                    prev_delta = deltas.loc[i, index]
                    p = b * a * prev_delta
                    if p > p_aux:
                        p_aux = p
                        best_prev = i

                deltas.loc[j, index+1] = p_aux
                phis.loc[j, index+1] = best_prev

        idxmax = deltas.iloc[:, -1].idxmax()
        prediction = phis.loc[idxmax, :].to_list()
        prediction.append(idxmax)
        return prediction











    


    
    

        