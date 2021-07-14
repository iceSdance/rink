cells = '00010203041011121314202122232430313233344041424344'

len_s = 2  # length of each symbol in the cells
m = 5  # matrix_number

matrix = [[cells[i:i + len_s] for i in range(0, m * m * len_s, len_s)][j:j + m] for j in range(0, m * m, m)]
print(matrix)
# print the matrix
for i in range(m + 2):
    if i == 0 or i == m + 1:
        print('-' * (m * (len_s + 1) + 3))
    else:
        print('| ', end="")
        for j in range(m):
            print(matrix[i-1][j] + ' ', end="")
        print('|')