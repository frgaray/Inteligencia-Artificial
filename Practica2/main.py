import numpy  as np
import pandas as pd
from HMM import HMM
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from os.path import abspath, dirname, join

cwd = abspath(dirname(__file__))



def main():
    csv_path = join(cwd, 'ner_dataset.csv')
    data = pd.read_csv(csv_path, header=None, sep='\t')
    
    # X_train, X_test, y_train, y_train = train_test_split(X, y, test_size=0.3, random_state=1)
    data.iloc[ : , 0] = data.iloc[ : , 0].str.lower()
    hmm = HMM(data)

    print(hmm.sensor_matrix)




def test():
    memo = {'ovnis': 1}
    # memo['ovnis'] += 1
    memo['perros'] = 1
    print(memo['perros'])

if __name__ == '__main__':
    main()
    # test()