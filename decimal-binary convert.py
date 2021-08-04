def list_binary_str_fix_length(d):
    binary_str = ['0' for _ in range(d)]
    binary_str_list = [''.join(binary_str)]

    while binary_str != ['1' for _ in range(d)]:
        for j in range(-1, -(d + 1), -1):
            binary_str[j] = '01'.strip(binary_str[j])
            if binary_str[j] == '1':
                binary_str_list.append(''.join(binary_str))
                break
            else:
                continue
    return binary_str_list

d = 0
for binary in list_binary_str_fix_length(8):
    print(binary, d)
    d += 1