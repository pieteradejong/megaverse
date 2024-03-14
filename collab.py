"""
Thu March 14, 2024 - Pieter de Jong
Crossmint Coding collaboration challenge

Battleship:

implement attakc function
coord player guess (x,y) -> return [miss, hit, sink, win]


deside:
- game state variabls
no constuictors
- only diff b/w ships in lengths
- board capped by 100x100
- need to map [x,y] -> ship present
- need a collection of ships, map: (i,j) -> set for ship
- if repeat attach on coords, then return 'error' -> in board, mark as "1"

design:
- board as list[list]
- cells are one of []
- function `attack`:
- if cell is None: miss
- if cell is ship: 
    if len(ship) == 1: ..
    delete coord from ship
    if win: return win
    elif sink: return sink
    else: return hit
    
[miss, hit, sink, win] 

"""
import logging


def init():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Initializing application...")

def attack(i, j) -> str:
    # returns either: [miss, hit, sink, win]
    cell = board[i][j]
    # print(f'expect 0: cell = {cell}')
    if cell == 1:
        return 'error'
    if cell == 0:
        return 'miss'
    if isinstance(cell, set):
        ship = cell 
        if len(ship) == 1:
            ships_all.remove(ship) # O(N)
            if len(ships_all) == 0:
                return 'win'
            else:
                return 'sink'
        else:
            ship.remove((i,j))
            print(f'expect to be 1: {len(ship)}')
            return 'hit'
    raise ValueError('erroneous cell error')


ships_all = []
ship1 = { (0,1), (0,2) }
ships_all.append(ship1)
board= [
    [0, ship1, ship1],
    [0, 0, 0],
    [0, 0, 0]
]
def main():
    logging.info("Starting application...")
    res = attack(0,0)
    print(f'expect res=miss: {res}')
    print(f'move result: {res}')
    res = attack(0,1)
    print(f'expect res=hit: {res}')

    logging.info("Finished application.")


if __name__ == "__main__":
    init()
    main()
