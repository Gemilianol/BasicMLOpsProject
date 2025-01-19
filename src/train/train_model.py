import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from pmdarima import auto_arima
from features.feature_engineering import process_features
import warnings
import mlflow
import mlflow.sklearn
import mlflow.models.signature
from mlflow.models.signature import infer_signature
import os
import yaml

warnings.simplefilter(action='ignore', category=FutureWarning)

def load_config():
    """Load configuration from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), "../config/train_config.yaml")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def train_model():
    """
    Main function to train the model with MLflow tracking.
    """
    # Load configuration
    config = load_config()

    # Get the stationarity data
    stationary_data = process_features()
    
    # Separate the independent variables (X) from target variable (y)
    target = config['target_variable']
    X = stationary_data.drop(columns=[target])
    y = stationary_data[target]

    # Train-test split
    test_size = config["train"]["test_size"]
    random_state = config["train"]['random_state']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, 
                                                        random_state=random_state, 
                                                        shuffle=False)  # No shuffle to keep time order.
    
    with mlflow.start_run(run_name="model_training_pipeline") as run:
        try:
            # Fit AutoARIMA
            seasonal = config['arima']['seasonal']
            m = config['arima']['seasonal_period']
            arima_model = auto_arima(y_train, seasonal=seasonal, m=m, trace=True, error_action='ignore', suppress_warnings=True)
            
            if len(y_test) == 0:
                raise ValueError("y_test is empty. Ensure the train-test split is correct.")
            arima_forecast = arima_model.predict(n_periods=int(len(y_test))) # n_periods must be an integer

            arima_rmse = np.sqrt(mean_squared_error(y_test, arima_forecast))
            print("\n" + "-"*50 + "\n")
            print(f"AutoARIMA RMSE: {arima_rmse:.4f}")
            
            # Log ARIMA metrics
            mlflow.log_metric("arima_rmse", arima_rmse)
            
        except Exception as e:
            print(f"Error during ARIMA fitting: {e}")
            arima_model = None
            arima_rmse = float('inf')

        try:
            # Train Linear Regression
            linear_model = LinearRegression()
            linear_model.fit(X_train, y_train)
            linear_forecast = linear_model.predict(X_test)
            linear_rmse = np.sqrt(mean_squared_error(y_test, linear_forecast))
            print("\n" + "-"*50 + "\n")
            print(f"Linear Regression RMSE: {linear_rmse:.4f}")
            
            # Log Linear Regression metrics
            mlflow.log_metric("linear_rmse", linear_rmse)
            
        except Exception as e:
            print(f"Error during Linear Regression training: {e}")
            linear_model = None
            linear_rmse = float('inf')

        # Select best model
        if arima_rmse < linear_rmse:
            best_model, best_model_name = arima_model, "AutoARIMA"
        else:
            best_model, best_model_name = linear_model, "Linear Regression"

        print("\n" + "-"*50 + "\n")
        print(f"Best model: {best_model_name}")
        
        # Log best model name and parameters
        mlflow.log_param("best_model", best_model_name)
        
        # Solving warning: MLflow Warning: Missing Model Signature and Input Example
        
        # Infer the signature
        signature = infer_signature(X_train, y_train)
        
        # Log the model to MLflow
        artifact_path = "best_model"
        mlflow.sklearn.log_model(
            sk_model=best_model,
            artifact_path=artifact_path,
            signature=signature
        )

        # Output the logged model URI
        model_uri = f"runs:/{mlflow.active_run().info.run_id}/{artifact_path}"
        print(f"Model logged at: {model_uri}")

        print("\n" + "-"*50 + "\n")
        print(f"{best_model_name} logged to MLflow.")

if __name__ == "__main__":
    train_model()
