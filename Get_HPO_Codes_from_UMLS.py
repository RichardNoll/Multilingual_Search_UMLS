import requests
from urllib.parse import urlparse

def get_last_part_of_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    last_part = path_parts[-1]
    return last_part

def get_first_ui(apikey, version, string):
    uri = "https://uts-ws.nlm.nih.gov"
    content_endpoint = "/rest/search/"+version
    full_url = uri + content_endpoint
    page = 0
    
    try:
        while True:
            page += 1
            query = {'string':string,'apiKey':apikey, 'pageNumber':page}
            r = requests.get(full_url,params=query)
            r.raise_for_status()
            outputs  = r.json()
        
            items = outputs['result']['results']
            
            if len(items) == 0:
                if page == 1:
                    print('No results found.'+'\n')
                    return None
                else:
                    break
            
            for result in items:
                ui = result['ui']
                return ui
                
    except Exception as except_error:
        print(except_error)
        return None

def get_atoms(apikey, version, identifier, source=None):
    uri = 'https://uts-ws.nlm.nih.gov'
    page = 0

    try:
        if source is None:
            content_endpoint = '/rest/content/'+str(version)+'/CUI/'+str(identifier)+'/atoms'
        else:
            content_endpoint = '/rest/content/'+str(version)+'/CUI/'+str(identifier)+'/atoms'
                
        query = {'apiKey':apikey, 'ttys': 'PT', 'sabs': 'HPO'}
        r = requests.get(uri+content_endpoint, params=query)
        r.encoding = 'utf-8'
                
        if r.status_code != 200:
            raise Exception('Search term ' + "'" + str(identifier) + "'" + ' not found')
                    
        items  = r.json()
                    
        for atom in items['result']:
            print('Name: ' + atom['name'])
            print('Code: ' + get_last_part_of_url(atom['code']))
            print('Source Vocabulary: ' + atom['rootSource'])
            print('\n')
            
    except Exception as except_error:
        print(except_error)

if __name__ == "__main__":
    apikey = ""  # Set your API key here
    version = "current"  # Set the version here
    identifier = input("Enter identifier: ")
    source = None


    first_ui = get_first_ui(apikey, version, identifier)
    if first_ui:
        get_atoms(apikey, version, first_ui, source)
