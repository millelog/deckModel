from Globals import BOARD_HEIGHT

class Deck:
    points = []
    boundingSegmentsLeft = []
    boundingSegmentsRight = []
    color = (0, 0, 1)
    boardPositions = []
    maxY = 0


    def __init__(self):
        self.color = (0, 0, 1)
        self.points = [(10, 10), (1000, 10), (1100, 510), (900, 1100), (10, 1100), (110, 700)]
        self.boundingSegmentsLeft = [{'yRange': (10, 700), 'points': ((10, 10), (110, 700))}, {'yRange': (700, 1100), 'points': ((110, 700), (10, 1100))}]
        self.boundingSegmentsRight = [{'yRange': (10, 510), 'points': ((1000, 10), (1100, 510))}, {'yRange': (510, 1100), 'points': ((1100, 510), (900, 1100))}]
        self.maxY = max(self.points, key=lambda idx: idx[1])[1]
        self.boardPositions = self.populateBoardPositions()

    def populateBoardPositions(self):
        boardPos = []
        y = 10
        while y < self.maxY:
            targetY = y + (BOARD_HEIGHT / 2)
            leftBound = self.XBound(targetY, self.boundingSegmentsLeft)
            rightBound = self.XBound(targetY, self.boundingSegmentsRight)
            if not leftBound or not rightBound:
                break
            width = rightBound-leftBound
            boardPos.append({'width': width, 'pos': (leftBound, y)})
            y += BOARD_HEIGHT
        return boardPos

    def pointSlopeX(self, y, p0, p1):
        return ((y - p0[1]) * (p1[0] - p0[0])) / (p1[1] - p0[1]) + p0[0]

    def XBound(self, y, boundingSegments):
        # boundingSegments[0]['yRange'] = height range of this segment
        # boundingSegments[0]['points'][0:1] = the two points defining the line for this segment
        for boundingSegment in boundingSegments:
            if boundingSegment['yRange'][0] < y <= boundingSegment['yRange'][1]:
                return self.pointSlopeX(y, boundingSegment['points'][0], boundingSegment['points'][1])

        return None

    def draw(self, ctx):
        if not self.points:
            return
        i = 0
        ctx.move_to(self.points[i][0], self.points[i][1])
        i += 1
        while i < len(self.points):
            ctx.line_to(self.points[i][0], self.points[i][1])
            i += 1
        ctx.close_path()
        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])
        ctx.set_line_width(.5)
        ctx.stroke()
