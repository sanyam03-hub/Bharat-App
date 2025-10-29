# Project Samarth

An intelligent Q&A system for India's agriculture and climate data using live datasets from data.gov.in.

## Overview

Project Samarth is a question-answering system that connects programmatically to live public datasets from data.gov.in to answer natural language questions about India's agriculture and climate data. The system can combine multiple datasets, return concise answers with dataset citations, and display charts when relevant.

## Features

- Natural language processing for understanding user queries
- Live data fetching from data.gov.in APIs
- Data integration and analysis capabilities
- Interactive web interface built with Streamlit
- Support for complex queries involving multiple datasets
- Chart generation for data visualization
- Dataset citation with clickable URLs

## Setup Instructions

1. Clone or download the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Project Structure

```
project_samarth/
│
├── app.py                      # Main Streamlit application
├── data_connectors/
│   ├── agriculture_data.py     # Fetch and process crop data
│   ├── climate_data.py         # Fetch and process rainfall data
│
├── core/
│   ├── query_parser.py         # NLP and keyword mapping for user questions
│   ├── data_integrator.py      # Combines and analyzes datasets
│
├── utils/
│   ├── helpers.py              # Reusable helper functions
│   ├── constants.py            # API URLs, mappings, etc.
│
└── requirements.txt            # Necessary dependencies
```

## Sample Queries

Try these sample questions in the application:

1. "Compare average annual rainfall in Tamil Nadu and Maharashtra over the last 5 years."
2. "Which district in Uttar Pradesh produced the most wheat in 2020?"
3. "Analyze rice production trends in Bihar over the last decade and correlate with rainfall."
4. "What are the top 3 crops in Karnataka by production volume last year?"

Note: The application uses mock data for demonstration purposes. In a production environment, it would connect to live datasets from data.gov.in.

## Dependencies

- streamlit
- pandas
- requests
- matplotlib
- numpy

## How It Works

1. **Data Discovery and Access**: Connects to official data.gov.in APIs for rainfall and crop production data
2. **Question Understanding**: Uses lightweight NLP to parse user queries and extract intent
3. **Data Integration**: Combines datasets based on query requirements
4. **Answer Generation**: Produces concise text answers, charts, and data source citations

## Example Output Format

```
Answer Summary:
Tamil Nadu received an average of 912 mm rainfall vs Maharashtra's 1024 mm between 2015-2020.

Supporting Data:
- Top Crops (Tamil Nadu): Rice, Maize, Sugarcane
- Top Crops (Maharashtra): Cotton, Jowar, Soybean

Sources:
1. https://data.gov.in/node/135611 (IMD Rainfall Dataset)
2. https://data.gov.in/node/135712 (Crop Production Dataset)
```