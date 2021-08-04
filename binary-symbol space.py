binary_symbol = ['Y', 'n']  # can't stop thinking what if a 3 or more element symbol list
s = 4
sample_space = []
Y_sample_space = {event: [] for event in range(1, s + 1)}
print(f'2 power {s}: {2 ** s}')

for d in range(1, s + 1):
    outcome = [binary_symbol[0] for _ in range(d)]
    sample_space.append(''.join(outcome))

    while outcome != [binary_symbol[1] for _ in range(d)]:
        for j in range(-1, -(d + 1), -1):
            outcome[j] = ''.join(binary_symbol).strip(outcome[j])
            if outcome[j] == binary_symbol[1]:
                sample_space.append(''.join(outcome))
                break
            else:
                continue
    # for outcome in sample_space:
    #     print(f'{" " * (len(str(len(sample_space))) - len(str(sample_space.index(outcome) + 1)))}'
    #           f'{sample_space.index(outcome) + 1} {outcome} ', end='')
    #     print('\n' if (sample_space.index(outcome) + 1) % 8 == 0 else '', end='')

    Y = [outcome for outcome in sample_space if outcome[-1] == binary_symbol[0] and len(outcome) == d]
    print(f'{Y}')
    Y_sample_space[d] = Y
    # n = [outcome for outcome in sample_space if outcome[-1] == binary_symbol[1]]
    # print(f'{n}')
print(sample_space)
print(Y_sample_space)