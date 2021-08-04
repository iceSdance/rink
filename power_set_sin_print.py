# event_space = ['1', '2', '3', '4']
# event_space = ['HH', 'HT', 'TH', 'TT']
event_space = ['Y', 'n']
F = [['∅'], [event_space[0]]]
outcomes = [event_space[0]]

while F[-1] != [event_space[-1]]:
    outcomes = outcomes[:len(outcomes) - 2] + [event_space[event_space.index(outcomes[len(outcomes) - 2]) + 1]]\
        if F[-1][-1] == event_space[-1]\
        else outcomes + [event_space[event_space.index(outcomes[len(outcomes) - 1]) + 1]]
    F.append(outcomes)
print(F)
print(f'F have {len(F)} elements, '
      f'{"equals to" if len(F) == 2 ** len(event_space) else "it should be"} '
      f'2^{len(event_space)}: {2 ** len(event_space)}')
