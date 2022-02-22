from Globals import SUPPORT_WIDTH
class Support:
    x = 0
    y = 0
    width = SUPPORT_WIDTH
    height = 280

    def __init__(self, xPos, yPos):
        self.x = xPos
        self.y = yPos

    def draw(self, ctx):
        ctx.rectangle(self.x, self.y, self.width, self.height)
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(.5)
        ctx.stroke()
    def print(self):
        print("X: "+str(self.x)+" | Y: "+str(self.y))