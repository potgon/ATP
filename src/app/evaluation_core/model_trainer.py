from sklearn.model_selection import train_test_split


class ModelTrainer:
    def __init__(self, model, parameters=None):
        """
        Initialize the ModelTrainer with a specific model and optional parameters.

        Args:
            model: The predictive model to be trained.
            parameters: Optional parameters for the model. Defaults to None.
        """
        self.model = model
        self.parameters = parameters
        self.trained_model = None

        def split_data(self, X, y, test_size=0.2, random_state=None):
            """
            Split the dataset into training and testing sets.

            Args:
                X (_type_): Feature matrix.
                y (_type_): Target variable.
                test_size (float, optional): Proportion of the dataset to include in the test split. Defaults to 0.2.
                random_state (_type_, optional): Controls the shuffling applied to the data before the split. Defaults to None.
            """
            return train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )

        def preprocess_data(self, X_train, X_test):
            """
            Preprocess the data (e.g., scaling, normalization) before training the model.
            Override this method based on specific model requirements.

                Args:
                    X_train (_type_): Training feature matrix.
                    X_test (_type_): Testing feature matrix.
            """

        def train_model(self, X_train, y_train):
            """
            Train the model using the training dataset.

            Args:
                X_train (_type_): Training feature matrix.
                y_train (_type_): Training target variable.
            """
            # Fit the model
            self.trained_model = self.model.fit(X_train, y_train)

        def evaluate_model(self, X_test, y_test):
            """
            Evaluate the model using the testing dataset.

            Args:
                X_test (_type_): Testing feature matrix.
                y_test (_type_): Testing target variable.
            """
            # Implement evaluation logic (e.g., accuracy for classification)
            # This method should be adjusted based on the model and problem type
            return self.trained_model.score(X_test, y_test)

        def predict(self, X):
            """
            Make predictions using the trained model.

            Args:
                X (_type_): Feature matrix for which to make predictions.
            """
            return self.trained_model.predict(X)
