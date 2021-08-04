# event_space = ['1', '2', '3', '4']
event_space = ['HH', 'HT', 'TH', 'TT']
# event_space = ['1', '2', '3', '4', '5']
# event_space = ['1', '2', '3', '4', '5', '6', '7', '8']
F = [['∅']]
d = {1: "st", 2: "nd", 3: "rd"}

a = [event_space[0]]
num = [str(event_space.index(aa) + 1) + d.get(event_space.index(aa) + 1, "th") for aa in a]
F.append(a)
print(f'F: {F}')
while F[-1] != [event_space[-1]]:
    if F[-1][-1] == event_space[-1]:
        print(f"\nnow the very last element of F is '{F[-1][-1]}' which the last element of list{event_space}\n"
              f'next outcome will back to the {"&".join(num[:len(num) - 2])} {a[:len(a) - 2]} and append '
              f'the {event_space.index(a[len(a) - 2]) + 2}{d.get(event_space.index(a[len(a) - 2]) + 2, "th")}'
              f' element {[event_space[event_space.index(a[len(a) - 2]) + 1]]} of this event_space')
        a = a[:len(a) - 2] + [event_space[event_space.index(a[len(a) - 2]) + 1]]
        num = [str(event_space.index(aa) + 1) + d.get(event_space.index(aa) + 1, "th") for aa in a]
    else:
        print(f'\nnow F end with the {"&".join(num)} element of "{event_space}"')
        a = a + [event_space[event_space.index(a[len(a) - 1]) + 1]]
        num = [str(event_space.index(aa) + 1) + d.get(event_space.index(aa) + 1, "th") for aa in a]
        print(f'next append the {"&".join(num)} element: {a}')
    F.append(a)

    print(f'F: {F}')
print(f'now F have {len(F)} elements, '
      f'{"equals to" if len(F) == 2 ** len(event_space) else "it should be"} {2 ** len(event_space)}')
