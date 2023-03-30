def header():
    while (level := int(input('level: '))) not in range(1, 7):
        print('The level should be within the range of 1 to 6')
    else:
        return f"{level * '#'} {input('text: ')}\n"


def _list():
    while (rows := int(input('Number of rows: '))) <= 0:
        print('The number of rows should be greater than zero')
    else:
        list_txt = ''
        for i in range(1, rows + 1):
            list_txt += (str(i) + '. ' if user_input == 'ordered-list' else '* ') \
                        + input(f"Row #{i}: ") + '\n'
        return list_txt


features = {'plain': lambda: input('text: '), 'bold': lambda: f"**{input('text: ')}**",
            'italic': lambda: f"*{input('text: ')}*", 'header': header,
            'link': lambda: f"[{input('Label: ')}]({input('URL: ')})",
            'inline-code': lambda: f"`{input('text: ')}`", 'new-line': lambda: '\n',
            'ordered-list': _list, 'unordered-list': _list}
msg = ''

while True:
    user_input = input('Choose a formatter: ')
    if user_input == '!help':
        print('Available formatters:', ' '.join(features)+'\nspecial commands: !help !done')
    elif user_input == '!done':
        with open('output.md', 'w') as output:
            output.write(msg)
        break
    elif user_input not in features:
        print('Unknown formatting type or command')
    else:
        msg += features[user_input]()
        print(msg)
