
import json
import urllib.request
from argparse import ArgumentParser

# Constants
ANKI_CONNECT_URL = 'http://localhost:8765'

def request(action: str, **params) -> dict:
    return {'action': action, 'params': params, 'version': 6}

def invoke(action: str, **params) -> dict:
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(ANKI_CONNECT_URL, request_json)))
    
    if 'error' in response and response['error'] is not None:
        raise Exception(response['error'])
    
    return response['result']

def create_card(deckname: str, front: str, back: str) -> None:
    params = {}  # Add necessary parameters for AnkiConnect here
    params['deckName'] = deckname
    params['fields'] = {'Front': front, 'Back': back}
    result = invoke('addNote', note=params)
    print(f'Card creation result: {result}')

def main():
    parser = ArgumentParser('Anki manager')
    parser.add_argument('-i', '--info', help='information', action='store_true')
    parser.add_argument('-c', '--create', help='create cards', action='store_true')
    args = parser.parse_args()

    # TODO: Implement further logic based on args (not shown in provided code snippet)

if __name__ == "__main__":
    main()
