from Globals import BOARD_HEIGHT

class BoardPlacer:
    shortBoards = []
    longBoards = []
    deck = None

    def __init__(self, shortBoards, longBoards, deck):
        self.shortBoards = shortBoards
        self.longBoards = longBoards
        self.deck = deck

    def placeBoards(self):
        sbIdx = 0
        lbIdx = 0
        for position in self.deck.boardPositions:
            if sbIdx <= lbIdx:
                self.shortBoards[sbIdx].position = position['pos']
                sbIdx += 1
            else:
                self.longBoards[lbIdx].position = position['pos']
                lbIdx += 1

