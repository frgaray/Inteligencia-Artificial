import itertools
import numpy  as np
import pandas as pd

class FrequentistHMM():

    prior_counts = pd.Series()

    priors = pd.Series()

    trans_counts = pd.DataFrame(dtype=int)

    trans_matrix = pd.DataFrame()

    sensor_counts = pd.DataFrame(dtype=int)

    sensor_matrix = pd.DataFrame()

    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise Exception('Un HMM necesita un pd.DataFrame como entrada con sólo dos columnas. La primera X y la segunda Y.')
        y = data.iloc[ : , 1]

        self.set_trans_counts(y)
        self.set_sensor_counts(data)
        self.set_priors()
        self.set_trans_matrix()
        self.set_sensor_matrix()

    def set_trans_counts(self, y):
        y.apply(self.count_transition_frequencies)

    def count_transition_frequencies(self, y_i):
        """Método Auxiliar de `set_trans_counts`.
        Se pobla una matriz de conteo de las frecuencia de las transiciones de los valores de interés
        (@trans_counts).
        Además se pobla un vector de conteo sobre frecuencias de las apariciones generales de los
        valores de interés (@prior_counts).
        """
        for first, second in itertools.pairwise(y_i.split()):
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
            x_i = row[0].split()
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
        Normaliza el vector de conteos a priori (@priors)
        """
        self._priors = self.prior_counts.apply(lambda x: x / self.prior_counts.sum())

    def set_trans_matrix(self):
        self._trans_matrix = self.get_probs_matrix(self.trans_counts)

    def set_sensor_matrix(self):
        self._sensor_matrix = self.get_probs_matrix(self.sensor_counts)

    def get_probs_matrix(self, count_matrix):
        """Auxiliar para `set_trans_matrix` y `set_sensor_matrix`.
        Pobla la matriz de probabilidades según la matriz de conteo dada.
        Se hizo especialmente para las matrices de conteo `trans_counts` y `sensor_counts`.

        Se normaliza sumando sobre axis=1.

        La manera de lidiar con observaciones que no se observaron en @count_matrix es usando la
        fórmula:

            (prob(observación) + 1)
           -------------------------
           observaciones_totales + n
        
        donde "prob(observación)" es igual a 0 cuando no se contó ninguna aparición.
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
        """Auxiliar de `get_probs_matrix`"""
        return count_matrix.apply(np.sum, axis=1) 
    
    def get_penalizer(self, count_matrix):
        """Auxiliar de `get_probs_matrix`"""
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
    
    def viterbi_predict(self, x):
        x = x.split()
        x_1 = x.pop(0)
        deltas = pd.DataFrame(self.priors).T
        if x_1 in self.sensor_matrix.index:
            deltas = pd.DataFrame(self.sensor_matrix.loc[x_1, :]).T * self.priors.T

        for index, x_i in enumerate(x):
            ...
            

        # deltas = pd.concat([deltas, pd.DataFrame(self.sensor_matrix.loc[x[0], :]).T])
        print(self.priors)
        print(deltas)
        ...
 











    


    
    

        