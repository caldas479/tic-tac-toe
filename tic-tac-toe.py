# Tiago Caldas ist199125

# AUXILIARY FUNCTIONS

def position_coordinates(p):
    """Returns the coordinates of a position on the board.

    :param p: Position
    :return: tuple, coordinates
    """
    board_positions = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    for row_index in range(3):
        for col_index in range(3):
            if board_positions[row_index][col_index] == p:
                return (row_index, col_index)

def organize_tuple(t):
    """Returns a tuple organized into board format.

    :param t: tuple
    :return: tuple, Board
    """
    c = 0
    row1, row2, row3 = (), (), ()
    for e in t:
        if c <= 2:
            row1 += (e,)
        elif c <= 5:
            row2 += (e,)
        else:
            row3 += (e,)
        c += 1
    return (row1, row2, row3)

def diagonal_position(p):
    """Returns the number of the diagonal where the position is located or False if it's not on any.

    :param p: Position
    :return: int or bool, 1 2 or False
    """
    diagonal1, diagonal2 = (1, 5, 9), (3, 5, 7)
    if p in diagonal1:
        return 1
    elif p in diagonal2:
        return 2
    else:
        return False

def fork_positions(tab, player):
    """Returns a tuple with all positions that can create a fork.

    Fork conditions: row-column/row-diagonal/column-diagonal and in the row, column, or diagonal where
    the intersection position is, there can only be one and only one player's piece. So their sum should be equal
    to the player's value.

    :param tab: Board
    :param player: int, player's value
    :return: tuple
    """
    fork_pos = (0,)  # To avoid returning None in case there is no fork
    for p in get_free_positions(tab):
        c, d = position_coordinates(p), diagonal_position(p)
        if sum(get_row(tab, c[0] + 1)) == sum(get_column(tab, c[1] + 1)) == player or \
                (d and sum(get_row(tab, c[0] + 1)) == sum(get_diagonal(tab, d)) == player) or \
                (d and sum(get_column(tab, c[1] + 1)) == sum(get_diagonal(tab, d)) == player):
            fork_pos += (p,)
    return fork_pos

# GAME MODES

def basic(tab):
    """Returns a position depending on the game strategies.

    :param tab: Board
    :return: Position
    """
    if center(tab):
        return center(tab)
    elif free_corner(tab):
        return free_corner(tab)
    elif free_side(tab):
        return free_side(tab)

def normal(tab, player):
    """Returns a position depending on the game strategies.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    if victory(tab, player):
        return victory(tab, player)
    elif block(tab, player):
        return block(tab, player)
    elif center(tab):
        return center(tab)
    elif opposite_corner(tab, player):
        return opposite_corner(tab, player)
    elif free_corner(tab):
        return free_corner(tab)
    elif free_side(tab):
        return free_side(tab)

def perfect(tab, player):
    """Returns a position depending on the game strategies.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    if victory(tab, player):
        return victory(tab, player)
    elif block(tab, player):
        return block(tab, player)
    elif fork(tab, player):
        return fork(tab, player)
    elif fork_block(tab, player):
        return fork_block(tab, player)
    elif center(tab):
        return center(tab)
    elif opposite_corner(tab, player):
        return opposite_corner(tab, player)
    elif free_corner(tab):
        return free_corner(tab)
    elif free_side(tab):
        return free_side(tab)

# GAME STRATEGY

def victory(tab, player):  # 1
    """Returns the first free position that allows one of the players to win the game.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    for p in get_free_positions(tab):
        new_tab = mark_position(tab, player, p)
        if winner_player(new_tab) != 0:  # If there is a winning player after marking one of the free positions
            return p

def block(tab, player):  # 2
    """Returns the first free position that allows the opponent to win.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    return victory(tab, -player)

def fork(tab, player):  # 3
    """Returns the first free position that allows the player to create a fork.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    if len(fork_positions(tab, player)) > 1:
        return fork_positions(tab, player)[1]

def fork_block(tab, player):  # 4
    """Returns the free position that allows blocking the opponent's fork.

    If the opponent only has one fork, returns that position.
    Otherwise, the player must create a 2 in a row, where their blocking is not in the opponent's forks.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    if len(fork_positions(tab, -player)) == 2:  # In case there is one fork
        return fork_positions(tab, -player)[1]
    elif len(fork_positions(tab, -player)) > 2:  # When there are more than one fork
        for p in get_free_positions(tab):
            c = position_coordinates(p)
            # To create a 2 in a row, there can only be one player's piece
            if sum(get_row(tab, c[0] + 1)) == player or sum(get_column(tab, c[1] + 1)) == player or \
                    sum(get_diagonal(tab, 1)) == player or sum(get_diagonal(tab, 2)) == player:
                new_tab = mark_position(tab, player, p)
                if block(new_tab, -player) not in fork_positions(tab, -player):
                    return p

def center(tab):  # 5
    """Returns the center position if it's free.

    :param tab: Board
    :return: Position
    """
    if is_position_free(tab, 5):
        return 5

def opposite_corner(tab, player):  # 6
    """Returns the position of the corner opposite to the opponent's corner if it's free.

    :param tab: Board
    :param player: int, player's value
    :return: Position
    """
    corners = (1, 3, 7, 9)
    for i in range(4):
        c = position_coordinates(corners[i])
        # Corner is occupied by the opponent and opposite corner is free
        if (tab[c[0]][c[1]] == -player and is_position_free(tab, corners[3 - i])):
            return corners[3 - i]

def free_corner(tab):  # 7
    """Returns the position of the first free corner.

    :param tab: Board
    :return: Position
    """
    corners = (1, 3, 7, 9)
    for c in corners:
        if is_position_free(tab, c):
            return c

def free_side(tab):  # 8
    """Returns the position of the first free side.

    :param tab: Board
    :return: Position
    """
    for side in (2, 4, 6, 8):
        if is_position_free(tab, side):
            return side

# MAIN PROGRAM CODE

def is_board(tab):
    """Checks if the argument is a board.

    Board conditions: tuple with 3 tuples, each with 3 elements 1, -1, or 0.

    :param tab: universal
    :return: bool, True or False
    """
    c = 0
    values = (1, 0, -1)
    if type(tab) == tuple and len(tab) == 3:
        for row in tab:
            if type(row) == tuple and len(row) == 3:
                for e in row:
                    if e in values and type(e) == int:
                        c += 1
    return c == 9

def is_position(p):
    """Checks if the argument is a position.

    :param p: universal
    :return: bool, True or False
    """
    return p in (1, 2, 3, 4, 5, 6, 7, 8, 9) and type(p) == int

def get_column(tab, c):
    """Returns a tuple with column 1, 2, or 3 of the board. Raises an error if the arguments are not valid.

    :param tab: Board
    :param c: int, column indicator
    :return: tuple, column
    """
    if not(is_board(tab) and c in (1, 2, 3) and type(c) == int):
        raise ValueError('get_column: one of the arguments is invalid')
    return (tab[0][c - 1], tab[1][c - 1], tab[2][c - 1])

def get_row(tab, r):
    """Returns a tuple with row 1, 2, or 3 of the board. Raises an error if the arguments are not valid.

    :param tab: Board
    :param r: int, row indicator
    :return: tuple, row
    """
    if not(is_board(tab) and r in (1, 2, 3) and type(r) == int):
        raise ValueError('get_row: one of the arguments is invalid')
    return tab[r - 1]

def get_diagonal(tab, d):
    """Returns a tuple with diagonal 1 or 2 of the board. Raises an error if the arguments are not valid.

    diagonal1: descending left to right
    diagonal2: ascending left to right

    :param tab: Board
    :param d: int, diagonal indicator
    :return: tuple, diagonal
    """
    if not(is_board(tab) and d in (1, 2) and type(d) == int):
        raise ValueError('get_diagonal: one of the arguments is invalid')
    if d == 1:
        return (tab[0][0], tab[1][1], tab[2][2])
    else:
        return (tab[2][0], tab[1][1], tab[0][2])

def board_str(tab):
    """Returns the string representing the board. Raises an error if the argument is not valid.

    :param tab: Board
    :return: string, Board representation
    """
    if not is_board(tab):
        raise ValueError('board_str: the argument is invalid')
    string = ''
    for i1 in range(3):  # Loop for each row
        row = tab[i1]
        for i2 in range(3):  # Loop for each element of the row
            if row[i2] == 1:
                string += ' X '
            elif row[i2] == -1:
                string += ' O '
            else:
                string += '   '
            if i2 == 0 or i2 == 1:  # After first and second element
                string += '|'
        if i1 == 0 or i1 == 1:  # After first and second row
            string += '\n-----------\n'
    return string

def is_position_free(tab, p):
    """Checks if the argument is a free position. Raises an error if the arguments are not valid.

    :param tab: Board
    :param p: Position
    :return: bool, True or False
    """
    if not(is_board(tab) and is_position(p)):
        raise ValueError('is_position_free: one of the arguments is invalid')
    c = position_coordinates(p)
    return tab[c[0]][c[1]] == 0

def get_free_positions(tab):
    """Returns a tuple with all free positions on the board. Raises an error if the argument is not valid.

    :param tab: Board
    :return: tuple, Free positions
    """
    if not is_board(tab):
        raise ValueError('get_free_positions: the argument is invalid')
    free_positions = ()
    positions = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    for p in positions:
        if is_position_free(tab, p):
            free_positions += (p,)
    return free_positions

def winner_player(tab):
    """Returns 1, -1, or 0 if player X, O, or none has won. Raises an error if the argument is not valid.

    :param tab: Board
    :return: int
    """
    if not is_board(tab):
        raise ValueError('winner_player: the argument is invalid')
    possibilities = (get_row(tab, 1), get_row(tab, 2), get_row(tab, 3),
                     get_column(tab, 1), get_column(tab, 2), get_column(tab, 3),
                     get_diagonal(tab, 1), get_diagonal(tab, 2))
    win_X, win_O = (1, 1, 1), (-1, -1, -1)
    for p in possibilities:
        if p == win_X:
            return 1
        elif p == win_O:
            return -1
    return 0

def mark_position(tab, player, p):
    """Returns the new board with the position marked by the player. Raises an error if the arguments are not valid.

    :param tab: Board
    :param player: int, player's value
    :param p: Position
    :return: Board
    """
    if not(is_board(tab) and player in (1, -1) and is_position(p)):
        raise ValueError('mark_position: one of the arguments is invalid')
    if not is_position_free(tab, p):
        raise ValueError('mark_position: the position is not free')
    c = position_coordinates(p)
    tab = list(tab)
    tab[c[0]] = list(tab[c[0]])
    tab[c[0]][c[1]] = player
    tab[c[0]] = tuple(tab[c[0]])
    return tuple(tab)


def manual_position_choice(tab):
    """Returns the position chosen by the player. Raises an error if the argument or position is not valid.

    :param tab: Board
    :return: Position
    """
    if not is_board(tab):
        raise ValueError('manual_position_choice: the argument is invalid')
    pos = int(input("Player's turn. Choose a free position: "))
    if pos not in get_free_positions(tab):
        raise ValueError('manual_position_choice: the entered position is invalid')
    return pos

def auto_position_choice(tab, player, strategy):
    """Returns the position chosen by the computer. Raises an error if the arguments are not valid.

    :param tab: Board
    :param player: int, player's value
    :param strategy: string
    :return: Position
    """
    if not(is_board(tab) and player in (1, -1) and strategy in ('basic', 'normal', 'perfect')):
        raise ValueError('auto_position_choice: one of the arguments is invalid')
    if strategy == 'basic':
        return basic(tab)
    elif strategy == 'normal':
        return normal(tab, player)
    else:
        return perfect(tab, player)

def tic_tac_toe_game(player, strategy):
    """Returns 'X', 'O', or 'DRAW' depending on the winning player. Raises an error if the arguments are not valid.

    :param player: string
    :param strategy: string
    :return: string
    """
    if not(player in ('X', 'O') and strategy in ('basic', 'normal', 'perfect')):
        raise ValueError('tic_tac_toe_game: one of the arguments is invalid')
    print("Welcome to TIC-TAC-TOE.\nThe player plays with '", player, "'.", sep='')
    tab = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    move_count = 0
    if player == 'X':
        while winner_player(tab) == 0:
            tab = mark_position(tab, 1, manual_position_choice(tab))  # Player starts
            print(board_str(tab))
            move_count += 1
            if move_count == 5 or winner_player(tab) != 0:  # In case of draw or player wins
                break
            print("Computer's turn (", strategy, "):", sep='')
            tab = mark_position(tab, -1, auto_position_choice(tab, -1, strategy))
            print(board_str(tab))
    else:
        while winner_player(tab) == 0:
            print("Computer's turn (", strategy, "):", sep='')
            tab = mark_position(tab, 1, auto_position_choice(tab, 1, strategy))  # Computer starts
            print(board_str(tab))
            if move_count == 4 or winner_player(tab) != 0:  # In case of draw or computer wins
                break
            tab = mark_position(tab, -1, manual_position_choice(tab))
            print(board_str(tab))
            move_count += 1
    if winner_player(tab) == 1:
        return 'X'
    elif winner_player(tab) == -1:
        return 'O'
    return 'DRAW'


# Change here
print(tic_tac_toe_game('X', 'perfect'))