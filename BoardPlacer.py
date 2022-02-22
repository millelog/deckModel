from Globals import BOARD_HEIGHT, SUPPORT_WIDTH
from Support import Support


class BoardPlacer:
    shortBoards = []
    longBoards = []
    supports = []
    deck = None
    boardWidthsCombined = []

    def __init__(self, shortBoards, longBoards, deck):
        self.shortBoards = sorted(shortBoards, key=lambda x: x.width)
        self.longBoards = sorted(longBoards, key=lambda x: x.width)
        self.deck = deck
        self.supports = []
        self.boardWidthsCombined = self.buildBoardCombiner()

    def buildBoardCombiner(self):
        boardCombiner = []
        for i in range(len(self.shortBoards)):
            for j in range(len(self.longBoards)):
                boardCombiner.append({'sbIdx': i, 'lbIdx': j, 'width': self.shortBoards[i].width+self.longBoards[j].width})
        return sorted(boardCombiner, key=lambda x: x['width'])

    def getUniquePlacedSupportIndexes(self):
        supportGroupIdxs = []
        for bp in self.deck.boardPositions:
            if bp['lbIdx'] != -1 and bp['sbIdx'] != -1 and bp['supportIdx'] not in supportGroupIdxs:
                supportGroupIdxs.append(bp['supportIdx'])
        return supportGroupIdxs

    def getMinYInGroup(self, group):
        minY = 100000
        for boardPosition in group:
            if boardPosition['supportIdx'] % 2 == 0:
                minY = min(self.longBoards[boardPosition['lbIdx']].position[1], minY)
            else:
                minY = min(self.shortBoards[boardPosition['sbIdx']].position[1], minY)
        return minY

    def placeSupports(self):
        supportIdxs = self.getUniquePlacedSupportIndexes()
        for supportIdx in supportIdxs:
            supportGroup = self.getSupportGroup(supportIdx)
            meanSupportPos = self.getMeanSupportPos(supportGroup)
            xPos = meanSupportPos - SUPPORT_WIDTH/2
            yPos = self.getMinYInGroup(supportGroup)
            self.supports.append(Support(xPos, yPos))
            self.supports[supportIdx].print()


    def getSupportGroup(self, supportIdx):
        returnArray = []
        for bp in self.deck.boardPositions:
            if bp['supportIdx'] == supportIdx and bp['lbIdx'] != -1 and bp['sbIdx'] != -1:
                returnArray.append(bp)
        return returnArray

    def getMeanSupportPos(self, supportGroup):
        meanSupportPos = 0
        for sp in supportGroup:
            if sp['supportIdx'] % 2 == 0:
                meanSupportPos += self.shortBoards[sp['sbIdx']].position[0]
            else:
                meanSupportPos += self.longBoards[sp['lbIdx']].position[0]
        return meanSupportPos/len(supportGroup)

    def getMinMaxSupportGroup(self, supportGroup):
        widths = []
        for boardPosition in supportGroup:
            if boardPosition['supportIdx'] % 2 == 0:
                widths.append(self.longBoards[boardPosition['lbIdx']].width+boardPosition['pos'][0])
            else:
                widths.append(self.shortBoards[boardPosition['sbIdx']].width+boardPosition['pos'][0])
        return min(widths), max(widths)

    def invalidPairSupport(self, closestPair, supportIdx, boardPosIdx):
        supportGroup = self.getSupportGroup(supportIdx)
        supportGroup.append({'supportIdx': supportIdx, 'lbIdx': closestPair['lbIdx'], 'sbIdx': closestPair['sbIdx'], 'pos': self.deck.boardPositions[boardPosIdx]['pos']})
        if len(supportGroup) == 0:
            return False
        supportMin, supportMax = self.getMinMaxSupportGroup(supportGroup)
        return abs(supportMax-supportMin) > SUPPORT_WIDTH * .75

    def removeInvalidFromCombinedBoards(self, invalidPairs):
        if len(invalidPairs) == 0:
            return self.boardWidthsCombined

        returnArray = self.boardWidthsCombined
        for p in invalidPairs:
            for nbp in returnArray:
                if nbp['sbIdx'] == p['sbIdx'] or nbp['lbIdx'] == p['lbIdx']:
                    returnArray.remove(nbp)
        return returnArray

    def placeBoardPair(self, closestPair, boardPosIdx):
        self.shortBoards[closestPair['sbIdx']].placed = True
        self.longBoards[closestPair['lbIdx']].placed = True
        self.shortBoards[closestPair['sbIdx']].index = closestPair['sbIdx']
        self.longBoards[closestPair['lbIdx']].index = closestPair['lbIdx']
        self.removeBoardsFromCombo(closestPair['sbIdx'], closestPair['lbIdx'])
        self.deck.boardPositions[boardPosIdx]['lbIdx'] = closestPair['lbIdx']
        self.deck.boardPositions[boardPosIdx]['sbIdx'] = closestPair['sbIdx']
        position = self.deck.boardPositions[boardPosIdx]
        if position['shortFirst']:
            self.shortBoards[position['sbIdx']].position = position['pos']
            self.longBoards[position['lbIdx']].position = (
            position['pos'][0] + self.shortBoards[position['sbIdx']].width, position['pos'][1])
        else:
            self.longBoards[position['lbIdx']].position = position['pos']
            self.shortBoards[position['sbIdx']].position = (
            position['pos'][0] + self.longBoards[position['lbIdx']].width, position['pos'][1])

    def fillBoardPositions(self):
        invalidPairs = []
        for i in range(len(self.deck.boardPositions)):
            tryAgain = True
            while tryAgain:
                combinedBoardWidthsWoInvalid = self.removeInvalidFromCombinedBoards(invalidPairs)
                if len(combinedBoardWidthsWoInvalid) == 0:
                    return
                closestPair = self.get_closest_boardCombo(combinedBoardWidthsWoInvalid, self.deck.boardPositions[i]['width'])
                tryAgain = self.invalidPairSupport(closestPair, self.deck.boardPositions[i]['supportIdx'], i)
                if tryAgain:
                    invalidPairs.append(closestPair)
            self.placeBoardPair(closestPair, i)
            invalidPairs = []

    def removeBoardsFromCombo(self, sbIdx, lbIdx):
        self.boardWidthsCombined = [b for b in self.boardWidthsCombined if not (b['sbIdx'] == sbIdx or b['lbIdx'] == lbIdx)]

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

        self.placeSupports()
