import pygame, sys
from pygame.locals import *


def get_sudoku_problem():
    return [[6, 8, 5, 1, 3, -1, -1, 4, 7],
            [7, -1, -1, -1, -1, -1, -1, 1, -1],
            [-1, 1, -1, 7, 6, 4, -1, 5, -1],
            [9, -1, -1, -1, 7, -1, 5, -1, 4],
            [8, -1, 1, -1, -1, 9, -1, 7, 2],
            [4, -1, 3, -1,-1, 6, -1, -1, -1],
            [-1, -1, -1, 4, 2, 7, 3, 9, -1],
            [-1, 4, -1, 9, -1, -1, -1, 6, 8],
            [1, -1, 7, -1, -1, -1, 4, -1, -1]]


def find_solution():
    board = get_sudoku_problem()
    solve_grid(board, get_next_coordinate(board, (0, 0)), [], 1)


def solve_grid(board, coordinate, moves, offset):
    if is_solved(board):
        return True
    has_valid_cell_solution = solve_cell(board, coordinate, offset)
    if has_valid_cell_solution:
        moves.append((coordinate, board[coordinate[0]][coordinate[1]]))
        next_coordinate = get_next_coordinate(board, coordinate)
        update_display(board, next_coordinate)
        return solve_grid(board, next_coordinate, moves, 1)
    else:
        element = moves.pop()
        resetCoordinate = element[0]
        lastAttemptedValue = element[1]
        board[resetCoordinate[0]][resetCoordinate[1]] = -1
        update_display(board, resetCoordinate)
        return solve_grid(board, resetCoordinate, moves, lastAttemptedValue+1)


def solve_cell(board, coordinate,  index):
    if index >9:
        return False
    elif is_valid_entry(board, coordinate, index):
        board[coordinate[0]][coordinate[1]] = index
        return True
    else:
        return solve_cell(board, coordinate, index +1)


def is_solved(board):
    for row in board:
        for cell in row:
            if cell == -1:
                return False
    return True


def get_next_coordinate(board, coordinate):
    for row in board:
        for cell in row:
            if cell == -1 and (board.index(row) > coordinate[0] or (board.index(row) == coordinate[0] and row.index(cell) > coordinate[1])):
                return board.index(row), row.index(cell)
    return -1, -1


def is_valid_entry(board, coordinate, value):
    return is_valid_column(board, coordinate, value) \
           & is_valid_row(board, coordinate, value) \
           & is_valid_square(board, coordinate, value)


def is_valid_column(board, coordinate, value):
    for row in board:
        if row[coordinate[1]] == value:
            return False
    return True


def is_valid_row(board, coordinate, value):
    for cell in board[coordinate[0]]:
        if cell == value:
            return False
    return True


def is_valid_square(board, coordinate, value):
    v_square = get_square_indexes(coordinate[0] / 3)
    h_square = get_square_indexes(coordinate[1] / 3)
    for row in v_square:
        for cell in h_square:
            if board[row][cell] == value:
                return False
    return True


def get_square_indexes(limit):
    if limit < 1:
        return [0, 1, 2]
    elif limit < 2:
        return [3, 4, 5]
    elif limit < 3:
        return [6, 7, 8]


def print_hello_world():
    print("This line will be printed.")

# Sets size of grid
WINDOWMULTIPLIER = 5
WINDOWSIZE = 90
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
FPS= 5
# Set up the colours
BLACK = (0,  0,  0)
WHITE = (255,255,255)
LIGHTGRAY = (200, 200, 200)
RED = (235, 64, 52)
BASICFONTSIZE = 20


def init_game():
    global FPSCLOCK, DISPLAYSURF
    global BASICFONT, BASICFONTSIZE

    pygame.init()
    BASICFONT = pygame.font.SysFont("comicsansms", BASICFONTSIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Sudoku Solver')
    find_solution()
    # Puzzle Solved, wait for User to Exit
    while True:
        check_quit()


def update_display(board, currentWorkSquare):
    check_quit()
    render_grid(board, currentWorkSquare)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def check_quit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def render_grid(board, currentWorkSquare):
    DISPLAYSURF.fill(WHITE)
    SQUARESIZE = int((WINDOWMULTIPLIER * WINDOWSIZE) / 3)
    CELLSIZE = int(SQUARESIZE / 3)
    #minor lines
    draw_lines(CELLSIZE, LIGHTGRAY)
    #major lines
    draw_lines(SQUARESIZE, BLACK)
    
    draw_highlight_square(currentWorkSquare, CELLSIZE)
    populate_board_data(board, CELLSIZE)

def draw_highlight_square(currentWorkSquare, CELLSIZE):
    y = currentWorkSquare[0] * CELLSIZE
    x = currentWorkSquare[1] * CELLSIZE
    pygame.draw.lines(DISPLAYSURF, RED, True,
                      [(x, y), (x + CELLSIZE, y), (x + CELLSIZE, y + CELLSIZE), (x, y + CELLSIZE)]
                      )


def draw_lines(DEMARCATIONSIZE, COLOR):
    for x in range(0, WINDOWWIDTH, DEMARCATIONSIZE):
        pygame.draw.line(DISPLAYSURF, COLOR, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, DEMARCATIONSIZE):
        pygame.draw.line(DISPLAYSURF, COLOR, (0, y), (WINDOWWIDTH, y))


def populate_board_data(board, CELLSIZE):
    yOffset = 0
    for row in board:
        populate_row_data(row, yOffset, CELLSIZE)
        yOffset += CELLSIZE


def populate_row_data(row, yOffset, CELLSIZE):
    xOffset = 0
    for cell in row:
        if cell != -1:
            populate_cell(cell, xOffset, yOffset, CELLSIZE)
        xOffset += CELLSIZE


def populate_cell(cellData, x, y, CELLSIZE):
    cellSurf = BASICFONT.render('%s' %(cellData), True, BLACK)
    cellRect = cellSurf.get_rect()
    centerCell = CELLSIZE / 2
    cellRect.center = (x + centerCell, y + centerCell)
    DISPLAYSURF.blit(cellSurf, cellRect)

init_game()
