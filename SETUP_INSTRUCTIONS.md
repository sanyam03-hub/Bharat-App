# Setup Instructions for Project Samarth

## Getting API Access from data.gov.in

1. Visit [data.gov.in](https://data.gov.in/)
2. Register for a new account or log in if you already have one
3. Navigate to your profile and generate an API key
4. Copy the API key for use in the configuration

## Finding Resource IDs

1. On data.gov.in, search for datasets related to:
   - Agricultural production statistics
   - Rainfall and climate data
2. Select the datasets you want to use
3. Note the resource IDs from the dataset URLs

## Configuring the Application

1. Open `config.py` in a text editor
2. Replace `YOUR_DATA_GOV_API_KEY_HERE` with your actual API key
3. Replace the placeholder resource IDs with actual resource IDs:
   - `RAINFALL_DATA_RESOURCE_ID` - Resource ID for rainfall data
   - `CROP_PRODUCTION_RESOURCE_ID` - Resource ID for crop production data

## Example Configuration

```python
# API Keys
DATA_GOV_API_KEY = "your_actual_api_key_here"

# API Endpoints
RAINFALL_DATA_RESOURCE_ID = "actual_rainfall_resource_id_here"
CROP_PRODUCTION_RESOURCE_ID = "actual_crop_production_resource_id_here"
```

## Testing the Setup

1. Set `USE_MOCK_DATA = False` in `config.py` to use real data
2. Run the test script:
   ```
   python test_data_fetch.py
   ```
3. If successful, you should see real data from data.gov.in
4. If you get errors, check your API key and resource IDs

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**: Check that your API key is correct and active
2. **404 Not Found Error**: Verify that your resource IDs are correct
3. **Connection Errors**: Ensure you have internet access

### Using Mock Data for Testing

If you want to test the application without API access:
1. Set `USE_MOCK_DATA = True` in `config.py`
2. The application will use generated mock data instead of real API calls

## Running the Application

Once configured, run the application with:
```
streamlit run app.py
```

Then open your browser to the URL provided by Streamlit (usually http://localhost:8501).