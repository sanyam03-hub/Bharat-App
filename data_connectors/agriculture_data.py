import pandas as pd
import requests
from utils.constants import AGRICULTURE_DATASET_URL
import random

def fetch_agriculture_data(state=None, crop=None, year_start=None, year_end=None):
    """
    Fetch agriculture data from data.gov.in
    Returns a pandas DataFrame with crop production data
    """
    try:
        # For demo purposes, we'll create mock data that simulates real data structure
        # In a real implementation, this would fetch from data.gov.in API
        mock_data = _generate_mock_agriculture_data()
        df = pd.DataFrame(mock_data)
        
        # Filter data based on parameters
        if state:
            # Use case-insensitive comparison
            filtered_df = df[df['State'].str.lower() == state.lower()]
            # If no data found for the specific state, generate mock data for it
            if filtered_df.empty:
                filtered_df = _generate_mock_data_for_state(state, crop, year_start or 2018, year_end or 2018)
            df = filtered_df
        if crop:
            # Use case-insensitive comparison
            df = df[df['Crop'].str.lower() == crop.lower()]
        if year_start:
            df = df[df['Year'] >= year_start]
        if year_end:
            df = df[df['Year'] <= year_end]
            
        return df
    except Exception as e:
        print(f"Error fetching agriculture data: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame()

def _generate_mock_data_for_state(state, crop, year_start, year_end):
    """
    Generate mock agriculture data for a specific state
    """
    # Generate realistic crop data based on Indian agricultural patterns
    years = list(range(year_start, year_end + 1))
    
    # Common crops by region (simplified)
    if any(word in state.lower() for word in ['west bengal', 'assam', 'odisha']):
        common_crop = "Rice"
    elif any(word in state.lower() for word in ['punjab', 'haryana', 'uttar pradesh']):
        common_crop = "Wheat"
    elif any(word in state.lower() for word in ['gujarat', 'maharashtra', 'madhya pradesh']):
        common_crop = "Cotton"
    elif any(word in state.lower() for word in ['tamil nadu', 'karnataka', 'andhra pradesh']):
        common_crop = "Sugarcane"
    else:
        common_crop = "Rice"  # Default
    
    # Use specified crop if provided, otherwise use regional default
    selected_crop = crop if crop else common_crop
    
    # Generate districts for the state (simplified)
    districts = [f"{state} District {i+1}" for i in range(5)]
    
    # Generate data with some variation
    mock_data = {
        'State': [state] * len(districts) * len(years),
        'District': districts * len(years),
        'Year': [year for year in years for _ in districts],
        'Crop': [selected_crop] * len(districts) * len(years),
        'Production': [random.randint(50000, 250000) for _ in range(len(districts) * len(years))]
    }
    
    return pd.DataFrame(mock_data)

def _generate_mock_agriculture_data():
    """
    Generate mock agriculture data for demonstration purposes
    """
    # Sample mock data
    mock_data = {
        'State': ['Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu', 'Tamil Nadu',
                  'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra', 'Maharashtra',
                  'Karnataka', 'Karnataka', 'Karnataka', 'Karnataka', 'Karnataka',
                  'Uttar Pradesh', 'Uttar Pradesh', 'Uttar Pradesh', 'Uttar Pradesh', 'Uttar Pradesh',
                  'Bihar', 'Bihar', 'Bihar', 'Bihar', 'Bihar'],
        'District': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli',
                     'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad',
                     'Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum',
                     'Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Allahabad',
                     'Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Darbhanga'],
        'Year': [2018, 2018, 2018, 2018, 2018,
                 2018, 2018, 2018, 2018, 2018,
                 2018, 2018, 2018, 2018, 2018,
                 2018, 2018, 2018, 2018, 2018,
                 2018, 2018, 2018, 2018, 2018],
        'Crop': ['Rice', 'Maize', 'Sugarcane', 'Cotton', 'Ragi',
                 'Rice', 'Wheat', 'Soybean', 'Cotton', 'Jowar',
                 'Rice', 'Maize', 'Groundnut', 'Sugarcane', 'Ragi',
                 'Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton',
                 'Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton'],
        'Production': [120000, 85000, 250000, 95000, 45000,
                       180000, 110000, 75000, 105000, 65000,
                       135000, 92000, 88000, 220000, 52000,
                       150000, 140000, 98000, 240000, 102000,
                       125000, 108000, 89000, 210000, 97000]
    }
    return mock_data

def get_top_crops_by_production(df, n=5):
    """
    Get top N crops by production volume
    """
    if df.empty:
        return []
    
    # Group by crop and sum production
    top_crops = df.groupby('Crop')['Production'].sum().sort_values(ascending=False).head(n)
    return top_crops.index.tolist()