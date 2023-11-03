import numpy  as np
import pandas as pd
from HMM import FrequentistHMM
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from os.path import abspath, dirname, join
from datetime import datetime


cwd = abspath(dirname(__file__))



def main():
    csv_path = join(cwd, 'data', 'ner_dataset.csv')
    data = pd.read_csv(csv_path, header=None, sep='\t')
    data.iloc[ : , 0] = data.iloc[ : , 0].str.lower() # Inciso II) Parte: 1/3. Las otras partes están en `HMM.py.count_transition_frequencies` y `HMM.py.set_sensor_counts`

    X = data.iloc[ : , 0]
    y = data.iloc[ : , 1] 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # Inciso III)
    data_train = pd.concat([X_train, y_train], axis=1)

    print(f'Comienza entrenamiento a las: {now()}')
    hmm = FrequentistHMM(data_train) # Inciso IV) Las probabilidades están en los atributos @priors, @trans_matrix y @sensor_matrix
    print(f'Termina entrenamiento a las: {now()}') # Con mi dinosaurio tardó aproximadamente 2min 33s

    print(f'Comienza predicción a las: {now()}')
    y_pred = hmm.viterbi_predict(X_test) # Inciso V) Parte: 1/2. La otra parte está en `HMM.py.viterbi`
    print(f'Termina predicción a las: {now()}') # Con mi dinosaurio tardó aproximadamente 18min 9s

    y_test = flat_y(y_test)
    print(classification_report(y_test, y_pred)) # Inciso VI) 
    

def flat_y(y):
    """Auxiliar para aplanar una serie de cadenas a una lista de palabras"""
    y = y.apply(str.split).to_list()
    y =  [item for sublist in y for item in sublist]
    return y

def now():
    """Auxiliar para obtener el tiempo de ahora"""
    return datetime.now().strftime("%H:%M:%S")

if __name__ == '__main__':
    main()