from Globals import BOARD_HEIGHT

class BoardPlacer:
    shortBoards = []
    longBoards = []
    deck = None

    def __init__(self, shortBoards, longBoards, deck):
        self.shortBoards = shortBoards
        self.longBoards = longBoards
        self.deck = deck

    def getBoardCombo(self, width, sbIndexes, lbIndexes):
        minDelta = 100000000
        sbIdx = 0
        lbIdx = 0
        for i in range(len(sbIndexes)):
            for j in range(len(lbIndexes)):
                delta = width-(self.shortBoards[i].width+self.longBoards[j].width)
                if delta < minDelta:
                    sbIdx = sbIndexes[i]
                    lbIdx = lbIndexes[j]
                    minDelta = delta
        return sbIdx, lbIdx

    def placeBoards(self):
        sbIndexes = []
        lbIndexes = []
        longNext = True
        for i in range(len(self.shortBoards)):
            sbIndexes.append(i)
        for i in range(len(self.longBoards)):
            lbIndexes.append(i)
        for position in self.deck.boardPositions:
            sbIdx, lbIdx  = self.getBoardCombo(position['width'], sbIndexes, lbIndexes)
            sbIndexes.remove(sbIdx)
            lbIndexes.remove(lbIdx)
            print(lbIndexes)
            if longNext:
                self.longBoards[lbIdx].position = position['pos']
                self.shortBoards[sbIdx].position = (position['pos'][0]+self.longBoards[lbIdx].width, position['pos'][1])
            else:
                self.shortBoards[sbIdx].position = position['pos']
                self.longBoards[lbIdx].position = (position['pos'][0]+self.shortBoards[sbIdx].width, position['pos'][1])
            self.longBoards[lbIdx].placed = True
            self.shortBoards[sbIdx].placed = True

            longNext = not longNext

