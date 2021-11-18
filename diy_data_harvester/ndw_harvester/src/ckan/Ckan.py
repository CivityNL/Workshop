import requests

class Ckan:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
    
    def upsert_situations(self, resource_id, situations):
        # Don't know how to this properly in Python
        payload = '{"records": ['

        for i in range(0, len(situations)):
            payload += situations[i].to_json()
            if i < len(situations) - 1:
                payload += ","
        
        payload += '], "force": true, "method": "upsert", "resource_id": "' + resource_id + '"}'

        # urllib wants to POST bytes, but payload is a string. 
        headers = {
            'Authorization': '48b1a4bc-2e39-4e64-b95b-4b6d3eb69ecc',
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", 
            self.url + '/api/3/action/datastore_upsert', 
            headers=headers, 
            data=payload
        )

        # TODO: in case of an error, CKAN will return te following JSON:
        # {"help": "https://tst-ckan-dataplatform-nl.dataplatform.nl/api/3/action/help_show?name=datastore_upsert", "success": false, "error": {"__type": "Validation Error", "key": ["fields \"situation_id\" are missing but needed as key"]}}
        # Parse this message and throw an error if needed