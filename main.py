import cairo
import os
from numpy import random
from Board import Board
from Deck import Deck
from BoardPlacer import BoardPlacer
from Globals import BOARD_HEIGHT, WIDTH, HEIGHT


def initCtx(width, height):
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()
    return ctx


def drawAll(ctx, boardPlacer):
    boardPlacer.deck.draw(ctx)
    for board in boardPlacer.shortBoards:
        if board.placed:
            board.draw(ctx)
    for board in boardPlacer.longBoards:
        if board.placed:
            board.draw(ctx)
    for support in boardPlacer.supports:
        support.draw(ctx)


def genBoards(mean):
    boards = []
    lengths = random.normal(mean, 50, 100)
    for i in range(len(lengths)):
        boards.append(Board((0, 0), lengths[i], BOARD_HEIGHT))
    return boards


if __name__ == '__main__':
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = initCtx(WIDTH, HEIGHT)
    boardPlacer = BoardPlacer(genBoards(350), genBoards(575), Deck())
    boardPlacer.placeBoards()
    drawAll(ctx, boardPlacer)


    try:
        os.makedirs(os.path.join("_build", "png"))
    except EnvironmentError:
        pass
    filename = os.path.join("_build", "png", "%s.png" % 'test')

    surface.write_to_png(filename)



