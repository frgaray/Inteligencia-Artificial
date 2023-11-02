import numpy  as np
import pandas as pd
from HMM import FrequentistHMM
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from os.path import abspath, dirname, join

cwd = abspath(dirname(__file__))



def main():
    csv_path = join(cwd, 'ner_dataset.csv')
    data = pd.read_csv(csv_path, header=None, sep='\t')
    
    # X_train, X_test, y_train, y_train = train_test_split(X, y, test_size=0.3, random_state=1)
    data.iloc[ : , 0] = data.iloc[ : , 0].str.lower()
    hmm = FrequentistHMM(data.head())

    print(hmm.sensor_matrix)
    # print(hmm.trans_matrix)
    # print(hmm.priors)

    hmm.viterbi_predict("aaaa")



def test():
    s = "Hola a todos"
    s = s.split()
    print(s.pop(0))
    print(s)

if __name__ == '__main__':
    main()
    # test()