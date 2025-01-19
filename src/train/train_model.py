from features.feature_engineering import process_features

def train_model():
    """
    Main function to train the model.
    """
    # Obtener los datos estacionarios
    stationary_data = process_features()
    
    # Continuar con el entrenamiento del modelo usando stationary_data
    print(stationary_data.head())
    # Aquí seguirías con la lógica de entrenamiento...

if __name__ == "__main__":
    train_model()
