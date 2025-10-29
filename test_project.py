"""
Test script for Project Samarth
This script tests the core functionality of the Q&A system
"""

from core.query_parser import parse_query
from core.data_integrator import generate_answer

def test_query_parsing():
    """Test the query parsing functionality"""
    print("Testing query parsing...")
    
    # Test case 1: Compare rainfall query
    query1 = "Compare average annual rainfall in Tamil Nadu and Maharashtra over the last 5 years."
    intent1, params1 = parse_query(query1)
    print(f"Query: {query1}")
    print(f"Intent: {intent1}")
    print(f"Params: {params1}")
    print()
    
    # Test case 2: Top crops query
    query2 = "What are the top 3 crops in Karnataka by production volume last year?"
    intent2, params2 = parse_query(query2)
    print(f"Query: {query2}")
    print(f"Intent: {intent2}")
    print(f"Params: {params2}")
    print()
    
    # Test case 3: Wheat production query
    query3 = "Which district in Uttar Pradesh produced the most wheat in 2020?"
    intent3, params3 = parse_query(query3)
    print(f"Query: {query3}")
    print(f"Intent: {intent3}")
    print(f"Params: {params3}")
    print()
    
    # Test case 4: Crop trend query
    query4 = "Analyze rice production trends in Bihar over the last decade and correlate with rainfall."
    intent4, params4 = parse_query(query4)
    print(f"Query: {query4}")
    print(f"Intent: {intent4}")
    print(f"Params: {params4}")
    print()

def test_answer_generation():
    """Test the answer generation functionality"""
    print("Testing answer generation...")
    
    # Test case 1: Compare rainfall
    intent1 = "compare_rainfall"
    params1 = {
        "states": ["Tamil Nadu", "Maharashtra"],
        "year_start": 2015,
        "year_end": 2020
    }
    answer1, chart1, sources1 = generate_answer(intent1, params1)
    print(f"Intent: {intent1}")
    print(f"Params: {params1}")
    print(f"Answer: {answer1}")
    print(f"Sources: {sources1}")
    print()
    
    # Test case 2: Top crops
    intent2 = "top_crops"
    params2 = {
        "states": ["Karnataka"],
        "years": [2020]
    }
    answer2, chart2, sources2 = generate_answer(intent2, params2)
    print(f"Intent: {intent2}")
    print(f"Params: {params2}")
    print(f"Answer: {answer2}")
    print(f"Sources: {sources2}")
    print()
    
    # Test case 3: Crop trend analysis
    intent3 = "crop_trend"
    params3 = {
        "states": ["Bihar"],
        "crops": ["Rice"],
        "year_start": 2010,
        "year_end": 2020
    }
    answer3, chart3, sources3 = generate_answer(intent3, params3)
    print(f"Intent: {intent3}")
    print(f"Params: {params3}")
    print(f"Answer: {answer3}")
    print(f"Sources: {sources3}")
    print()

if __name__ == "__main__":
    test_query_parsing()
    test_answer_generation()
    print("All tests completed!")