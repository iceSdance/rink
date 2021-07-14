import random


def print_checkerboard():
    for i in range(m + 2):
        if i == 0 or i == m + 1:
            print('-', end="")
            for h in range(1, m + 1):
                print('-' * len_s + str(h), end="")
            print('--')
        else:
            print(i, '', end="")
            for j in range(m):
                print(checkerboard[i-1][j].replace('_', ' ') + ' ', end="")
            print(i)


def one_move(xo):
    while True:
        move_x, move_y = input('Enter the coordinates: ').split()
        if not move_x.isdigit() or not move_y.isdigit():
            print('You should enter numbers!')
            continue
        elif not 0 < int(move_x) < m + 1 or not 0 < int(move_y) < m + 1:
            print(f'Coordinates should be from 1 to {m}!')
            continue
        elif checkerboard[(int(move_x) - 1)][(int(move_y) - 1)] != '_' * len_s:
            print('This cell is occupied! Choose another one!')
            continue
        else:
            global x, y
            x, y = int(move_x) - 1, int(move_y) - 1
            checkerboard[x][y] = xo
            break


def game_not_finish():
    row = [checkerboard[x][y + a] for a in range(max(-y, -(w - 1)), min(m - y, w))]
    column = [checkerboard[x + a][y] for a in range(max(-x, -(w - 1)), min(m - x, w))]
    diagonal_down = [checkerboard[x + a][y + a] for a in range(max(-x, -y, -(w - 1)), min(m - x, m - y, w))] \
        if m - abs(x - y) >= w else []  # diagonal\
    diagonal_up = [checkerboard[x - a][y + a] for a in range(max(-((m - 1) - x), -y, -(w - 1)), min(x + 1, m - y, w))] \
        if (x + 1) + (y + 1) > w and (m - x) + (m - y) > w else []  # diagonal/
    # the diagonal line maybe doesn't exist because it to short to win

    # check all possible combinations this point could win in the 4 lines:
    check = [row, column, diagonal_down, diagonal_up]
    # print(check)
    all_possible = [line[i:i + w] for line in check for i in range(len(line) - w + 1)]
    # print(all_possible)
    different_element_each = [len(set(combination)) for combination in all_possible]
    # print(different_element_each)
    if 1 in different_element_each:
        print(f'{all_possible[different_element_each.index(1)][1]} wins')
        return False
    elif '_' not in str(checkerboard):
        print('Draw')
        return False
    else:
        print('Game not finished')
        return True


len_s = 1  # length of each symbol in the cells
m = 9  # matrix_number
w = 4  # number of same symbols need to win
cells = '_' * len_s * m * m

checkerboard = [[cells[i:i + len_s] for i in range(0, m * m * len_s, len_s)][j:j + m] for j in range(0, m * m, m)]
# move = 1
checkerboard[random.randint(0, m - 1)][random.randint(0, m - 1)] = 'X' * len_s
print_checkerboard()

move = 2
x, y = 0, 0

while True:
    x_or_o = 'O' * len_s if move % 2 == 0 else 'X' * len_s
    one_move(x_or_o)
    print_checkerboard()
    if game_not_finish():
        move += 1
        continue
    else:
        break
