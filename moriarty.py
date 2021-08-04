import argparse
a = argparse.ArgumentParser()
a.add_argument("file")
# b = a.parse_args()

filename = a.parse_args().file
# filename = b.file
opened_file = open(filename)
encoded_text = opened_file.read()  # read the file into a string
opened_file.close()  # always close the files you've opened
print(encoded_text)


def decode_caesar_cipher(s, n):
    alpha = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',.?!"
    s = s.strip()
    text = ''
    for c in s:
        text += alpha[(alpha.index(c) + n) % len(alpha)]
    print(len(alpha))
    print('Decoded text: "' + text + '"')


decode_caesar_cipher(encoded_text, 103)
