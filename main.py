#!/Users/artem/PycharmProjects/anki_export/venv/bin/python3
import json
import urllib.request
from query_template import params
from argparse import ArgumentParser

parser = ArgumentParser('Anki mamaner')
parser.add_argument('-i', '--info', help='information', action = 'store_true')
parser.add_argument('-c', '--create', help='create cards', action = 'store_true')
#parser.add_argument('-s', '--start', help='start account number in our account list(file)', type = int, default = 0)
#parser.add_argument('-e', '--end', help='end account number in our account list(file)', type = int, default = 1000)
args = parser.parse_args()


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    # print(requestJson)
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    # print(response)
    return response['result']

card_example_dict = None

def create_card(deckname, front, back):
    params['deckName'] = deckname
    params['fields']['Front'] = front
    params['fields']['Back'] = back
    result = invoke('addNote', note = params)
    print('got result: {}'.format(result))

if __name__ == "__main__":
    
    create_card('test1', 'autoqueston', 'autoposted answer')
    if args.info:
        result = invoke('findCards', query = 'deck:test1')
        print('got result: {}'.format(result))
        result = invoke('cardsInfo', cards = result)
        print('got result: {}'.format(result))
    if args.create:
        print(params)
        result = invoke('addNote', note = params)
        # print('got result: {}'.format(result))

    # invoke('createDeck', deck='test1')
    # result = invoke('deckNames')
    # print('got list of decks: {}'.format(result))
