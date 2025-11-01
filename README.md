# Project Samarth - Intelligent Q&A on Agri & Climate Data

Project Samarth is an intelligent question-answering system for India's agriculture and climate data. It connects to live datasets from data.gov.in, processes natural language queries, integrates multiple datasets, generates concise answers with citations, and visualizes data through charts.

## Features

- Natural language understanding of agricultural and climatic questions
- Live data retrieval from government APIs (data.gov.in)
- Cross-dataset correlation (e.g., crop yield vs rainfall)
- Answer summarization with source attribution
- Dynamic chart rendering for trends and comparisons
- Support for all Indian states and union territories

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd project-samarth
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Get an API key from [data.gov.in](https://data.gov.in/):
   - Register on the data.gov.in website
   - Generate an API key from your account dashboard

4. Configure the application:
   - Open `config.py`
   - Replace `YOUR_DATA_GOV_API_KEY_HERE` with your actual API key
   - Replace the resource IDs with actual resource IDs from data.gov.in:
     - `RAINFALL_DATA_RESOURCE_ID`
     - `CROP_PRODUCTION_RESOURCE_ID`

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. Open your browser and go to the URL provided by Streamlit (usually http://localhost:8501)

3. Ask questions about agriculture and climate data, for example:
   - "What is the rainfall in Maharashtra?"
   - "Compare rainfall in Tamil Nadu and Kerala"
   - "What are the top crops in Punjab?"
   - "Show wheat production trend in Haryana"

## Configuration

### Using Real Data from data.gov.in

To use real data from data.gov.in:
1. Set `USE_MOCK_DATA = False` in `config.py`
2. Ensure you have a valid API key
3. Use correct resource IDs for the datasets

### Using Mock Data (for demonstration)

To use mock data instead of real API calls:
1. Set `USE_MOCK_DATA = True` in `config.py`

## Supported States and Union Territories

The application supports all Indian states and union territories:
- Andhra Pradesh
- Arunachal Pradesh
- Assam
- Bihar
- Chhattisgarh
- Goa
- Gujarat
- Haryana
- Himachal Pradesh
- Jharkhand
- Karnataka
- Kerala
- Madhya Pradesh
- Maharashtra
- Manipur
- Meghalaya
- Mizoram
- Nagaland
- Odisha
- Punjab
- Rajasthan
- Sikkim
- Tamil Nadu
- Telangana
- Tripura
- Uttar Pradesh
- Uttarakhand
- West Bengal
- Andaman and Nicobar Islands
- Chandigarh
- Dadra and Nagar Haveli and Daman and Diu
- Lakshadweep
- Delhi
- Puducherry
- Ladakh
- Jammu and Kashmir

## Supported Crops

The application supports queries about common crops including:
- Rice
- Wheat
- Maize
- Sugarcane
- Cotton
- Jowar
- Bajra
- Ragi
- Tur
- Urad
- Moong
- Gram
- Groundnut
- Sunflower
- Soybean
- Potatoes
- Jute
- Barley
- Mustard
- Peas

## Project Structure

- `app.py`: Main Streamlit application frontend
- `core/`:
  - `query_parser.py`: Parses natural language questions into structured queries
  - `data_integrator.py`: Combines and analyzes data from multiple sources
- `data_connectors/`:
  - `agriculture_data.py`: Handles crop production data from data.gov.in
  - `climate_data.py`: Manages rainfall and climate datasets
- `utils/`:
  - `constants.py`: Stores API endpoints and mappings
  - `helpers.py`: Shared utility functions across modules
- `config.py`: Configuration file for API keys and settings

## API Configuration

For detailed instructions on configuring the API integration, see:
- [API_CONFIGURATION_GUIDE.md](API_CONFIGURATION_GUIDE.md)
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

## Testing and Debugging

Several scripts are provided to help with testing and debugging:
- `test_api_response.py`: Test actual API responses
- `validate_api_format.py`: Validate API response format and data processing
- `find_resource_ids.py`: Help identify correct resource IDs
- `debug_correlation.py`: Debug correlation analysis functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.