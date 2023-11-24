class XmasPostcard:
    def __init__(self, width, height):
        self.canvas = list(map(list, ['-' * width,
                                      *[f"|{' ' * (width - 2)}|" for _ in range(height - 2)],
                                      '-' * width]))
        self.canvas[27] = list(f"|{'Merry Xmas'.center(width - 2)}|")

    @staticmethod
    def decorate_tree(h, interval):
        tiers, peg = ['^'], 0
        for tier in [list("/" + '*' * (i * 2 + 1) + "\\") for i in range(h - 1)]:
            for twig in range(1, len(tier) - 1):
                if twig % 2 == 0:
                    tier[twig] = 'O' if peg % interval == 0 else '*'
                    peg += 1
            tiers.append(tier)
        return tiers

    def place_(self, trees):
        for t in trees:
            tree, x, y = self.decorate_tree(t[0], t[1]), t[2], t[3]
            self.canvas[x][y] = 'X'
            for i in range(len(tree)):
                self.canvas[x + 1 + i][y - i:y + i + 1] = ''.join(tree[i])
            self.canvas[x + len(tree) + 1][y - 1:y + 2] = "| |"
        print(*[''.join(row) for row in self.canvas], sep='\n')


input_arg = list(map(int, input().split()))
if len(input_arg) >= 4:
    trees = [list(input_arg[i:i + 4]) for i in range(0, len(input_arg), 4) if len(input_arg[i:i + 4]) == 4]
    XmasPostcard(50, 30).place_(trees)
else:
    h, interval = input_arg[0], input_arg[1]
    tiers = XmasPostcard.decorate_tree(h, interval)
    print('X'.center(h * 2), *[''.join(tier).center(h * 2) for tier in tiers], '| |'.center(h * 2), sep='\n')



# 5 1 4 10 5 2 4 37 5 3 4 17 5 4 4 30 5 5 4 24 5 3 12 24 5 2 12 17 5 1 12 30
# 7 3 7 37 4 2 10 25 11 1 5 14 10 4 9 30 5 4 16 19
# 10 6
# 3 2
