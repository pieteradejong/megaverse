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

Room for improvement:
- reduce number of HTTP calls
- 

Phase 2:
- fetch current map
- traverse current map; for each cell, if not 'SPACE', then `POST /api/[object]` with row, col as payload
- verify result at `https://challenge.crossmint.io/map`
- approach: traversal + individual POSTs seems necessary, as the endpoints do not accept a list of cells to update;
and there is no quickly discernable "algorithmic" way to determine calls to make.

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
    

def add_polyanet(i,j) -> None:
    payload = {'row': i, 'column': j, 'candidateId': candidateId}
    response = requests.post(f'{BASE_API_URL}/polyanets', json=payload)
    if response.status_code == 200:
        logging.info('Successfully added polyanet at row: %s, column: %s', i, j)
    else:
        logging.error('Failed to add polyanet at row: %s, column: %s - Status Code: %s', r, c, response.status_code)

def handle(i, j, cell):
    if cell == CelestialBody.POLYANET.value:
        print(f'Polyanet found at: {i} {j}')
        add_polyanet(i, j)

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
    print(goal)


if __name__ == '__main__':
    main()
