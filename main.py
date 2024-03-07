"""
Thursday March 7, 2024. Crossmint "Megaverse" challenge.
Solution by Pieter de Jong.

Part 1: 
- fetch goal map
- traverse goal map; for each cell, if it's 'POLYANET', then `POST /api/polyanets` with row, col as payload
- verify result at `https://challenge.crossmint.io/map`


"""

import logging
import requests
import json
import sys

BASE_API_URL = 'https://challenge.crossmint.io/api'

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
    

def add_polyanet(r,c) -> None:
    payload = {'row': r, 'column': c}
    response = requests.post(f'{BASE_API_URL}/polyanets', json=payload)
    if response.status_code == 200:
        logging.info('Successfully added polyanet at row: %s, column: %s', r, c)
    else:
        logging.error('Failed to add polyanet at row: %s, column: %s - Status Code: %s', r, c, response.status_code)

def handle(i, j, cell):
    pass

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    config = load_config()
    candidateId = config['CANDIDATE_ID']
    
    resp = requests.get(f'{BASE_API_URL}/map/{candidateId}/goal')
    goal = resp.json().get('goal') 
    
    for i, row in enumerate(goal):
        print(row)
        for j, cell in enumerate(row):
            handle(i, j, cell)

if __name__ == '__main__':
    main()
