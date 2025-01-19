from data.data_processing import get_series
from features.stationarity import make_stationary

def process_features():
    """
    Processes the raw combined data to produce a stationary DataFrame.

    Returns:
    - pd.DataFrame: A DataFrame with stationary time series.
    """
    # Get the series as DataFrame
    combined_data = get_series()
    
    # Apply the first difference to all the series on the DataFrame
    stationary_data = make_stationary(combined_data)
    
    return stationary_data