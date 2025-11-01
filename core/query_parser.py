import re
from utils.constants import INDIAN_STATES, COMMON_CROPS
import datetime

def parse_query(query):
    """
    Parse user query to extract intent and parameters
    Returns intent and parameters dictionary
    """
    original_query = query
    query = query.lower()
    
    # Identify intent based on keywords
    intent = "unknown"
    params = {}
    
    # Extract state names with fuzzy matching for common misspellings
    states_found = []
    for state in INDIAN_STATES:
        state_lower = state.lower()
        # Direct match
        if state_lower in query:
            states_found.append(state)
        # Fuzzy matching for common misspellings
        elif _is_similar_state_name(state_lower, query):
            states_found.append(state)
    
    if states_found:
        params['states'] = states_found
    
    # Extract crop names
    crops_found = []
    for crop in COMMON_CROPS:
        if crop.lower() in query:
            crops_found.append(crop)
    if crops_found:
        params['crops'] = crops_found
    
    # Extract years (simple pattern matching for 4-digit years)
    # Try different patterns to catch various ways years might be expressed
    # First try to find 4-digit years directly
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', original_query)  # Capture full 4-digit years
    print(f"DEBUG: Found years with basic pattern: {years}")
    
    # If we didn't find years with the basic pattern, try a more flexible approach
    if not years:
        # Look for patterns like "2018-2020", "from 2018 to 2020", "between 2018 and 2020"
        year_range_patterns = [
            r'(?:from\s+)?(\d{4})\s*(?:to|-)\s*(\d{4})',
            r'between\s+(\d{4})\s+and\s+(\d{4})',
            r'(\d{4})\s*(?:to|-)\s*(\d{4})',
        ]
        
        for pattern in year_range_patterns:
            matches = re.findall(pattern, original_query, re.IGNORECASE)
            if matches:
                # Extract both years from the first match
                if len(matches[0]) >= 2:
                    years = [matches[0][0], matches[0][1]]
                    print(f"DEBUG: Found years with range pattern: {years}")
                    break
    
    # If still no years found, try to find individual years
    if not years:
        # Look for individual 4-digit years
        individual_years = re.findall(r'\b(19\d{2}|20\d{2})\b', original_query)  # Capture full 4-digit years
        if individual_years:
            years = individual_years
            print(f"DEBUG: Found individual years: {years}")
    
    # If still no years found, check for relative time references
    if not years:
        # Look for patterns like "last 3 years", "past 5 years", "recent years", "last 3 available years", etc.
        # Handle "last X available years" or "last X years"
        last_years_match = re.search(r'(?:last|past|previous)\s+(\d+)\s+(?:available\s+)?(?:year|years)', original_query, re.IGNORECASE)
        if last_years_match:
            num_years = int(last_years_match.group(1))
            # Calculate the year range based on current year
            current_year = datetime.datetime.now().year
            year_start = current_year - num_years + 1  # +1 because we want inclusive range
            year_end = current_year
            
            years = list(range(year_start, year_end + 1))
            params['years'] = years
            params['year_start'] = year_start
            params['year_end'] = year_end
            print(f"DEBUG: Found relative time reference: last {num_years} years ({year_start}-{year_end})")
        
        # Handle "recent years" (default to last 3 years)
        elif re.search(r'recent\s+(?:available\s+)?(?:year|years)', original_query, re.IGNORECASE):
            num_years = 3  # Default to 3 years for "recent"
            current_year = datetime.datetime.now().year
            year_start = current_year - num_years + 1
            year_end = current_year
            
            years = list(range(year_start, year_end + 1))
            params['years'] = years
            params['year_start'] = year_start
            params['year_end'] = year_end
            print(f"DEBUG: Found relative time reference: recent years ({year_start}-{year_end})")

    if years:
        # Convert to integers if they aren't already
        if isinstance(years[0], str):
            years = [int(y) for y in years]
        params['years'] = sorted(years)
        if len(years) >= 2:
            params['year_start'] = min(years)
            params['year_end'] = max(years)
        elif len(years) == 1:
            # If only one year is specified, use it as both start and end
            params['year_start'] = years[0]
            params['year_end'] = years[0]
    
    # Debug: Print the parsed parameters
    print(f"DEBUG: Parsed params: {params}")
    
    # Determine intent - ORDER MATTERS HERE!
    # Check for specific intents first
    if "analyze" in query and ("correlate" in query or "correlation" in query):
        intent = "analyze_correlation"
    elif "compare" in query and "rainfall" in query:
        intent = "compare_rainfall"
    elif "trend" in query and ("crop" in query or "production" in query):
        intent = "crop_trend"
    elif "most" in query and "wheat" in query:
        intent = "highest_wheat_production"
    elif ("top" in query and "crop" in query and ("type" in query or "specific" in query)) or \
         ("list" in query and "top" in query and "crop" in query):
        # New intent for specific crop type queries
        intent = "top_crops_by_type"
    elif "top" in query and "crop" in query:
        intent = "top_crops"
    elif ("climate" in query or "weather" in query or "rainfall" in query or "pattern" in query) and states_found:
        intent = "climate_info"
    elif "production" in query and crops_found and states_found:
        intent = "crop_production"
    elif states_found and ("crop" in query or "agricultur" in query):
        intent = "crop_production"
    elif states_found and ("rain" in query or "climate" in query or "weather" in query):
        intent = "climate_info"
    else:
        # Default intent for general queries
        intent = "general_query"
    
    return intent, params

def _is_similar_state_name(state_name, query):
    """
    Check if query contains a similar state name (handles common misspellings)
    """
    # Common misspellings mapping
    misspellings = {
        'maharashtra': ['maharashta', 'maharashtr', 'maharastra'],
        'tamil nadu': ['tamilnadu', 'tamilnad'],
        'uttar pradesh': ['uttarpradesh', 'up'],
        'madhya pradesh': ['madhyapradesh'],
        'west bengal': ['westbengal'],
        'andhra pradesh': ['andhrapradesh'],
        'arunachal pradesh': ['arunachalpradesh'],
        'himachal pradesh': ['himachalpradesh'],
        'jharkhand': ['jharkhand'],
        'chhattisgarh': ['chhattisgarh'],
        'uttarakhand': ['uttrakhand'],
        'karnataka': ['karnataka'],
        'kerala': ['kerala'],
        'odisha': ['odisha', 'orisaa', 'orissa'],
        'punjab': ['punjab'],
        'rajasthan': ['rajasthan'],
        'sikkim': ['sikkim'],
        'telangana': ['telangana'],
        'tripura': ['tripura'],
        'manipur': ['manipur'],
        'meghalaya': ['meghalaya'],
        'mizoram': ['mizoram'],
        'nagaland': ['nagaland'],
        'goa': ['goa'],
        'gujarat': ['gujarat'],
        'haryana': ['haryana'],
        'assam': ['assam'],
        'bihar': ['bihar'],
        'delhi': ['delhi', 'nct of delhi'],
    }
    
    # Check for direct substring matches
    if state_name in query:
        return True
    
    # Check for common misspellings
    state_key = state_name.replace(' ', '')
    if state_key in misspellings:
        for misspelling in misspellings[state_key]:
            if misspelling in query:
                return True
    
    # Also check with spaces removed
    state_no_spaces = state_name.replace(' ', '')
    query_no_spaces = query.replace(' ', '')
    if state_no_spaces in query_no_spaces:
        return True
        
    return False