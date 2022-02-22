class Board:
    position = (0, 0)
    width = 0
    height = 0
    placed = False
    index = -1

    def __init__(self, pos, widthParam, heightParam):
        self.position = pos
        self.width = widthParam
        self.height = heightParam
        self.index = -1
        self.placed = False


    def draw(self, ctx):
        ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(.5)
        ctx.stroke()
