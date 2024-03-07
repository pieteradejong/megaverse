"""
Thursday March 7, 2024. Crossmint "Megaverse" challenge.
Solution by Pieter de Jong.

Phase 1: 
- fetch goal map
- traverse goal map; for each cell, if it's 'POLYANET', then `POST /api/polyanets` with row, col as payload
- verify result at `https://challenge.crossmint.io/map`


Overall notes as I go:
- solution assumes the given map is all `SPACE`; so we only need to POST to the API for the cells that are `POLYANET`.
else, we'd have to perform DELETE calls to ensure all non-POLYANET/etc cells are set to SPACE.
(This presumes the DELETE call does in fact set the value to SPACE.)


Phase 2:
- fetch current map
- traverse current map; for each cell, if not 'SPACE', then `POST /api/[object]` with row, col as payload
- verify result at `https://challenge.crossmint.io/map`
- approach: traversal + individual POSTs seems necessary, as the endpoints do not accept a list of cells to update;
and there is no quickly discernable "algorithmic" way to determine calls to make.
- cell values on my map seem to include:
{'LEFT_COMETH', 'RED_SOLOON', 'BLUE_SOLOON', 'DOWN_COMETH', 'SPACE', 'POLYANET', 'PURPLE_SOLOON', 'RIGHT_COMETH', 'UP_COMETH', 'WHITE_SOLOON'}

Room for improvement:
- reduce number of HTTP calls
- 

"""

import logging
import requests
import json
import sys
from enum import Enum

BASE_API_URL = 'https://challenge.crossmint.io/api'

class CelestialBody(Enum):
    SPACE = 'SPACE'
    POLYANET = 'POLYANET'
    SOLOON = 'SOLOON'
    COMET = 'COMET'

    # Phase 2
    RED_SOLOON = 'RED_SOLOON'
    BLUE_SOLOON = 'BLUE_SOLOON'
    PURPLE_SOLOON = 'PURPLE_SOLOON'
    WHITE_SOLOON = 'WHITE_SOLOON'

    UP_COMETH = 'UP_COMETH'
    RIGHT_COMETH = 'RIGHT_COMETH'
    DOWN_COMETH = 'DOWN_COMETH'
    LEFT_COMETH = 'LEFT_COMETH'
    
def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            if 'CANDIDATE_ID' not in config or not config['CANDIDATE_ID']:
                raise ValueError("CANDIDATE_ID is not set in the config file.")
            return config
    except FileNotFoundError:
        logging.error("The configuration file config.json does not exist.")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error("Error decoding config.json. Ensure it is valid JSON.")
        sys.exit(1)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        sys.exit(1)
    

def add_polyanet(i, j, value = '') -> None:
    payload = {'row': i, 'column': j, 'candidateId': candidateId}
    response = requests.post(f'{BASE_API_URL}/polyanets', json=payload)
    if response.status_code == 200:
        logging.info('Successfully added polyanet at row: %s, column: %s', i, j)
    else:
        logging.error('Failed to add polyanet at row: %s, column: %s - Status Code: %s', r, c, response.status_code)

def add_soloon(i, j, value) -> None:
    # this function should make the POST req and know about the exact params based on color.
    color = value.split('_')[0].lower()
    payload = {'row': i, 'column': j, 'candidateId': candidateId, 'color': color} # TODO: text/value validation. now fragile
    response = requests.post(f'{BASE_API_URL}/soloons', json=payload)
    if response.status_code == 200:
        logging.info('Successfully added soloon at row: %s, column: %s', i, j)
    else:
        logging.error('Failed to add soloon at row: %s, column: %s - Status Code: %s', i, j, response.status_code)

def add_comet(i, j, value) -> None:
    direction = value.split('_')[0].lower()
    payload = {'row': i, 'column': j, 'candidateId': candidateId, 'direction': direction}
    response = requests.post(f'{BASE_API_URL}/comeths', json=payload)
    if response.status_code == 200:
        logging.info('Successfully added comet at row: %s, column: %s', i, j)
    else:
        logging.error('Failed to add comet at row: %s, column: %s - Status Code: %s', i, j, response.status_code)

def handle(i, j, cell):
    if cell == CelestialBody.POLYANET.value:
        print(f'Polyanet found at: {i} {j}')
        add_polyanet(i, j)

def updateMap(i, j, cell):
    # this function should only determine polyanet/comet/soloon, and call resp. funciton
    # with the original value. strategy pattern
    if 'SOLOON' in cell:
        add_soloon(i, j, cell)
    elif 'POLYANET' in cell:
        add_polyanet(i, j, cell)
    elif 'COMET' in cell:
        add_comet(i, j, cell)
    

    # match cell:
    #     case CelestialBody.POLYANET.value:
    #         add_polyanet(i, j)
    #     case CelestialBody.SOLOON.value:
    #         add_soloon(i, j)
    #     case CelestialBody.COMET.value:
    #         add_comet(i, j)
    #     case _:
    #         logging.warning(f'Unknown celestial body {cell} at position ({i}, {j})')

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    config = load_config()
    global candidateId # design choice for convenience; not ideal
    candidateId = config['CANDIDATE_ID']
    
    # Phase 1:
    # resp = requests.get(f'{BASE_API_URL}/map/{candidateId}/goal')
    # goal = resp.json().get('goal') 
    
    # for i, row in enumerate(goal):
    #     for j, cell in enumerate(row):
    #         handle(i, j, cell)
    
    # Phase 2:
    resp = requests.get(f'{BASE_API_URL}/map/{candidateId}/goal')
    goal = resp.json().get('goal') 
    options = set()
    for i, row in enumerate(goal):
        for j, cell in enumerate(row):
            # options.add(cell)
            updateMap(i, j, cell)


if __name__ == '__main__':
    main()
