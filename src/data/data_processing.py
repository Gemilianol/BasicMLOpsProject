from datetime import datetime
import pandas as pd
import os

import warnings
warnings.filterwarnings("ignore")

def load_series(file_path, date_col, value_col, sep=";", date_format=None):
    """
    Load and clean the dataset to obtain a time series (pd.Series).
    
    Args:
    - file_path (str): File path of the raw CSV file.
    - date_col (str): Date column name.
    - value_col (str): Value column name.
    - sep (str): Separator of the CSV file. Default is ";".
    - date_format (str, optional): Date format to explicitly convert it.
    
    Returns:
    - pd.Series: Time series with the index as monthly periods and corresponding values.
    """
    # Load the file
    data = pd.read_csv(file_path, sep=sep)

    # Clean column names and strip white spaces in date column
    data.columns = data.columns.str.replace(r'\n', ' ', regex=True)
    data[date_col] = data[date_col].str.strip()

    # Handle numeric conversion for value column
    if data[value_col].dtype == "object":
        data[value_col] = data[value_col].str.replace(",", ".").astype(float)

    # Map months from Spanish to English if applicable
    month_map = {
        "ene": "Jan", "feb": "Feb", "mar": "Mar", "abr": "Apr", "may": "May", "jun": "Jun",
        "jul": "Jul", "ago": "Aug", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dec"
    }
    if data[date_col].str.contains(r"^\s*(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s*-\s*\d{2}$", 
                                   regex=True, na=False).any():
        data[date_col] = data[date_col].replace(month_map, regex=True)

    # Convert date column to datetime format
    data[date_col] = pd.to_datetime(data[date_col], format=date_format, errors="coerce")

    # Drop duplicates and sort by date
    data.drop_duplicates(subset=[date_col], inplace=True)
    data.sort_values(by=date_col, inplace=True)

    # Set index to the date column
    data.set_index(date_col, inplace=True)

    # Create time series
    ts = data[value_col]

    # Fill missing dates with a continuous daily index
    full_index = pd.date_range(start=ts.index.min(), end=ts.index.max(), freq='D')
    ts = ts.reindex(full_index)

    # Forward-fill missing values (e.g., for weekends)
    ts.fillna(method='ffill', inplace=True)

    # Resample to monthly frequency and take the median
    ts = ts.resample("M").median()

    # Convert index to monthly period format
    ts.index = ts.index.to_period('M')

    return ts

def get_series():
    base_dir = "data"  # Adjusted to start from the project root directory
    datasets = [
        {"file_path": os.path.join(base_dir, "raw/exchange_rate.csv"), 
         "date_col": "Mes", "value_col": "Tipo de cambio nominal promedio mensual", 
         "date_format": "%b-%y"},
        {"file_path": os.path.join(base_dir, "raw/informal_exchange_rate.csv"), 
         "date_col": "Fecha", "value_col": "Venta", "date_format": "%d/%m/%Y"},
        {"file_path": os.path.join(base_dir, "raw/inflation_data.csv"), 
         "date_col": "Fecha", "value_col": "Valor", "date_format": "%d/%m/%Y"},
        {"file_path": os.path.join(base_dir, "raw/M2_variation.csv"), 
         "date_col": "Fecha", "value_col": "Valor", "date_format": "%d/%m/%Y"},
        {"file_path": os.path.join(base_dir, "raw/interest_rate.csv"), 
         "date_col": "Fecha", "value_col": "Valor", "date_format": "%d/%m/%Y"},
        {"file_path": os.path.join(base_dir, "raw/IPMP.csv"), 
         "date_col": "Período", "value_col": "IPMP (dic-01=100)", "date_format": "%b-%y"},
        {"file_path": os.path.join(base_dir, "raw/IPMP.csv"), 
         "date_col": "Período", "value_col": "IPMP Agropecuario (dic-01=100)", "date_format": "%b-%y"},
        {"file_path": os.path.join(base_dir, "raw/IPMP.csv"), 
         "date_col": "Período", "value_col": "IPMP Metales (dic-01=100)", "date_format": "%b-%y"},
        {"file_path": os.path.join(base_dir, "raw/IPMP.csv"), 
         "date_col": "Período", "value_col": "IPMP Petróleo (dic-01=100)", "date_format": "%b-%y"},
    ]
    
    # Load all the series
    # Three datasets have the same key so in order to avoid replace the values of the column "Valor":
    series = {
    f"{os.path.splitext(os.path.basename(ds['file_path']))[0]}_{ds['value_col']}": load_series(**ds)
    for ds in datasets
    }
        
    # Combine all series into one DataFrame
    processed_dataset = pd.concat(series.values(), axis=1)
    
    # Rename columns
    processed_dataset.columns = ['Official Exchange Rate', 'Informal Exchange Rate', 'Inflation', 'Monetary Supply (M2)', 'Interest Rate', 
                                 'General IPMP', 'Agriculture IPMP', 'Metals IPMP', 'Crude Oil IPMP']
    
    # Drop rows with NaN values (Since not all the series has the same time lentgh)
    processed_dataset = processed_dataset.dropna()
    
    # # Define the output file path
    output_path = os.path.join(base_dir, "processed/combined_cleaned_data.csv")
    
    # # If file exists, rename with timestamp
    if os.path.exists(output_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_path.replace(".csv", f"_{timestamp}.csv")
    
    # # Save to CSV
    processed_dataset.to_csv(output_path)
    print(f"File saved as '{output_path}'.")
    
    return processed_dataset

if __name__ == "__main__":
    get_series()
