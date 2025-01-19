import pandas as pd

def make_stationary(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms all time series in the DataFrame by applying the first difference 
    to ensure stationarity.
    
    Args:
    - data (pd.DataFrame): Input DataFrame with time series as columns.
    
    Returns:
    - pd.DataFrame: Transformed DataFrame with stationary series.
    """
    # Apply first difference to all columns
    stationary_data = data.diff().dropna()
    
    return stationary_data
