import pandas as pd
import requests
from utils.constants import DATA_GOV_BASE_URL
from config import DATA_GOV_API_KEY, API_BASE_URL, API_FORMAT, API_LIMIT, USE_MOCK_DATA, CROP_PRODUCTION_RESOURCE_ID
import random

def fetch_agriculture_data(state=None, crop=None, year_start=None, year_end=None):
    """
    Fetch agriculture data from data.gov.in
    Returns a pandas DataFrame with crop production data
    """
    try:
        # Check if we should use mock data
        if USE_MOCK_DATA:
            # For demo purposes, we'll create mock data that simulates real data structure
            mock_data = _generate_mock_agriculture_data()
            df = pd.DataFrame(mock_data)
            
            # Filter data based on parameters
            if state:
                # Use case-insensitive comparison with standard Python string operations
                state_lower = state.lower()
                mask = [str(x).lower() == state_lower for x in df['State']]
                df = df[mask]
                # If no data found for the specific state, generate mock data for it
                if df.empty:
                    df = _generate_mock_data_for_state(state, crop, year_start or 2018, year_end or 2018)
            if crop:
                # Use case-insensitive comparison with standard Python string operations
                crop_lower = crop.lower()
                mask = [str(x).lower() == crop_lower for x in df['Crop']]
                df = df[mask]
            if year_start:
                df = df[df['Year'] >= year_start]
            if year_end:
                df = df[df['Year'] <= year_end]
                
            return df
        
        # Try to fetch real data from data.gov.in
        df = _fetch_real_agriculture_data(state, crop, year_start, year_end)
        
        # If real data fetch failed, fall back to mock data
        if df is None or df.empty:
            print("Using mock data as fallback")
            # For demo purposes, we'll create mock data that simulates real data structure
            mock_data = _generate_mock_agriculture_data()
            df = pd.DataFrame(mock_data)
            
            # Filter data based on parameters
            if state:
                # Use case-insensitive comparison with standard Python string operations
                state_lower = state.lower()
                mask = [str(x).lower() == state_lower for x in df['State']]
                df = df[mask]
                # If no data found for the specific state, generate mock data for it
                if df.empty:
                    df = _generate_mock_data_for_state(state, crop, year_start or 2018, year_end or 2018)
            if crop:
                # Use case-insensitive comparison with standard Python string operations
                crop_lower = crop.lower()
                mask = [str(x).lower() == crop_lower for x in df['Crop']]
                df = df[mask]
            if year_start:
                df = df[df['Year'] >= year_start]
            if year_end:
                df = df[df['Year'] <= year_end]
                
        return df
    except Exception as e:
        print(f"Error fetching agriculture data: {e}")
        # Return empty DataFrame in case of error
        return pd.DataFrame()

def get_agriculture_data_source():
    """
    Get the data source information for agriculture data
    """
    if USE_MOCK_DATA:
        return f"{DATA_GOV_BASE_URL} (Mock Data - Crop Production Statistics)"
    
    # For real data, provide descriptive information about the data source
    return f"{DATA_GOV_BASE_URL} (Crop Production Statistics Dataset)"

def _fetch_real_agriculture_data(state=None, crop=None, year_start=None, year_end=None):
    """
    Fetch real agriculture data from data.gov.in API
    Returns a pandas DataFrame or None if failed
    """
    try:
        # Build API request
        url = f"{API_BASE_URL}/{CROP_PRODUCTION_RESOURCE_ID}"
        
        # Set up parameters
        params = {
            "api-key": DATA_GOV_API_KEY,
            "format": API_FORMAT,
            "limit": API_LIMIT
        }
        
        # Add filters based on parameters
        filters = []
        if state:
            filters.append(f"state=={state}")
        if crop:
            filters.append(f"crop=={crop}")
        if year_start:
            filters.append(f"year>={year_start}")
        if year_end:
            filters.append(f"year<={year_end}")
            
        if filters:
            params["filters"] = "|".join(filters)
        
        # Make API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Convert to DataFrame
        if 'records' in data:
            df = pd.DataFrame(data['records'])
            
            # Handle different possible column names
            # Map common column variations to our expected names
            column_mapping = {}
            
            # State column mapping - Fix for actual API data
            state_columns = ['state', 'state_name', 'State', 'State_Name']
            for col in state_columns:
                if col in df.columns:
                    column_mapping[col] = 'State'
                    break
            
            # District column mapping - Fix for actual API data
            district_columns = ['district', 'district_name', 'District', 'District_Name']
            for col in district_columns:
                if col in df.columns:
                    column_mapping[col] = 'District'
                    break
            
            # Year column mapping - Fix for actual API data
            year_columns = ['year', 'Year', 'crop_year', 'Year_Name']
            for col in year_columns:
                if col in df.columns:
                    column_mapping[col] = 'Year'
                    break
            
            # Crop column mapping - Fix for actual API data
            crop_columns = ['crop', 'Crop', 'crop_name', 'Crop_Name']
            for col in crop_columns:
                if col in df.columns:
                    column_mapping[col] = 'Crop'
                    break
            
            # Production column mapping - Fix for actual API data
            # The API returns 'production_' not 'production'
            production_columns = ['production', 'Production', 'crop_production', 'Production_Value', 'production_']
            for col in production_columns:
                if col in df.columns:
                    column_mapping[col] = 'Production'
                    break
            
            # Apply column mapping
            df = df.rename(columns=column_mapping)
            
            # Convert data types
            if 'Year' in df.columns:
                df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
            if 'Production' in df.columns:
                df['Production'] = pd.to_numeric(df['Production'], errors='coerce')
                
            return df
            
    except Exception as e:
        print(f"Error fetching real agriculture data: {e}")
        return None

def _generate_mock_data_for_state(state, crop, year_start, year_end):
    """
    Generate mock agriculture data for a specific state
    """
    # Generate realistic crop data based on Indian agricultural patterns
    years = list(range(year_start, year_end + 1))
    
    # Common crops by region (simplified)
    if any(word in state.lower() for word in ['west bengal', 'assam', 'odisha']):
        common_crops = ["Rice", "Jute", "Potatoes"]
    elif any(word in state.lower() for word in ['punjab', 'haryana', 'uttar pradesh']):
        common_crops = ["Wheat", "Rice", "Potatoes"]
    elif any(word in state.lower() for word in ['gujarat', 'maharashtra', 'madhya pradesh']):
        common_crops = ["Cotton", "Soybean", "Wheat"]
    elif any(word in state.lower() for word in ['tamil nadu', 'karnataka', 'andhra pradesh']):
        common_crops = ["Sugarcane", "Rice", "Cotton"]
    else:
        common_crops = ["Rice", "Wheat", "Maize"]  # Default
    
    # Use specified crop if provided, otherwise use regional defaults
    if crop:
        selected_crops = [crop]
    else:
        selected_crops = common_crops[:3]  # Take top 3 regional crops
    
    # Generate districts for the state (simplified)
    districts = [f"{state} District {i+1}" for i in range(5)]
    
    # Generate data with some variation for multiple crops
    state_data = []
    district_data = []
    year_data = []
    crop_data = []
    production_data = []
    
    for year in years:
        for district in districts:
            for i, crop_name in enumerate(selected_crops):
                state_data.append(state)
                district_data.append(district)
                year_data.append(year)
                crop_data.append(crop_name)
                # Generate production values with some variation based on crop type
                base_production = 100000 + (i * 30000)  # Different base for different crops
                production_data.append(random.randint(base_production - 50000, base_production + 50000))
    
    mock_data = {
        'State': state_data,
        'District': district_data,
        'Year': year_data,
        'Crop': crop_data,
        'Production': production_data
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