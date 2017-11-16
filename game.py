
import random, sys
import nose

# Miniproject: 2048 game.

def make_board():
    '''
    Create a game board in its initial state.
    The board is a dictionary mapping (row, column) coordinates
    (zero-indexed) to integers which are all powers of two (2, 4, ...).
    Exactly two locations are filled.
    Each contains either 2 or 4, with an 80% probability of it being 2.

    Arguments: none
    Return value: the board
    '''

    lstints = [2, 2, 2, 2, 4]
    value1 = lstints[random.randint(1, 5) % 5]
    value2 = lstints[random.randint(1, 5) % 5]
    x1, y1 = (random.randint(0, 3), random.randint(0, 3))
    while True:
        (x2, y2) = (random.randint(0, 3), random.randint(0, 3))
        if not (x1, y1) == (x2, y2):
            break
    return ({(x1, y1) : value1, (x2, y2) : value2})

def get_row(board, row_n):
    '''
    Return a row of the board as a list of integers.
    Arguments:
      board -- the game board
      row_n -- the row number

    Return value: the row
    '''

    assert 0 <= row_n < 4
    lst = []
    for i in range(0, 4):
        if (row_n, i) in board:
            lst.append(board[row_n, i])
        else:
            lst.append(0)
    return lst

def get_column(board, col_n):
    '''
    Return a column of the board as a list of integers.
    Arguments:
      board -- the game board
      col_n -- the column number

    Return value: the column
    '''

    assert 0 <= col_n < 4
    lst = []
    for i in range(0,4):
        if (i, col_n) in board:
            lst.append(board[i, col_n])
        else:
            lst.append(0)
    return lst

def put_row(board, row, row_n):
    '''
    Given a row as a list of integers, put the row values into the board.

    Arguments:
      board -- the game board
      row   -- the row (a list of integers)
      row_n -- the row number

    Return value: none; the board is updated in-place.
    '''

    assert 0 <= row_n < 4
    assert len(row) == 4
    for i in range(0, 4):
        if not row[i] == 0:
            board[row_n, i] = row[i]
        elif (row_n, i) in board:
            board.pop((row_n, i))

def put_column(board, col, col_n):
    '''
    Given a column as a list of integers, put the column values into the board.

    Arguments:
      board -- the game board
      col   -- the column (a list of integers)
      col_n -- the column number

    Return value: none; the board is updated in-place.
    '''

    assert 0 <= col_n < 4
    assert len(col) == 4
    for i in range(0, 4):
        if not col[i] == 0:
            board[i, col_n] = col[i]
        elif (i, col_n) in board:
            board.pop((i, col_n))

def make_move_on_list(numbers):
    '''
    Make a move given a list of 4 numbers using the rules of the
    2048 game.

    Argument:
      numbers -- a list of 4 numbers

    Return value:
      The list after moving the numbers to the left.  The original list
      is not altered.
    '''

    assert len(numbers) == 4
    numcpy = numbers[:]
    for i in numcpy:
        if i == 0:
            numbers.remove(0)
            numbers.append(0)
    for i in range(0, 3):
        if numbers[i] == numbers[i + 1] and not (numbers[i] == 0):
            numbers[i] += numbers[i + 1]
            numbers[i + 1] = 0
    numcpy = numbers[:]
    for i in numcpy:
        if i == 0:
            numbers.remove(0)
            numbers.append(0)
    while len(numbers) < 4:
        numbers.append(0)
    return numbers


def make_move(board, cmd):
    '''
    Make a move on a board given a movement command.
    Movement commands include:

      'w' -- move numbers upward
      's' -- move numbers downward
      'a' -- move numbers to the left
      'd' -- move numbers to the right

    Arguments:
      board  -- the game board
      cmd    -- the command letter

    Return value: none; the board is updated in-place.
    '''

    assert cmd in ['w', 'a', 's', 'd']
    if cmd == 'w':
        for i in range(0, 4):
            put_column(board, make_move_on_list(get_column(board, i)), i)
    if cmd == 'a':
        for i in range(0, 4):
            put_row(board, make_move_on_list(get_row(board, i)), i)
    if cmd == 's':
        for i in range(0, 4):
            lst = get_column(board, i)
            lst.reverse()
            make_move_on_list(lst)
            lst.reverse()
            put_column(board, lst,i)
    if cmd == 'd':
        for i in range(0, 4):
            lst = get_row(board, i)
            lst.reverse()
            make_move_on_list(lst)
            lst.reverse()
            put_row(board, lst, i)

def game_over(board):
    '''
    Return True if the game is over i.e. if no moves can be made on the board.
    The board is not altered.

    Argument: board -- the game board
    Return value: True if the game is over, else False
    '''

    referenceboard = board.copy()
    make_move(referenceboard, 'w')
    make_move(referenceboard, 'a')
    make_move(referenceboard, 's')
    make_move(referenceboard, 'd')
    if referenceboard == board and len(board) == 16:
        return True
    return False

def update(board, cmd):
    '''
    Make a move on a board given a movement command.  If the board has changed,
    then add a new number (2 or 4, 90% probability it's a 2) on a
    randomly-chosen empty square on the board.  This function assumes that a
    move can be made on the board.

    Arguments:
      board  -- the game board
      cmd    -- the command letter

    Return value: none; the board is updated in-place.
    '''

    insertionlist = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    referenceboard = board.copy()
    make_move(board, cmd)
    if not referenceboard == board:
        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if (x, y) not in board:
                board[(x, y)] = insertionlist[random.randint(1, 10)
                                             % len(insertionlist)]
                break


def display(board):
    '''
    Display the board on the terminal in a human-readable form.

    Arguments:
      board  -- the game board

    Return value: none
    '''

    s1 = '+------+------+------+------+'
    s2 = '| {:^4s} | {:^4s} | {:^4s} | {:^4s} |'

    print(s1)
    for row in range(4):
        c0 = str(board.get((row, 0), ''))
        c1 = str(board.get((row, 1), ''))
        c2 = str(board.get((row, 2), ''))
        c3 = str(board.get((row, 3), ''))
        print(s2.format(c0, c1, c2, c3))
        print(s1)

def play_game():
    '''
    Play a game interactively.  Stop when the board is completely full
    and no moves can be made.

    Arguments: none
    Return value: none
    '''

    b = make_board()
    display(b)
    while True:
        if game_over(b):
            print('Game over!')
            break

        move = input('Enter move: ')
        if move not in ['w', 'a', 's', 'd', 'q']:
            print("Invalid move!  Only 'w', 'a', 's', 'd' or 'q' allowed.")
            print('Try again.')
            continue
        if move == 'q':  # quit
            return
        update(b, move)
        display(b)


def list_to_board(lst):
    '''
    Convert a length-16 list into a board.
    '''
    board = {}
    k = 0
    for i in range(4):
        for j in range(4):
            if lst[k] != 0:
                board[(i, j)] = lst[k]
            k += 1
    return board

def random_game():
    '''Play a random game.'''
    board = make_board()
    display(board)
    while True:
        print()
        move = random.choice('wasd')
        update(board, move)
        display(board)
        if game_over(board):
            break