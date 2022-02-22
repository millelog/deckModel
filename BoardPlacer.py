from Globals import BOARD_HEIGHT

class BoardPlacer:
    shortBoards = []
    longBoards = []
    deck = None
    boardWidthsCombined = []

    def __init__(self, shortBoards, longBoards, deck):
        self.shortBoards = sorted(shortBoards, key=lambda x: x.width)
        self.longBoards = sorted(longBoards, key=lambda x: x.width)
        self.deck = deck
        self.boardWidthsCombined = self.buildBoardCombiner()

    def buildBoardCombiner(self):
        boardCombiner = []
        for i in range(len(self.shortBoards)):
            for j in range(len(self.longBoards)):
                boardCombiner.append({'sbIdx': i, 'lbIdx': j, 'width': self.shortBoards[i].width+self.longBoards[j].width})
        return sorted(boardCombiner, key=lambda x: x['width'])

    def placeBoard(self, closestPair, boardPosIdx):
        self.shortBoards[closestPair['sbIdx']].placed = True
        self.longBoards[closestPair['lbIdx']].placed = True
        self.removeBoardsFromCombo(closestPair['sbIdx'], closestPair['lbIdx'])
        self.deck.boardPositions[boardPosIdx]['lbIdx'] = closestPair['lbIdx']
        self.deck.boardPositions[boardPosIdx]['sbIdx'] = closestPair['sbIdx']

    def fillBoardPositions(self):
        for i in range(len(self.deck.boardPositions)):
            closestPair = self.get_closest_boardCombo(self.boardWidthsCombined, self.deck.boardPositions[i]['width'])
            self.placeBoard(closestPair, i)


    def removeBoardsFromCombo(self, sbIdx, lbIdx):
        self.boardWidthsCombined = [b for b in self.boardWidthsCombined if b['sbIdx'] != sbIdx and b['lbIdx'] != lbIdx]

    def get_closest_boardCombo(self, arr, target):
        n = len(arr)
        left = 0
        right = n - 1
        mid = 0

        # edge case - last or above all
        if target >= arr[n - 1]['width']:
            return arr[n - 1]
        # edge case - first or below all
        if target <= arr[0]['width']:
            return arr[0]
        # BSearch solution: Time & Space: Log(N)

        while left < right:
            mid = (left + right) // 2  # find the mid
            if target < arr[mid]['width']:
                right = mid
            elif target > arr[mid]['width']:
                left = mid + 1
            else:
                return arr[mid]

        if target < arr[mid]['width']:
            return self.find_closest(arr[mid - 1], arr[mid], target)
        else:
            return self.find_closest(arr[mid], arr[mid + 1], target)

    def find_closest(self, val1, val2, target):
        return val2 if target - val1['width'] >= val2['width'] - target else val1

    def placeBoards(self):
        self.fillBoardPositions()
        for position in self.deck.boardPositions:
            if position['shortFirst']:
                self.shortBoards[position['sbIdx']].position = position['pos']
                self.longBoards[position['lbIdx']].position = (position['pos'][0] + self.shortBoards[position['sbIdx']].width, position['pos'][1])
            else:
                self.longBoards[position['lbIdx']].position = position['pos']
                self.shortBoards[position['sbIdx']].position = (position['pos'][0] + self.longBoards[position['lbIdx']].width, position['pos'][1])
