"""
Test script for correlation analysis in Project Samarth
"""

from core.data_integrator import generate_answer

def test_correlation_analysis():
    """Test the correlation analysis functionality"""
    print("Testing correlation analysis...")
    
    # Test case: Analyze correlation between rice production and rainfall in Bihar
    intent = "analyze_correlation"
    params = {
        "states": ["Bihar"],
        "crops": ["Rice"],
        "year_start": 2010,
        "year_end": 2020
    }
    answer, chart, sources = generate_answer(intent, params)
    print(f"Intent: {intent}")
    print(f"Params: {params}")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
    print()

if __name__ == "__main__":
    test_correlation_analysis()
    print("Correlation analysis test completed!")