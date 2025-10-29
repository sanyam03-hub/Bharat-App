import pandas as pd
import requests
from utils.constants import CLIMATE_DATASET_URL
import random

def fetch_climate_data(state=None, year_start=None, year_end=None):
    """
    Fetch climate data (rainfall) from data.gov.in
    Returns a pandas DataFrame with rainfall data
    """
    try:
        # For demo purposes, we'll create mock data that simulates real data structure
        # In a real implementation, this would fetch from data.gov.in API
        mock_data = _generate_mock_climate_data()
        df = pd.DataFrame(mock_data)
        
        # Filter data based on parameters
        if state:
            filtered_df = df[df['State'].str.lower() == state.lower()]
            # If no data found for the specific state, generate mock data for it
            if filtered_df.empty:
                filtered_df = _generate_mock_data_for_state(state, year_start or 2016, year_end or 2020)
            df = filtered_df
        if year_start:
            df = df[df['Year'] >= year_start]
        if year_end:
            df = df[df['Year'] <= year_end]
            
        return df
    except Exception as e:
        print(f"Error fetching climate data: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame()

def _generate_mock_data_for_state(state, year_start, year_end):
    """
    Generate mock climate data for a specific state
    """
    # Generate realistic rainfall data based on Indian climate patterns
    years = list(range(year_start, year_end + 1))
    
    # Base rainfall varies by region (simplified)
    if any(word in state.lower() for word in ['tamil', 'kerala', 'coastal']):
        base_rainfall = 1200  # High rainfall
    elif any(word in state.lower() for word in ['rajasthan', 'gujarat', 'haryana']):
        base_rainfall = 600   # Low rainfall
    else:
        base_rainfall = 900   # Moderate rainfall
    
    # Generate data with some variation
    mock_data = {
        'State': [state] * len(years),
        'Year': years,
        'Rainfall': [base_rainfall + random.randint(-200, 200) for _ in years]
    }
    
    return pd.DataFrame(mock_data)

def _generate_mock_climate_data():
    """
    Generate mock climate data for demonstration purposes
    """
    # Sample mock data
    mock_data = {
        'State': ['Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu',
                  'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra',
                  'Karnataka', 'Karnataka', 'Karnataka', 'Karnataka', 'Karnataka'],
        'Year': [2016, 2017, 2018, 2019, 2020,
                 2016, 2017, 2018, 2019, 2020,
                 2016, 2017, 2018, 2019, 2020],
        'Rainfall': [950, 1020, 890, 920, 980,
                     1120, 1080, 1050, 1100, 1070,
                     1250, 1300, 1280, 1220, 1260]
    }
    return mock_data

def get_average_rainfall(df):
    """
    Calculate average rainfall from the dataframe
    """
    if df.empty or 'Rainfall' not in df.columns:
        return 0
    
    return df['Rainfall'].mean()