import pandas as pd
from data_connectors.agriculture_data import fetch_agriculture_data, get_top_crops_by_production
from data_connectors.climate_data import fetch_climate_data, get_average_rainfall
from utils.constants import AGRICULTURE_DATASET_URL, CLIMATE_DATASET_URL
import matplotlib.pyplot as plt
import numpy as np

def generate_answer(intent, params):
    """
    Generate answer based on intent and parameters
    Returns answer text, chart (if any), and data sources
    """
    answer = ""
    chart = None
    sources = []
    
    if intent == "compare_rainfall":
        answer, chart, sources = _handle_compare_rainfall(params)
    elif intent == "crop_trend":
        answer, chart, sources = _handle_crop_trend(params)
    elif intent == "highest_wheat_production":
        answer, chart, sources = _handle_highest_wheat_production(params)
    elif intent == "top_crops":
        answer, chart, sources = _handle_top_crops(params)
    elif intent == "analyze_correlation":
        answer, chart, sources = _handle_analyze_correlation(params)
    elif intent == "climate_info":
        answer, chart, sources = _handle_climate_info(params)
    elif intent == "crop_production":
        answer, chart, sources = _handle_crop_production(params)
    elif intent == "general_query":
        answer, chart, sources = _handle_general_query(params)
    else:
        answer = "I'm sorry, I couldn't understand your query. Please try rephrasing."
        sources = []
    
    return answer, chart, sources

def _ensure_dataframe(df):
    """Ensure we have a proper pandas DataFrame"""
    if isinstance(df, pd.DataFrame):
        return df
    # If it's not a DataFrame, create an empty one
    return pd.DataFrame()

def _handle_climate_info(params):
    """Handle climate information queries"""
    states = params.get('states', [])
    year_start = params.get('year_start', 2016)
    year_end = params.get('year_end', 2020)
    
    if not states:
        return "Please specify a state for climate information.", None, []
    
    state = states[0]
    
    # Fetch climate data
    df = fetch_climate_data(state=state, year_start=year_start, year_end=year_end)
    df = _ensure_dataframe(df)
    
    # Check if DataFrame is empty
    if df.empty:
        return f"No climate data available for {state}.", None, [CLIMATE_DATASET_URL]
    
    # Calculate statistics
    avg_rainfall = float(df['Rainfall'].mean())
    min_rainfall = float(df['Rainfall'].min())
    max_rainfall = float(df['Rainfall'].max())
    
    answer = f"Climate information for {state} ({year_start}-{year_end}):\n"
    answer += f"- Average annual rainfall: {avg_rainfall:.0f} mm\n"
    answer += f"- Minimum annual rainfall: {min_rainfall:.0f} mm\n"
    answer += f"- Maximum annual rainfall: {max_rainfall:.0f} mm"
    
    # Create rainfall trend chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Year'], df['Rainfall'], marker='o', color='blue')
    ax.set_ylabel('Rainfall (mm)')
    ax.set_xlabel('Year')
    ax.set_title(f'Annual Rainfall Trend in {state}')
    plt.tight_layout()
    
    sources = [CLIMATE_DATASET_URL]
    return answer, fig, sources

def _handle_crop_production(params):
    """Handle crop production queries"""
    states = params.get('states', [])
    crops = params.get('crops', [])
    year_start = params.get('year_start', 2018)
    year_end = params.get('year_end', 2018)
    
    if not states:
        return "Please specify a state for crop production information.", None, []
    
    state = states[0]
    crop = crops[0] if crops else "Rice"  # Default to rice
    
    # Fetch data
    df = fetch_agriculture_data(state=state, crop=crop, year_start=year_start, year_end=year_end)
    df = _ensure_dataframe(df)
    
    # Check if DataFrame is empty
    if df.empty:
        return f"No data available for {crop} production in {state}.", None, [AGRICULTURE_DATASET_URL]
    
    total_production = float(df['Production'].sum())
    
    answer = f"{crop} production in {state} was {total_production:,.0f} units during {year_start}-{year_end}."
    
    # If we have district-wise data, show top districts
    if len(df) > 1:
        # Sort by production and get top 3
        sorted_df = df.sort_values(by='Production', ascending=False)
        top_districts = sorted_df.head(3)
        answer += "\n\nTop producing districts:"
        for _, row in top_districts.iterrows():
            answer += f"\n- {row['District']}: {float(row['Production']):,.0f} units"
    
    sources = [AGRICULTURE_DATASET_URL]
    return answer, None, sources

def _handle_general_query(params):
    """Handle general queries"""
    states = params.get('states', [])
    crops = params.get('crops', [])
    
    if states and not crops:
        # State-specific query, likely about climate
        return _handle_climate_info(params)
    elif states and crops:
        # State and crop-specific query
        return _handle_crop_production(params)
    elif crops and not states:
        # Crop-specific query without state
        return "Please specify a state along with the crop for more accurate information.", None, []
    else:
        # Truly general query
        return "I'm sorry, I couldn't understand your query. Please try rephrasing or ask about specific states and crops.", None, []

def _handle_compare_rainfall(params):
    """Handle rainfall comparison queries"""
    states = params.get('states', [])
    year_start = params.get('year_start', 2015)
    year_end = params.get('year_end', 2020)
    
    if len(states) < 2:
        return "Please specify at least two states for comparison.", None, []
    
    rainfall_data = {}
    for state in states[:3]:  # Limit to 3 states
        df = fetch_climate_data(state=state, year_start=year_start, year_end=year_end)
        df = _ensure_dataframe(df)
        if df.empty:
            continue
        avg_rainfall = float(get_average_rainfall(df))
        rainfall_data[state] = avg_rainfall
    
    if not rainfall_data:
        return "No climate data available for the specified states.", None, [CLIMATE_DATASET_URL]
    
    # Generate answer
    state_rainfall_list = [f"{state} received {rainfall:.0f} mm" for state, rainfall in rainfall_data.items()]
    answer = f"Average rainfall comparison ({year_start}-{year_end}): " + ", ".join(state_rainfall_list) + "."
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    states_list = list(rainfall_data.keys())
    rainfall_list = list(rainfall_data.values())
    ax.bar(states_list, rainfall_list, color=['blue', 'green', 'red'])
    ax.set_ylabel('Average Rainfall (mm)')
    ax.set_title('Average Rainfall Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    sources = [CLIMATE_DATASET_URL]
    return answer, fig, sources

def _handle_crop_trend(params):
    """Handle crop trend analysis queries"""
    crops = params.get('crops', [])
    states = params.get('states', [])
    year_start = params.get('year_start', 2010)
    year_end = params.get('year_end', 2020)
    
    if not states:
        return "Please specify a state for trend analysis.", None, []
    
    state = states[0]
    crop = crops[0] if crops else "Rice"  # Default to rice
    
    # Fetch data
    df = fetch_agriculture_data(state=state, crop=crop, year_start=year_start, year_end=year_end)
    df = _ensure_dataframe(df)
    
    if df.empty:
        return f"No data available for {crop} production in {state}.", None, [AGRICULTURE_DATASET_URL]
    
    # Calculate trend
    avg_production = float(df['Production'].mean())
    
    answer = f"{crop} production in {state} averaged {avg_production:,.0f} units from {year_start}-{year_end}."
    
    # Create trend chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Year'], df['Production'], marker='o')
    ax.set_ylabel('Production')
    ax.set_xlabel('Year')
    ax.set_title(f'{crop} Production Trend in {state}')
    plt.tight_layout()
    
    sources = [AGRICULTURE_DATASET_URL]
    return answer, fig, sources

def _handle_highest_wheat_production(params):
    """Handle highest wheat production queries"""
    states = params.get('states', [])
    year = params.get('years', [2020])[-1]  # Use the latest year if multiple provided
    
    if not states:
        return "Please specify a state for wheat production analysis.", None, []
    
    state = states[0]
    
    # Fetch data for wheat in the specified state and year
    df = fetch_agriculture_data(state=state, crop="Wheat", year_start=year, year_end=year)
    df = _ensure_dataframe(df)
    
    if df.empty:
        return f"No wheat production data available for {state} in {year}.", None, [AGRICULTURE_DATASET_URL]
    
    # Find district with highest production
    max_idx = df['Production'].idxmax()
    max_production_row = df.loc[max_idx]
    district = max_production_row['District']
    production = float(max_production_row['Production'])
    
    answer = f"In {year}, {district} district in {state} produced the most wheat with {production:,.0f} units."
    
    sources = [AGRICULTURE_DATASET_URL]
    return answer, None, sources

def _handle_top_crops(params):
    """Handle top crops queries"""
    states = params.get('states', [])
    year = params.get('years', [2020])[-1]  # Use the latest year if multiple provided
    
    if not states:
        return "Please specify a state for crop analysis.", None, []
    
    state = states[0]
    
    # Fetch data for the specified state and year
    df = fetch_agriculture_data(state=state, year_start=year, year_end=year)
    df = _ensure_dataframe(df)
    
    if df.empty:
        return f"No crop production data available for {state} in {year}.", None, [AGRICULTURE_DATASET_URL]
    
    # Get top crops
    top_crops = get_top_crops_by_production(df, 3)
    
    if not top_crops:
        return f"No crop production data available for {state} in {year}.", None, [AGRICULTURE_DATASET_URL]
    
    # Convert to string list if needed
    top_crops_str = [str(crop) for crop in top_crops]
    crops_list = ", ".join(top_crops_str)
    answer = f"The top 3 crops in {state} by production volume in {year} were: {crops_list}."
    
    sources = [AGRICULTURE_DATASET_URL]
    return answer, None, sources

def _handle_analyze_correlation(params):
    """Handle correlation analysis queries"""
    states = params.get('states', [])
    crops = params.get('crops', [])
    year_start = params.get('year_start', 2010)
    year_end = params.get('year_end', 2020)
    
    if not states:
        return "Please specify a state for correlation analysis.", None, []
    
    state = states[0]
    crop = crops[0] if crops else "Rice"  # Default to rice
    
    # Fetch both agriculture and climate data
    agri_df = fetch_agriculture_data(state=state, crop=crop, year_start=year_start, year_end=year_end)
    climate_df = fetch_climate_data(state=state, year_start=year_start, year_end=year_end)
    
    agri_df = _ensure_dataframe(agri_df)
    climate_df = _ensure_dataframe(climate_df)
    
    if agri_df.empty or climate_df.empty:
        return f"Insufficient data for correlation analysis between {crop} production and rainfall in {state}.", None, [AGRICULTURE_DATASET_URL, CLIMATE_DATASET_URL]
    
    # Merge dataframes on year
    merged_df = pd.merge(agri_df, climate_df, on='Year', how='inner')
    
    if merged_df.empty:
        return f"Could not correlate {crop} production and rainfall data for {state}.", None, [AGRICULTURE_DATASET_URL, CLIMATE_DATASET_URL]
    
    # Calculate correlation using a simple approach
    try:
        # Convert to numpy arrays to avoid type issues
        production_values = np.array(merged_df['Production'].values, dtype=float)
        rainfall_values = np.array(merged_df['Rainfall'].values, dtype=float)
        
        # Calculate correlation manually to avoid type issues
        # Center the data
        prod_mean = np.mean(production_values)
        rain_mean = np.mean(rainfall_values)
        prod_centered = production_values - prod_mean
        rain_centered = rainfall_values - rain_mean
        
        # Calculate correlation coefficient
        numerator = np.sum(prod_centered * rain_centered)
        denominator = np.sqrt(np.sum(prod_centered**2) * np.sum(rain_centered**2))
        
        if denominator != 0:
            correlation = numerator / denominator
        else:
            correlation = 0.0
            
        correlation = float(correlation)
    except Exception:
        correlation = 0.0
    
    answer = f"The correlation between {crop} production and rainfall in {state} from {year_start}-{year_end} is {correlation:.2f}."
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(merged_df['Rainfall'], merged_df['Production'], alpha=0.7)
    ax.set_xlabel('Rainfall (mm)')
    ax.set_ylabel('Production')
    ax.set_title(f'{crop} Production vs Rainfall in {state}')
    plt.tight_layout()
    
    sources = [AGRICULTURE_DATASET_URL, CLIMATE_DATASET_URL]
    return answer, fig, sources