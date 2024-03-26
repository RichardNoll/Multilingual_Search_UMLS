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
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

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
        Searches for and returns the first unique identifier (UI) for a given search string.

        Parameters:
            string (str): The search string used to query the UMLS API.

        Returns:
            str: The first unique identifier (UI) found, or None if no results are found.
        """
        content_endpoint = f"/rest/search/{self.version}"
        page = 0
        while True:
            page += 1
            params = {'string': string, 'pageNumber': page}
            results = self.make_request(content_endpoint, params)['result']['results']
            if results:
                return results[0]['ui']
            if page == 1:
                print('No results found.\n')
                return None

    def get_atoms(self, identifier, source=None):
        """
        Retrieves and prints details for atoms associated with a given identifier, optionally filtering by source.

        Parameters:
            identifier (str): The unique identifier for which to retrieve atom details.
            source (str, optional): The source by which to filter the atoms. Defaults to None.
        """
        content_endpoint = f"/rest/content/{self.version}/CUI/{identifier}/atoms"
        params = {'ttys': 'PT'}
        if source:
            params['sabs'] = source
        else:
            params['sabs'] = 'HPO,SNOMEDCT_US'
        
        atoms = self.make_request(content_endpoint, params)['result']
        for atom in atoms:
            print(f"Name: {atom['name']}")
            print(f"Code: {self.get_last_part_of_url(atom['code'])}")
            print(f"Source Vocabulary: {atom['rootSource']}\n")

if __name__ == "__main__":
    apikey = "" 
    tool = HealthTermFinder(apikey)
    identifier = input("Enter identifier: ")
    first_ui = tool.get_first_ui(identifier)
    if first_ui:
        tool.get_atoms(first_ui)
