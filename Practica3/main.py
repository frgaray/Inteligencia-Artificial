from sklearn import datasets, linear_model, tree, neighbors, pipeline, preprocessing, cluster
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from os.path import abspath, dirname, join

cwd = abspath(dirname(__file__))


def predict_linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)

    reg = linear_model.LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    with open(join(cwd, "models", "LinearRegression.txt"), 'w') as f:
        f.write(f"MSE: {mean_squared_error(y_test, y_pred)}\n")
        f.write(f"Coeficiente de Determinación (R^2): {r2_score(y_test, y_pred)}")

def predict_classifiers(classifiers, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)
    for clf, name in classifiers:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        with open(join(cwd, "models", f"{name}.txt"), 'w') as f:
            f.write(classification_report(y_test, y_pred))

def plot_inciso_3b(X, y_pred):
    fig, axs = plt.subplots()
    axs.scatter(X[:, 0], X[:, 1], c=y_pred)

    plt.suptitle("Gráfica Inciso 3b) xd")
    plt.show()

def main():
    # Ejercicio 1
    X, y = datasets.load_diabetes(return_X_y=True)
    predict_linear_regression(X, y)
    
    # Ejercicio 2
    X, y = datasets.load_digits(return_X_y=True)

    # Pasos para el Pipeline de KNN. Para incluir el escalamiento de los datos
    knn_steps = [("scaler", preprocessing.StandardScaler()),
                 ("knn", neighbors.KNeighborsClassifier(n_neighbors=10))]
    
    # Lista de tuplas de los clasificadores a comparar, en la forma (clf, str_name)
    classifiers = [(linear_model.Perceptron(random_state=0, max_iter=1000, eta0=1), "Perceptron"),
                   (tree.DecisionTreeClassifier(random_state=0), "DecisionTree"),
                   (pipeline.Pipeline(knn_steps), "KNN")]
    predict_classifiers(classifiers, X, y)

    # Ejercicio 3
    X, y = datasets.make_blobs(1000, random_state=0)
    kmeans = cluster.KMeans(n_clusters=3)
    y_pred = kmeans.fit_predict(X)
    plot_inciso_3b(X, y_pred)
    
if __name__ == "__main__":
    main()