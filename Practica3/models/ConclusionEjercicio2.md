Claramente el modelo que peor desempeño tuvo fue el DecisionTree.

Por otro lado, se puede decir que hay un empate entre el Perceptron y el KNN.
Sin embargo, aún podríamos hacer más cosas:
1. Realizar otros métodos de evaluación de modelos como K-Folds Cross Validation o B-Repeated Holdout.
2. El Perceptron tiene mejor precisión que el KNN prediciendo algunos dígitos y viceversa, entonces si se desea saber con certeza si una futura observación pertenece a la clase del dígito 1 (por ejemplo), sería mejor tomar la decisión del Perceptron. Mientras que por otro lado, si se quisiera predecir exactamente si la clase de una nueva observación es la del dígito 9 (por ejemplo), podríamos confiar más en la decisión de KNN, pues este modelo tiene mejor precisión clasificando este dígito en particular (y Perceptron el dígito 1, por ejemplo). Esto son sólo casos particulares en los cuales podríamos decidir por uno u otro, pero en términos generales ambos tienen prácticamente el mismo desempeño.