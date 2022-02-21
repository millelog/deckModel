import cairo
import os
from numpy import random
from Board import Board
from Deck import Deck
from Support import Support
from BoardPlacer import BoardPlacer
from Globals import BOARD_HEIGHT, WIDTH, HEIGHT




def initCtx(width, height):
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()
    return ctx


def drawAll(ctx, deck, shortBoards, longBoards, supports):
    deck.draw(ctx)
    for board in shortBoards:
        if board.placed:
            board.draw(ctx)
    for board in longBoards:
        if board.placed:
            board.draw(ctx)
    for support in supports:
        support.draw(ctx)


def genBoards(mean):
    boards = []
    lengths = random.normal(mean, 40, 30)
    for i in range(len(lengths)):
        boards.append(Board((0, 0), lengths[i], BOARD_HEIGHT))
    return boards


if __name__ == '__main__':
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = initCtx(WIDTH, HEIGHT)
    boardPlacer = BoardPlacer(genBoards(400), genBoards(600), Deck())
    supports = []
    supports.append(Support(590, 10))
    boardPlacer.placeBoards()
    drawAll(ctx, boardPlacer.deck, boardPlacer.shortBoards, boardPlacer.longBoards, supports)


    try:
        os.makedirs(os.path.join("_build", "png"))
    except EnvironmentError:
        pass
    filename = os.path.join("_build", "png", "%s.png" % 'test')

    surface.write_to_png(filename)



