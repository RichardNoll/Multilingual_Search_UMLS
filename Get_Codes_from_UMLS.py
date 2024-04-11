import requests
from urllib.parse import urlparse

class HealthTermFinder:
    """
    A tool for discovering standardized healthcare terminology across multiple languages using the UMLS API.

    Attributes:
        apikey (str): The API key required to access the UMLS API.
        version (str): The version of the UMLS API to use. Defaults to 'current'.
        session (requests.Session): A session object for making HTTP requests.

    Methods:
        make_request(endpoint, params): Makes an HTTP GET request to a specified UMLS API endpoint.
        get_last_part_of_url(url): Extracts the last part of a URL's path.
        get_first_ui(string): Searches for the first unique identifier (UI) based on a given search string.
        get_atoms(identifier, source): Retrieves atom details for a given identifier, optionally filtering by source.
    """

    def __init__(self, apikey, version='current'):
        """
        Initializes the HealthTermFinder with the specified API key and version.

        Parameters:
            apikey (str): The API key for accessing the UMLS API.
            version (str): The version of the UMLS API to use. Defaults to 'current'.
        """
        self.session = requests.Session()
        self.apikey = apikey
        self.version = version
        self.base_uri = 'https://uts-ws.nlm.nih.gov'

    def make_request(self, endpoint, params={}):
        """
        Makes an HTTP GET request to a specified endpoint of the UMLS API.

        Parameters:
            endpoint (str): The API endpoint to which the request is made.
            params (dict): A dictionary of parameters to be passed with the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            HTTPError: If the request fails.
        """
        url = f"{self.base_uri}{endpoint}"
        
        params['apiKey'] = self.apikey
        try:
           response = self.session.get(url, params=params)
           
           
           response.raise_for_status()
           return response.json()
        except requests.HTTPError as e:
           if e.response.status_code == 404:
             return None
           else:
               print(f"HTTP Error occurred: {e}")
           return None

    def get_last_part_of_url(self, url):
        """
        Extracts and returns the last part of a URL's path.

        Parameters:
            url (str): The URL from which to extract the last path segment.

        Returns:
            str: The last part of the URL's path.
        """
        return urlparse(url).path.split('/')[-1]

    def get_first_ui(self, string):
        """
        Searches for and returns unique identifiers (UI) for a given search string.
        It searches without source specification and then with 'MTH,MSH' sources.
    
        Parameters:
            string (str): The search string used to query the UMLS API.
    
        Returns:
            list: Unique identifiers (UI) found, up to 10 for each search type.
        """
        content_endpoint = f"/rest/search/{self.version}"
        relevant_ui = []
    
        # Search without specific source
        params = {
            'string': string,
            'pageNumber': 1,
            'inputType': 'atom',
            'sabs': '',
            'partialSearch': 'true',
            'searchType': 'words'
        }
        response = self.make_request(content_endpoint, params)
        results = response.get('result', {}).get('results', [])
        relevant_ui.extend([result['ui'] for result in results[:10]])
    
        # Search with specific sources if the first search had results
        if results:
            params['sabs'] = 'MTH,MSH'
            response = self.make_request(content_endpoint, params)
            results = response.get('result', {}).get('results', [])
            relevant_ui.extend([result['ui'] for result in results[:10]])
    
        return relevant_ui
    

    def get_atoms(self, first_ui):
        """
        Retrieves and prints details for atoms associated with a given identifier, optionally filtering by source.

        Parameters:
            identifier (str): The unique identifiers for which to retrieve atom details.
            source (str, optional): The source by which to filter the atoms. Defaults to None.
        """
        
        for i in first_ui:
        
            content_endpoint = f"/rest/content/{self.version}/CUI/{i}/atoms"
            params = {'ttys': 'PT', 'sabs': 'HPO,SNOMEDCT_US'}
            atoms = self.make_request(content_endpoint, params)
            if atoms:
                for atom in atoms['result']:
                    print(f"Name: {atom['name']}")
                    print(f"Code: {self.get_last_part_of_url(atom['code'])}")
                    print(f"Source Vocabulary: {atom['rootSource']}\n")
                break
     

if __name__ == "__main__":
    apikey = "" 
    tool = HealthTermFinder(apikey)
    identifier = input("Enter identifier: ")
    first_ui = tool.get_first_ui(identifier)
    if first_ui:
        tool.get_atoms(first_ui)
 
