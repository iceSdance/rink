import random, time, csv, os
import argparse


class Duskers:
    game_title = f"""+{'=' * 78}+
                           ╔══╗──╔╗╔╦═╗──────╔╗
                           ║╔═╬═╦╝║╠╣═╣╔═╗─╔═╬╬╦╦╗
                           ║╚╗║╬║╬║║╠═║║╬╚╗║╬║║╔╣╚╗
                           ╚══╩═╩═╝╚╩═╝╚══╝╠╗╠╩╝╚═╝
                           ────────────────╚═╝
                       (Survival ASCII Strategy Game)\n+{'=' * 78}+\n\n"""
    robot = {'s': """┼┼┼┼┼▄▄▄▄┼┼┼┼┼┼
┼┼┼┼█┼┼┼┼█┼┼┼┼┼
┼┼┼▐┼┼┼┼┼┼┼┼┼┼┼
┼┼┼┼▀▀▄▄▄┼┼┼┼┼┼
┼┼┼┼┼┼┼┼┼▐┼┼┼┼┼
┼┼█┼┼┼┼┼┼█┼┼┼┼┼
┼┼┼┼█▄▄▀▀┼┼┼┼┼┼""",
             'p': """┼┼┼┼┼┼┼█┼┼▄▄┼┼┼┼
┼┼┼┼┼█▀█▄▀┼▐▌┼┼┼
┼┼┼┼█┼▐▀┼┼┼┼▌┼┼┼
┼┼┼┼┼┼██┼┼┼█┼┼┼┼
┼┼┼┼┼█┼┼█▄▀┼┼┼┼┼
┼┼┼┼█┼┼┼┼┼┼┼┼┼┼┼
┼┼▄█┼┼┼┼┼┼┼┼┼┼┼┼
┼┼█┼┼┼┼┼┼┼┼┼┼┼┼┼"""}

    border = '+' + '=' * 78 + '+'

    def __init__(self, ran_seed, min_dur, max_dur, *locations):
        random.seed(str(ran_seed))
        self.min_dur, self.max_dur = min_dur, max_dur
        self.locations = locations
        self.current_player, self.players_titanium, self.army = '', 0, 'sss'
        self.ts, self.es = False, False

        self.store = {'1': {'mechanic': 'Titanium Scan', 'price': 250},
                      '2': {'mechanic': 'Enemy Encounter Scan', 'price': 500},
                      '3': {'mechanic': 'New Robot (Strong)', 'price': 1000},
                      '4': {'mechanic': 'New Robot (Power)', 'price': 3000}}
        store_txt_len = max([sum([len(str(x)) for x in (item['mechanic'], item['price'])])
                             for item in self.store.values()]) + 2
        store_msg_slice = [f"[] {self.store[n]['mechanic'].ljust(len(self.store[n]['mechanic']) + 2)}"
                           + f"{str(self.store[n]['price']).rjust(store_txt_len - len(self.store[n]['mechanic']) - 2)}"
                           for n in self.store.keys()]
        self.menu = {
            'main': {'new': ('[]  Game', self.new),
                     'load': ('[] Game', self.save_file, 'load'),
                     'high': ('[] scores', self.high_score),
                     'help': ('[]', self.game_help),
                     'exit': ('[]', self.exit_game)},
            'new': {'yes': ('[]', self.menu_option, 'game'),
                    'no': ('[]', self.new_no),
                    'menu': ('Return to Main[]', self.menu_option, 'main')},
            'game': {'ex': ('[]plore', self.explore),
                     'up': ('[]grade', self.upgrade),
                     'save': ('[]', self.save_file, 'save'),
                     'm': ('[]enu', self.game_m)},
            'game_up': {str(n): (txt, self.comprar, str(n)) for n, txt in enumerate(store_msg_slice, start=1)},
            'game_m': {'back': ('[] to game', self.menu_option, 'game'),
                       'main': ('Return to [] Menu', self.menu_option, 'main'),
                       'save': ('[] and exit', self.save_file, 'save_and_exit'),
                       'exit': ('[] game', self.exit_game)},
            'high': {'back': ('       []', self.menu_option, 'main')}
        }
        self.menu['game_up'].update({' ': ('',), 'back': ('[]'.ljust(store_txt_len), self.menu_option, 'game')})

        self.save_file = 'save_file_sp.csv'
        self.score_file = 'score_file.csv'

    def menu_option(self, item: str, msg_pre='', common_interface=True):
        if common_interface:
            self.common_interface(item, msg_pre=msg_pre)
        option = self.input_command(*self.menu[item].keys())
        method = self.menu.get(item)[option][1]
        return method() if len(self.menu[item][option]) == 2 else method(self.menu[item][option][2])

    def common_interface(self, item, msg_pre=''):
        if item in ['game']:
            print(self.border)
            print('\n'.join(['  |  '.join(self.robot[typ].split('\n')[i] for typ in self.army) for i in range(7)]),
                  f"| Titanium: {str(self.players_titanium).ljust(67)}|",
                  f"|{'[Ex]plore'.center(39)}{'[Up]grade'.center(39)}|\n" +
                  f"|{'[Save]   '.center(39)}{'[M]enu   '.center(39)}|",
                  '', sep='\n' + self.border + '\n', end='')
        else:
            print((self.game_title if item in ['main'] else '') + msg_pre, end='')
            sep = {'main': '\n'}.get(item, ' ')
            print(sep.join(self.menu_msg(self.menu[item])))

    def new(self):
        self.current_player = input('\nEnter your name: ')
        self.players_titanium, self.army, self.ts, self.es = 0, 'sss', False, False
        print(f"\nGreetings, commander {self.current_player}!")
        return self.menu_option('new', msg_pre='Are you ready to begin?\n')

    def new_no(self):
        return self.menu_option('new', msg_pre='\nHow about now.\nAre you ready to begin?\n')

    def explore(self):
        total = random.randint(1, 9)
        locations = self.explore_search(1, {})
        for i in range(1, total + 1):
            while option := self.input_command(*list(locations.keys()), 's', 'back'):
                if option == 's':
                    if i == total:
                        print('Nothing more in sight.\n       [Back]')
                        continue
                    else:
                        locations = self.explore_search(i + 1, locations)
                        break
                elif option == 'back':
                    return self.menu_option('game')

                else:
                    self.animate("Deploying robots")
                    encounter = random.random() < locations[option][2] * {'s': 1, 'p': 0.5}.get(self.army[0], 1)
                    print(f"Enemy encounter\n" if encounter else '', end='')
                    self.army = self.army[1:] if encounter else self.army
                    if not self.army:
                        self.write_score()
                        print("Mission aborted, the last robot lost...")
                        self.banner_interface('GAME OVER!')
                        self.menu_option('main')
                    else:
                        self.players_titanium += locations[option][1]
                        print(f"\n{locations[option][0].replace('_', ' ')} explored successfully, " +
                              (f"with no damage taken. \n" if not encounter else '1 robot lost..\n') +
                              f"Acquired {locations[option][1]} lumps of titanium")
                    return self.menu_option('game')

    def explore_search(self, i, locations):
        self.animate('Searching')
        locations[str(i)] = (random.choice(self.locations), random.randint(10, 100), random.random())
        print('', *[f"[{n}] {locations[n][0].replace('_', ' ')} " +
                    (f"Titanium: {locations[n][1]} " if self.ts else '') +
                    (f"Encounter rate: {round(locations[n][2] * 100)}%" if self.es else '')
                    for n in locations.keys()], sep='\n')
        print('\n[S] to continue searching')
        return locations

    def save_file(self, action: str):
        print('   Select save slot:')
        if not os.path.isfile(self.save_file):
            with open(self.save_file, "w", encoding='utf-8') as new: pass

        with open(self.save_file, encoding='utf-8') as load:
            file_reader = csv.reader(load, delimiter=",")
            slots_dict = {str(n): record for n, record in zip(list(range(1, 4)), [slot for slot in file_reader])}

        for i in range(1, 4):
            slot = slots_dict.get(str(i), 'empty')
            print(f"    [{str(i)}] " + (slot if slot == 'empty' else
                  f"{slot[0]} Titanium: {slot[1]} Robots: {len(slot[2])} Last save: {slot[3]}" +
                  (f" Upgrades:{' titanium' if slot[4].title() == 'True' else ''}"
                   f"{' enemy' if slot[5].title() == 'True' else ''} info"
                   if slot[4].title() == 'True' or slot[5].title() == 'True' else '')))

        while n := self.input_command(*[str(i) for i in range(1, 4)], 'back'):
            if n == 'back':
                return self.menu_option({'load': 'main', 'save': 'game', 'save_and_exit': 'game'}[action])
            elif action == 'load' and slots_dict.get(n, 'empty') == 'empty':
                print('Empty slot!')
                continue
            else:
                break

        {'save': self.write_slot, 'save_and_exit': self.write_slot, 'load': self.load_slot}[action](slots_dict, n)
        if 'exit' in action:
            self.exit_game()
        return self.menu_option('game')

    def write_slot(self, slots_dict, n):
        slots_dict[n] = [self.current_player, self.players_titanium, self.army,
                         time.strftime('%Y-%m-%d %H:%M', time.localtime()), self.ts, self.es]
        with open(self.save_file, "w", encoding='utf-8') as save:
            # ["Name", "Titanium", "Robots", "Last_save"]
            file_writer = csv.writer(save, delimiter=",", lineterminator="\n")
            for slot in slots_dict.values():
                file_writer.writerow(slot)
        self.banner_interface('GAME SAVED SUCCESSFULLY')
        # self.write_score()

    def load_slot(self, slots_dict, n):
        self.current_player, self.army = slots_dict[n][0], slots_dict[n][2]
        self.ts = {'True': True, 'False': False}[slots_dict[n][4].title()]
        self.es = {'True': True, 'False': False}[slots_dict[n][5].title()]
        self.players_titanium = int(slots_dict[n][1])
        self.banner_interface('GAME LOADED SUCCESSFULLY')
        print(f"Welcome back, commander {self.current_player}!")

    def game_m(self):
        self.banner_interface('MENU', '', *self.menu_msg(self.menu['game_m'], 26))
        self.menu_option('game_m', common_interface=False)

    def upgrade(self):
        self.banner_interface('UPGRADE STORE', 'price'.rjust(28), *self.menu_msg(self.menu['game_up'], 29))
        self.menu_option('game_up', common_interface=False)

    def comprar(self, item):
        if self.players_titanium >= self.store[item]['price']:
            if self.store[item]['mechanic'] == 'Titanium Scan':
                if self.ts is True:
                    print('already buy this')
                    return self.menu_option('game_up', common_interface=False)
                self.ts = True
                print('Purchase successful. '
                      'You can now see how much titanium you can get from each found location.')
            if self.store[item]['mechanic'] == 'Enemy Encounter Scan':
                if self.es is True:
                    print('already buy this')
                    return self.menu_option('game_up', common_interface=False)
                self.es = True
                print('Purchase successful. '
                      'You will now see how likely you will encounter an enemy at each found location.')
            if 'New Robot' in self.store[item]['mechanic']:
                self.army += {'New Robot (Strong)': 's', 'New Robot (Power)': 'p'}[self.store[item]['mechanic']]
                print('Purchase successful. You now have an additional robot')
            self.players_titanium -= self.store[item]['price']
        else:
            print(f"Opps..you need {self.store[item]['price'] - self.players_titanium} "
                  f"more Titanium to exchange {self.store[item]['mechanic']}")
            return self.menu_option('game_up', common_interface=False)
        return self.menu_option('game')

    def write_score(self):
        score_record = [self.current_player, self.players_titanium, time.time()]
        with open(self.score_file, "a", encoding='utf-8') as score_file:
            # ["Name", "Titanium", "Time"]
            file_writer = csv.writer(score_file, delimiter=",", lineterminator="\n")
            file_writer.writerow(score_record)

    def high_score(self):
        if not os.path.isfile(self.score_file):
            with open(self.score_file, "w", encoding='utf-8') as new: pass
        with open(self.score_file, encoding='utf-8') as high:
            file_reader = csv.reader(high, delimiter=",")
            high_10 = [r for r in file_reader]
        print('\n   HIGH SCORES', end='\n\n')
        for n, record in zip(list(range(1, 11)), sorted(high_10, key=lambda x: int(x[1]), reverse=True)):
            print(f'({n})', *record[:2])
        return self.menu_option('high')

    def game_help(self):
        print('here is some help msg')
        return self.menu_option('main')

    def input_command(*options):
        while (option := input('\nYour command:\n').strip().lower()) not in options:
            print('Invalid input')
        return option

    def banner_interface(self, *msgs):
        banner_len = max(30, max(map(len, msgs)) + 4)
        banner_border = f"|{'=' * banner_len}|".center(80)
        banner_msg = '\n'.join([f"|{msg.center(banner_len)}|".center(80) for msg in msgs])
        print(banner_border, banner_msg, banner_border, sep='\n')

    def menu_msg(self, menu: dict, length=0) -> "prepare strings for display the menu":
        return [msg[0].replace('[]', f'[{command.title()}]').ljust(length) for command, msg in menu.items()]

    def animate(self, msg):
        print(msg, end='')
        waiting_dur = 0 if self.min_dur + self.max_dur == 0 else random.randint(self.min_dur, self.max_dur)
        for _ in range(waiting_dur):
            time.sleep(0.2)
            print('.', end='')

    def exit_game(self):
        print('\nThanks for playing, bye!')
        exit()

# arg = argparse.ArgumentParser()
# arg.add_argument('ran_seed', default=10)
# arg.add_argument('min_dur', default=0)
# arg.add_argument('max_dur', default=0)
# arg.add_argument('locations', default='Destroyed_Arch,High_street,Green_park,Old_beach_bar')
# d_arg = arg.parse_args()
# d_arg = arg.parse_args('10 0 0 Low_street,Red_park,Perfect_Archl'.split())
# Duskers(d_arg.ran_seed, int(d_arg.min_dur), int(d_arg.max_dur), *d_arg.locations.split(',')).menu_option('main')
Duskers(23, 0, 0, 'Ice_Rink', 'Yi_He_Yuan', 'Yu_Yuan_Tan', 'Zi_Zhu_Yuan').menu_option('main')

# python3 -u duskers6-5.py 10 0 2 Low_street,Red_park,Perfect_Arch
