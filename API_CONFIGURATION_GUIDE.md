# API Configuration Guide

This guide explains how to properly configure the API integration with data.gov.in to ensure correct JSON format handling.

## 1. Getting API Access

1. Visit [data.gov.in](https://data.gov.in/)
2. Register for a new account or log in if you already have one
3. Navigate to your profile and generate an API key
4. Copy the API key for use in the configuration

## 2. Finding Resource IDs

To find the correct resource IDs:

1. On data.gov.in, search for datasets related to:
   - Agricultural production statistics
   - Rainfall and climate data
2. Select the datasets you want to use
3. Look at the dataset URL - the resource ID is part of the URL path
4. Example URL format: `https://data.gov.in/catalogue-number/resource/resource-id`
5. The resource ID is the last part of the URL

## 3. Understanding API Response Format

The data.gov.in API typically returns JSON in this format:

```json
{
  "title": "Dataset Title",
  "description": "Dataset Description",
  "keywords": "keyword1,keyword2",
  "license": "License Information",
  "records": [
    {
      "field1": "value1",
      "field2": "value2",
      "field3": "value3"
    },
    {
      "field1": "value4",
      "field2": "value5",
      "field3": "value6"
    }
  ],
  "total": 1000,
  "count": 10
}
```

## 4. Configuring the Application

1. Open `config.py` in a text editor
2. Replace `YOUR_DATA_GOV_API_KEY_HERE` with your actual API key
3. Replace the placeholder resource IDs with actual resource IDs:
   - `RAINFALL_DATA_RESOURCE_ID` - Resource ID for rainfall data
   - `CROP_PRODUCTION_RESOURCE_ID` - Resource ID for crop production data

## 5. Testing API Responses

Use the `test_api_response.py` script to examine the actual API response format:

1. Replace the placeholder resource IDs in the script with actual resource IDs
2. Update the config.py file with your actual API key
3. Run the script to see the actual API response format

## 6. Common Column Name Variations

The improved data connectors now handle common variations in column names:

### Climate Data Columns
- State: `state`, `state_name`, `State`, `State_Name`
- Year: `year`, `Year`, `crop_year`, `Year_Name`
- Rainfall: `rainfall`, `annual_rainfall`, `Rainfall`, `Annual_Rainfall`, `precipitation`

### Agriculture Data Columns
- State: `state`, `state_name`, `State`, `State_Name`
- District: `district`, `district_name`, `District`, `District_Name`
- Year: `year`, `Year`, `crop_year`, `Year_Name`
- Crop: `crop`, `Crop`, `crop_name`, `Crop_Name`
- Production: `production`, `Production`, `crop_production`, `Production_Value`

## 7. Troubleshooting

### Common Issues

1. **403 Forbidden Error**: Check that your API key is correct and active
2. **404 Not Found Error**: Verify that your resource IDs are correct
3. **Connection Errors**: Ensure you have internet access
4. **Empty Records**: The filters might be too restrictive

### Debugging Steps

1. Use the `test_api_response.py` script to see the actual API response
2. Check that the response contains a `records` field with data
3. Verify that the column names in the records match what the application expects
4. Use the `validate_api_format.py` script to test the complete data processing pipeline

## 8. Example Configuration

```python
# API Keys
DATA_GOV_API_KEY = "your_actual_api_key_here"

# API Endpoints (replace with actual resource IDs)
RAINFALL_DATA_RESOURCE_ID = "actual_rainfall_resource_id_here"
CROP_PRODUCTION_RESOURCE_ID = "actual_crop_production_resource_id_here"

# API Settings
API_BASE_URL = "https://api.data.gov.in/resource"
API_FORMAT = "json"
API_LIMIT = 1000

# Application Settings
USE_MOCK_DATA = False  # Set to True to use mock data instead of real API calls
```

## 9. Running with Real Data

Once configured, set `USE_MOCK_DATA = False` in `config.py` and run the application:

```
streamlit run app.py
```

Then test queries like:
- "Analyze correlation between rainfall and rice production in West Bengal"
- "What is the rainfall in Maharashtra?"
- "Compare rainfall in Tamil Nadu and Kerala"