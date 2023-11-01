import numpy  as np
import pandas as pd

class HMM():

    prior_counts = {}

    priors = pd.DataFrame()

    trans_counts = {}

    trans_matrix = pd.DataFrame()

    sensor_counts = {}

    possible_inputs = {}

    sensor_matrix = pd.DataFrame()

    def count_transition_frequencies(self, y_i):
        """Método Auxiliar"""
        y_i = y_i.split()
        y_i_len = len(y_i) - 1

        for index, output in enumerate(y_i):
            if output in self.prior_counts:
                self.prior_counts[output] += 1
            else:
                self.prior_counts[output] = 1

            if index == y_i_len:
                break

            transition = f'{output}->{y_i[index+1]}'
            if transition in self.trans_counts:
                self.trans_counts[transition] += 1
            else:
                self.trans_counts[transition] = 1

    def count_sensor_frequencies(self, data):
        """Auxiliar"""
        for index, row in data.iterrows():
            x_i = row[0]
            y_i = row[1]
            for x, y in zip(x_i.split(), y_i.split()):
                observation = f'{x}={y}'
                if observation in self.sensor_counts:
                    self.sensor_counts[observation] += 1
                else:
                    self.sensor_counts[observation] = 1
                
                if x not in self.possible_inputs:
                    self.possible_inputs[x] = 'o'

    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise Exception('Un HMM necesita un pd.DataFrame como entrada con sólo dos columnas. La primera X y la segunda Y.')
        X = data.iloc[ : , 0]
        y = data.iloc[ : , 1]

        y.apply(self.count_transition_frequencies)


        self.trans_matrix = False
        self.priors = False
        self.count_sensor_frequencies(data)

        self.sensor_matrix = False

    @property
    def trans_matrix(self):
        return self._trans_matrix
    
    def count_total_transitions(self):
        """Auxiliar"""
        totals = {}
        for key in self.prior_counts.keys():
            totals[key] = 0
            for transition in self.trans_counts.keys():
                if key == transition.split('->')[0]:
                    totals[key] += self.trans_counts[transition]
        return totals
    
    def get_penalizer(self, first):
        """Auxiliar"""
        penalizer = 0
        for second in self.prior_counts.keys():
            transition = f'{first}->{second}'
            if transition not in self.trans_counts.keys():
                penalizer += 1
        return penalizer
 
    @trans_matrix.setter
    def trans_matrix(self, dummy_arg):
        keys = self.prior_counts.keys()
        trans_matrix = pd.DataFrame(index=keys, columns=keys, dtype=float)

        totals = self.count_total_transitions()
        for first in keys:
            penalizer = self.get_penalizer(first)
            for second in keys:
                numerator = 0
                transition = f'{first}->{second}'
                if transition in self.trans_counts.keys():
                    numerator = self.trans_counts[transition]
                trans_matrix.loc[first, second] = (numerator + 1) / (totals[first] + penalizer)


        self._trans_matrix = trans_matrix
    @property
    def priors(self):
        return self._priors

    @priors.setter
    def priors(self, dummy_arg):
        ...

    @property
    def sensor_matrix(self):
        return self._sensor_matrix

    @sensor_matrix.setter
    def sensor_matrix(self, dummy_arg):
        input_keys  = self.possible_inputs.keys()
        output_keys = self.prior_counts.keys()
        sensor_matrix = pd.DataFrame(index=input_keys, columns=output_keys, dtype=float)
        for input in input_keys:
            for output in output_keys:
                observation = f'{input}={output}'
                probability = 1
                if observation in self.sensor_counts.keys():
                    probability = self.sensor_counts[observation] / self.prior_counts[output]
                sensor_matrix.loc[input , output] = probability
        self._sensor_matrix = sensor_matrix





    


    
    

        