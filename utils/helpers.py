import re

def extract_years_from_query(query):
    """
    Extract years from a query string
    Returns a list of years found in the query
    """
    # Pattern to match 4-digit years (19xx or 20xx)
    years = re.findall(r'\b(19|20)\d{2}\b', query)
    return [int(year) for year in years]

def normalize_state_name(state):
    """
    Normalize state names to standard format
    """
    # This would contain logic to standardize state names
    # For now, just return the input
    return state.strip().title()

def normalize_crop_name(crop):
    """
    Normalize crop names to standard format
    """
    # This would contain logic to standardize crop names
    # For now, just return the input
    return crop.strip().title()