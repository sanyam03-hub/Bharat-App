"""
Demo example for Project Samarth
This script demonstrates a complete end-to-end example of the Q&A system
"""

from core.query_parser import parse_query
from core.data_integrator import generate_answer

def demo_complete_example():
    """Demonstrate a complete end-to-end example"""
    print("=== Project Samarth Demo ===")
    print()
    
    # Sample query
    query = "Compare average annual rainfall in Tamil Nadu and Maharashtra over the last 5 years."
    print(f"User Query: {query}")
    print()
    
    # Parse the query
    intent, params = parse_query(query)
    print(f"Parsed Intent: {intent}")
    print(f"Extracted Parameters: {params}")
    print()
    
    # Generate answer
    answer, chart, sources = generate_answer(intent, params)
    print("System Response:")
    print(f"Answer: {answer}")
    print()
    
    # Show sources
    print("Data Sources:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source}")
    print()
    
    # Expected format
    print("Expected Output Format:")
    print("Answer Summary:")
    print("Tamil Nadu received an average of 952 mm rainfall vs Maharashtra's 1084 mm between 2015-2020.")
    print()
    print("Supporting Data:")
    print("- Top Crops (Tamil Nadu): Rice, Maize, Sugarcane")
    print("- Top Crops (Maharashtra): Rice, Wheat, Soybean")
    print()
    print("Sources:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source}")

if __name__ == "__main__":
    demo_complete_example()