import re
from utils.constants import INDIAN_STATES, COMMON_CROPS

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
    years = re.findall(r'\b(19|20)\d{2}\b', query)
    if years:
        years = [int(y) for y in years]
        params['years'] = sorted(years)
        if len(years) >= 2:
            params['year_start'] = min(years)
            params['year_end'] = max(years)
    
    # Determine intent
    if "compare" in query and "rainfall" in query:
        intent = "compare_rainfall"
    elif "trend" in query and ("crop" in query or "production" in query):
        intent = "crop_trend"
    elif "most" in query and "wheat" in query:
        intent = "highest_wheat_production"
    elif "top" in query and "crop" in query:
        intent = "top_crops"
    elif "analyze" in query and "correlate" in query:
        intent = "analyze_correlation"
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
        'uttrakhand': ['uttrakhand'],
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