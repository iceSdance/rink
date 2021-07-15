def show_grid():
    for i in range(5):
        print('-' * 9 if i == 0 or i == 4 else f'| {cells[i * 3 - 3]} {cells[i * 3 - 2]} {cells[i * 3 - 1]} |')


def make_a_move(xo):
    while True:
        move_x, move_y = input('Enter the coordinates: ').split()
        if not move_x.isdigit() or not move_y.isdigit():
            print('You should enter numbers!')
            continue
        elif not 0 < int(move_x) < 4 or not 0 < int(move_y) < 4:
            print('Coordinates should be from 1 to 3!')
            continue
        elif cells[(int(move_x) - 1) * 3 + (int(move_y) - 1)] != ' ':
            print('This cell is occupied! Choose another one!')
            continue
        else:
            global x, y
            x, y = int(move_x) - 1, int(move_y) - 1
            cells[x * 3 + y] = xo
            break


def game_not_finish(c):
    # rows, columns, diagonal '\' (top left to bottom right), diagonal '/' top right to bottom left:
    check = [[c[x * 3 + (y + a)] for a in range(-y, 3 - y)],
             [c[(x + a) * 3 + y] for a in range(-x, 3 - x)],
             [c[(x + a) * 3 + (y + a)] for a in range(-x, 3 - x)] if x == y else [],
             [c[(x + a) * 3 + (y - a)] for a in range(-x, 3 - x)] if x + y == 2 else []]

    if check.count([symbol, symbol, symbol]) == 1:
        print(f'{symbol} wins')
        return False
    elif ' ' not in c:
        print('Draw')
        return False
    else:
        return True


cells = [' ' for _ in range(9)]
show_grid()
symbol = 'X'

while True:
    make_a_move(symbol)
    show_grid()
    if game_not_finish(cells):
        symbol = 'XO'.strip(symbol)
        continue
    else:
        break
