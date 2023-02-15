class CoffeeMachine:
    cost = {'1': {'water': -250, 'milk': 0, 'beans': -16, 'cups': -1, 'money': 4},
            '2': {'water': -350, 'milk': -75, 'beans': -20, 'cups': -1, 'money': 7},
            '3': {'water': -200, 'milk': -100, 'beans': -12, 'cups': -1, 'money': 6}}
    units = {'water': 'ml of', 'milk': 'ml of', 'beans': 'g of coffee', 'cups': 'disposable', 'money': 'of'}

    def __init__(self, stock):
        self.stock = stock

    def buy(self, coffee):
        shortage = [i for i in self.stock if self.stock[i] + self.cost[coffee][i] < 0]
        if len(shortage) != 0:
            print(f'Sorry, not enough {" and ".join(shortage)}!')
        else:
            for item in self.cost[coffee]:
                self.stock[item] += self.cost[coffee][item]
            print('I have enough resources, making you a coffee!')

    def fill(self):
        for item in ['water', 'milk', 'beans', 'cups']:
            self.stock[item] += int(input(f'Write how many {self.units[item]} {item} you want to add: \n'))

    def remaining(self):
        print(f'\nThe coffee machine has:')
        for item in list(self.stock.keys()):
            print(f"{'$' if item == 'money' else ''}{self.stock[item]} {self.units[item]} {item}")


current, income = {'water': 400, 'milk': 540, 'beans': 120, 'cups': 9, 'money': 550}, 0
while True:
    operation = input("\nWrite action (buy, fill, take, remaining, exit): \n")
    if operation == 'exit':
        break
    elif operation == 'buy':
        coffee = input("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: \n")
        if coffee in CoffeeMachine.cost:
            CoffeeMachine(current).buy(coffee)
    elif operation == 'fill':
        CoffeeMachine(current).fill()
    elif operation == 'take':
        print(f'I gave you ${current["money"]}')
        income += current['money']
        current['money'] = 0
    elif operation == 'remaining':
        CoffeeMachine(current).remaining()
