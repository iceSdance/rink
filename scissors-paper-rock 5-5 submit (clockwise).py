import random


class MoreOptions:
    def __init__(self):
        self.options = ['rock', 'paper', 'scissors']
        self.score = 0

    def welcome(self):
        user_name = input('Enter your name:')
        print('hello, ' + user_name)
        rating = {}
        r = open('rating.txt', 'r')
        for i in r:
            name, rate = i.split()
            rating[name] = int(rate)
        self.score = 0 if user_name not in rating else rating[user_name]
        r.close()
        return self.score

    def play(self, score, options):
        if options.count(',') > 2:
            self.options = options.split(',')
        print("Okay, let's start")
        while True:
            user_chose = input()
            if "!exit" in user_chose:
                break
            elif "!rating" in user_chose:
                print('Your rating:', score)
            elif user_chose not in self.options:
                print('Invalid input')
            else:
                computer_chose = random.choice(self.options)
                x = self.options.index(user_chose) - self.options.index(computer_chose)
                if x == 0:
                    print(f'There is a draw {computer_chose}')
                    score += 50
                elif x in range(-(len(self.options) - 1), -int((len(self.options) - 1) / 2)) \
                       or x in range(1, int((len(self.options) - 1) / 2)):
                    print(f'Well done. The computer chose {computer_chose} and failed')
                    score += 100
                else:
                    print(f'Sorry, but the computer chose {computer_chose}')
        print('Bye!')


get_score = MoreOptions().welcome()
MoreOptions().play(get_score, input())