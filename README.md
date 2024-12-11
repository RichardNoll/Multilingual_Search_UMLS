# HealthTermFinder README

## Overview
The HealthTermFinder is a Python tool designed to facilitate the discovery of standardized healthcare terminology across multiple languages using the UMLS API. It provides functionality to search for unique identifiers (UI) and retrieve detailed atom information for these identifiers from UMLS.

## Features
- **Search for Unique Identifiers (UI):** Allows users to search for the first three UIs based on a given search string.
- **Retrieve Atom Details:** Retrieves detailed information for atoms associated with a given identifier, with an option to filter by source vocabulary.

## Requirements
- Python 3.x
- `requests` library

To install the required `requests` library, run:
```
pip install requests
```

## Configuration
Before using the HealthTermFinder, obtain an API key from the UMLS API website. Replace the `apikey` variable value in the script with your actual UMLS API key.

## Usage
1. **Initialization:** Instantiate the `HealthTermFinder` class with your UMLS API key.
   ```python
   apikey = "your_api_key_here"
   tool = HealthTermFinder(apikey)
   ```

2. **Search for UIs:** Use the `get_first_ui` method with a search string to find unique identifiers.
   ```python
   search_string = "diabetes"
   first_ui = tool.get_first_ui(search_string)
   print(first_ui)
   ```

3. **Retrieve Atom Details:** Once you have UIs, use the `get_atoms` method to fetch detailed information.
   ```python
   if first_ui:
       tool.get_atoms(first_ui)
   ```

## Methods
- `make_request(endpoint, params)`: Internal method to make HTTP GET requests to the UMLS API.
- `get_last_part_of_url(url)`: Utility method to extract the last part of a URL's path.
- `get_first_ui(string)`: Public method to search for the first three UIs based on a search string.
- `get_atoms(identifier, source=None)`: Public method to retrieve atom details for a given identifier, with optional source filtering.

## Error Handling
- The tool will print HTTP error messages if there are issues with the API requests.
- It will return `None` or an empty list if no results are found or if an error occurs.

## Notes
- Ensure that you comply with the terms of use for the UMLS API.
- The example API key in the script is a placeholder and should be replaced with a valid key.

## Conclusion
HealthTermFinder is a powerful tool for medical researchers and healthcare professionals who need to access standardized medical terminology across different languages, leveraging the comprehensive resources of the UMLS API.

## Example 
**Enter identifier:** husten

**Output:**

Name: Cough
Code: HP:0012735
Source Vocabulary: HPO

Name: Coughing
Code: 263731006
Source Vocabulary: SNOMEDCT_US

Name: Cough
Code: 49727002
Source Vocabulary: SNOMEDCT_US
