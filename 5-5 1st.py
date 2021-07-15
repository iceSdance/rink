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
            cells[(int(move_x) - 1) * 3 + (int(move_y) - 1)] = xo
            break


def game_not_finish():
    # prepare a list to check all the lines:
    check = []
    check += [cells[i:i + 3] for i in range(0, 9, 3)]  # all the rows of matrix
    check += [cells[i:i + 9:3] for i in range(0, 3)]  # all the columns of matrix
    check += [cells[0:9:4]]  # diagonal \ from top left to bottom right
    check += [cells[2:7:2]]  # diagonal / from top right to bottom left

    # a number list contain different element's number in each check line
    different_element_each = [len(set(line)) for line in check]

    if 1 in different_element_each and ' ' not in check[different_element_each.index(1)]:
        print(f'{check[different_element_each.index(1)][1]} wins')
        return False
    elif ' ' not in cells:
        print('Draw')
        return False
    else:
        return True


cells = [' ' for i in range(9)]
show_grid()
symbol = 'X'

while True:
    make_a_move(symbol)
    show_grid()
    if game_not_finish():
        symbol = 'XO'.strip(symbol)
        continue
    else:
        break
