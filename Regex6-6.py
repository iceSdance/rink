import re


def compare(str_a: str, str_b: str):
    if len(str_a.removesuffix('$')) <= 1:
        return (str_a.removesuffix('$') in ['', '.', str_b[:1], '*', '+', '.?', '?']
                and (not str_b[1:] if str_a.endswith('$') else True)
                and (not str_b if str_a == '?$' else True))

    if str_a[0] == '\\':
        return str_b[:1] == str_a[1] and compare(str_a[2:], str_b[1:])
    if str_a[0:2] in ['.?', '.*']:
        return compare(str_a[2:], str_b) or compare(str_a[1:], str_b[1:])
    if not str_b:
        return False if str_a[1:] != '?' else True

    if str_a[0] in ['?']:
        return compare(str_a[1:], str_b)
    if str_a[0] in ['*', '+']:
        return True if compare(str_a[1:], str_b) else compare(str_a, str_b[1:])
    if str_a[0] not in ['.', str_b[:1]]:
        return False if str_a[1] not in ['?', '*'] else compare(str_a[{'?': 2, '*': 1}[str_a[1]]:], str_b)

    return compare(str_a[1:], str_b[1:])


def entrance(str_a: str, str_b: str):
    return compare(str_a.removeprefix('^'), str_b) if str_a.startswith('^') \
        else compare(str_a.removeprefix('^'), str_b) or bool(str_b) and entrance(str_a, str_b[1:])


# _______________Bunmijemiyo____________________________________begin__
def compare_char(regex, char):
    return regex == char or regex == '.' or not regex


def compare_eq_str(regex, string):
    if not regex or regex == "$" and not string:
        return True
    elif regex[0] == "\\":
        return compare_eq_str(regex[1:], string)
    elif len(regex) > 1 and regex[1] == "?" and string:
        return compare_eq_str(regex[2:], string) or compare_eq_str(regex[0] + regex[2:], string)
    elif len(regex) > 1 and regex[1] == "*" and string:
        return compare_eq_str(regex[2:], string) or compare_eq_str(regex, string[1:])
    elif len(regex) > 1 and regex[1] == "+" and string:
        return compare_eq_str(regex[0] + regex[2:], string) or compare_eq_str(regex, string[1:])
    elif not string or not compare_char(regex[0], string[0]):
        return False
    else:
        return compare_eq_str(regex[1:], string[1:])


def compare_str(regex, string):

    if not string and regex:
        return False
    elif compare_eq_str(regex, string):
        return True
    elif regex[0] == "^":
        return compare_eq_str(regex[1:], string)
    else:
        return compare_str(regex, string[1:])
# _______________Bunmijemiyo____________________________________end__


test_list = {
    '\.$|end.': 'T', '3\+3|3+3=6': 'T', '\?|Is this working?': 'T', '\\\\|\\': 'T',
    '\.$|endp': 'F', '3\+3|3-3=6': 'F', '\?|Is this working!': 'F', '\?\+|\\': 'F',
    'colou\?r|color': 'F', 'colou\?r|colour': 'F',
    '^ab*c$|abcabc': 'T',
    '^.?$|': 'T', '^.?$|s': 'T', '^.?$|ss': 'F', '^.?$|sss': 'F',
    'col.*r$|ecolorr': 'T',
    '^app|apple': '', 'le$|apple': '', '^a|apple': '', '.$|apple': '', 'apple$|tasty apple': '',
    'a|a': '', 'a|b': '', '.|abc': '', 'a|.': '', '|a': '', '|': '', 'a|': '',
    'apple|apple': '', 'apwle|apple': '',
    '.?|': '', '.*|': '', '.+|': 'F', '.+|r': 'T'
}

print(f"{''.rjust(max(map(len, [n for n in test_list])) + 7)}"
      f"{'submit'.center(7)}"
      f"{'re'.center(7)}"
      f"{'answer'.center(7)}"
      # f"{'Deny'.center(7)}"
      )
for re_in in test_list:
    regex_arg, input_arg = re_in.split('|')
    print(f"{regex_arg.rjust(max(map(len, [n.split('|')[0] for n in test_list])))}"
          f"|{input_arg.ljust(max(map(len, [n.split('|')[1] for n in test_list])))}", end='  ')

    print(str(entrance(regex_arg, input_arg)).ljust(5), end='  ')
    print(str(compare_str(regex_arg, input_arg)).ljust(5), end='  ')
    # print(str(rrrrr(regex_arg, input_arg)).ljust(5), end='  ')
    print(
        str((lambda regex, string: bool(re.search(regex, string) is not None and (not regex or string)))
        (regex_arg, input_arg)).ljust(5), end='  ')

    print(test_list[re_in])