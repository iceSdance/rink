import random
# not publish
class Dominos:
    def __init__(self):
        self.domino_set = [[i, j] for i in range(0, 7) for j in range(i, 7)]
        self.hand = {player: [] for player in ['computer', 'player']}
        self.stock_pieces = []
        self.status = ''
        self.snake = []
        self.play_in_turns = ()

    def deal_pieces(self):
        while True:
            random.shuffle(self.domino_set)
            first_pieces = [piece for piece in self.domino_set[:14] if piece[0] == piece[1]]
            if first_pieces:
                index = self.domino_set[:14].index(max(first_pieces))
                self.hand['computer'], self.hand['player'] = self.domino_set[0:7], self.domino_set[7:14]
                self.stock_pieces = self.domino_set[14:]
                self.status = ['computer', 'player'][index // 7]
                self.snake.append(self.hand[self.status].pop(index % 7))
                self.play_in_turns = (['computer', 'player'][i % 2] for i in range(index // 7 + 1, 999))
                return self.interface(self.play_in_turns)

    def interface(self, player):
        self.status = next(player)
        print(f"{'=' * 70}\n"
              f"Stock size: {len(self.stock_pieces)}\n"
              f"Computer size: {len(self.hand['computer'])}")
        print(f"\n{''.join(str(p) for p in self.snake)}" if len(self.snake) <= 6 else
              f"\n{''.join(str(p) for p in self.snake[:3])}...{''.join(str(p) for p in self.snake[-3:])}")
        print(f'\nYour pieces:', *[f'{i + 1}:{piece}' for i, piece in enumerate(self.hand['player'])], sep='\n')

        self.if_game_not_over()
        self.play_a_hand(self.status)
        return self.interface(self.play_in_turns)

    def if_game_not_over(self):
        for player, pieces in self.hand.items():
            if not pieces:
                print(f"Status: The game is over. {'You' if player == 'player' else 'The computer'} won!")
                exit()
        for number in [self.snake[0][0], self.snake[-1][-1]]:
            if sum([piece.count(number) for piece in self.snake]) == 8:
                print('Status: The game is over. It\'s a draw!')
                exit()

    def play_a_hand(self, current_player):
        if current_player == 'player':
            print('\nStatus:It\'s your turn to make a move. Enter your command.')
            piece_amount = len(self.hand[current_player])
            while True:
                while (command := input()) not in [str(i) for i in range(-piece_amount, piece_amount + 1)]:
                    print('Invalid input. Please try again.')
                    continue
                if self.verify_legal(self.hand[current_player][abs(int(command)) - 1], self.snake, int(command)):
                    return self.take_action(current_player, int(command))
                else:
                    print('Illegal move. Please try again.')

        if current_player == 'computer':
            input('\nStatus: Computer is about to make a move. Press Enter to continue...\n')
            self.hand['computer'] = sorted(self.hand['computer'],
               key=lambda p: sum([p_s.count(p[0]) + p_s.count(p[1]) for p_s in self.hand['computer'] + self.snake])
                                           , reverse=True)
            for i, piece in enumerate(self.hand['computer']):
                for side in [-1, 1]:
                    if self.verify_legal(piece, self.snake, side):
                        command = side * (i + 1)
                        return self.take_action(current_player, command)
            else:
                return self.take_action(current_player, 0)

    def take_action(self, current_player, command):
        if command:
            self.snake.insert(0 if command < 0 else len(self.snake), self.hand[current_player].pop(abs(command) - 1))
        elif self.stock_pieces:
            self.hand[current_player].append(self.stock_pieces.pop(random.randint(0, len(self.stock_pieces) - 1)))

    @staticmethod
    def verify_legal(piece, sequence, left_or_right):
        if left_or_right == 0:
            return True
        end = 0 if left_or_right < 0 else -1
        # piece = piece[::-1] if piece[1 + end] != sequence[end][end] else piece ## not work
        piece[0], piece[1] = (piece[0], piece[1]) if piece[1 + end] == sequence[end][end] else (piece[1], piece[0])
        return sequence[end][end] in piece


Dominos().deal_pieces()