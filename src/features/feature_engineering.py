from data.data_processing import get_series
from features.stationarity import make_stationary

def process_features():
    """
    Processes the raw combined data to produce a stationary DataFrame.

    Returns:
    - pd.DataFrame: A DataFrame with stationary time series.
    """
    # Obtener el dataset combinado
    combined_data = get_series()
    
    # Aplicar transformación para hacerlo estacionario
    stationary_data = make_stationary(combined_data)
    
    return stationary_data