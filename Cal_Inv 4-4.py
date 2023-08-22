import csv
import sqlite3

class CalculatorInvestors:
    def __init__(self, ci_data):
        print('Welcome to the Investor Program!')
        self.conn = sqlite3.connect(ci_data)
        self.cur = self.conn.cursor()
        self.load_data()
        self.menu_ = {
            'MAIN MENU':     {'0': ('Exit', self.exit_cal),
                              '1': ('CRUD operations', self.menu, 'CRUD MENU'),
                              '2': ('Show top ten companies by criteria', self.menu, 'TOP TEN MENU')},
            'CRUD MENU':     {'0': ('Back', self.menu, 'MAIN MENU'),
                              '1': ('Create a company', self.create),
                              '2': ('Read a company', self.read),
                              '3': ('Update a company', self.update),
                              '4': ('Delete a company', self.delete),
                              '5': ('List all companies', self.list_all)},
            'TOP TEN MENU':  {'0': ('Back', self.menu, 'MAIN MENU'),
                              '1': ('List by ND/EBITDA', self.t10, 'ne'),
                              '2': ('List by ROE', self.t10, 'roe'),
                              '3': ('List by ROA', self.t10, 'roa')}}

    def menu(self, name):
        menu_msg = f'\n{name}\n' \
                   + '\n'.join(f'{i} {menu_text[0]}' for i, menu_text in self.menu_[name].items()) \
                   + '\nEnter an option:\n'
        while (option := input(menu_msg)) not in self.menu_[name]:
            print('Invalid option!')
        exe_menu = self.menu_[name][option]
        return exe_menu[1]() if len(exe_menu) == 2 else exe_menu[1](exe_menu[2])

    def load_data(self):
        tables = {'companies': 'companies (ticker STRING PRIMARY KEY,name STRING, sector STRING);',
                  'financial': '''financial (ticker STRING PRIMARY KEY,ebitda REAL,sales REAL,
                                             net_profit REAL,market_price REAL,net_debt REAL,assets REAL,
                                             equity REAL,cash_equivalents REAL,liabilities REAL);'''}
        for name in tables:
            self.cur.execute(f'CREATE TABLE IF NOT EXISTS {tables[name]}')
            if self.cur.execute(f'SELECT count(*) FROM {name};').fetchone()[0] == 0:
                with open(f"test/{name}.csv") as csv_file:
                    data = list(csv.reader(csv_file, delimiter=","))
                    for line in data[1:]:
                        self.cur.execute(f"INSERT INTO {name} VALUES {tuple(line)};")
                    for column in data[0]:
                        self.cur.execute(f'UPDATE {name} SET {column}=NULL WHERE {column}=""')
                    self.conn.commit()

    def search_by_name(self):
        name_search = input('Enter company name:\n')
        result_list = self.cur.execute(f"SELECT * FROM companies WHERE name LIKE '%{name_search}%'").fetchall()
        if len(result_list) == 0:
            print('Company not found!')
            return self.menu('MAIN MENU')
        else:
            print(*[f'{i} {com}' for i, com in enumerate([c[1] for c in result_list])], sep='\n')
            return [c[0] for c in result_list][int(input('Enter company number:\n'))]

    def input_financial_data(self, ticker):
        if self.cur.execute(f"SELECT count(*) FROM financial WHERE ticker='{ticker}'").fetchone()[0] == 0:
            self.cur.execute(f"INSERT INTO financial (ticker) VALUES ('{ticker}');")
        for item in ['ebitda', 'sales', 'net_profit', 'market_price', 'net_debt',
                     'assets', 'equity', 'cash_equivalents', 'liabilities']:
            fd = int(input(f"Enter {item.replace('_', ' ')} (in the format '987654321'):\n"))
            self.cur.execute(f"UPDATE financial SET {item}={fd} WHERE ticker='{ticker}';")
        self.conn.commit()

    def create(self):
        new_ticker = input(f"Enter ticker (in the format 'MOON'):\n")
        self.cur.execute(f"INSERT INTO companies (ticker) VALUES ('{new_ticker}');")
        for item in [('name', 'company', 'MOON Corp'), ('sector', 'industries', 'Technology')]:
            cc = input(f"Enter {item[1]} (in the format '{item[2]}'):\n")
            self.cur.execute(f"UPDATE companies SET {item[0]} = '{cc}' WHERE ticker='{new_ticker}';")
        self.input_financial_data(new_ticker)
        print('Company created successfully!')
        return self.menu('MAIN MENU')

    def read(self):
        ticker = self.search_by_name()
        query = f"SELECT ticker, name FROM companies WHERE ticker='{ticker}'"
        print(' '.join(list(self.cur.execute(query).fetchone())), end='\n')
        ind_v = self.cur.execute("""SELECT round(market_price / net_profit,2), round(market_price / sales,2), 
                                           round(market_price / assets,2), round(net_debt / ebitda,2), 
                                           round(net_profit / equity,2), round(net_profit / assets,2), 
                                           round(liabilities / assets,2) FROM financial """ +
                                   f"WHERE ticker='{ticker}'").fetchone()
        fi = {['P/E', 'P/S', 'P/B', 'ND/EBITDA', 'ROE', 'ROA', 'L/A'][i]: ind_v[i] for i in range(7)}
        print(*[f"{ind} = {fi[ind]}" for ind in fi], sep='\n')
        return self.menu('MAIN MENU')

    def update(self):
        ticker = self.search_by_name()
        self.input_financial_data(ticker)
        print('Company updated successfully!')
        return self.menu('MAIN MENU')

    def delete(self):
        ticker = self.search_by_name()
        self.cur.execute(f"DELETE FROM companies WHERE ticker='{ticker}'")
        self.conn.commit()
        print('Company deleted successfully!')
        return self.menu('MAIN MENU')

    def list_all(self):
        print('COMPANY LIST')
        all_companies = self.cur.execute(f"SELECT * FROM companies ORDER BY ticker;").fetchall()
        print(*[' '.join(list(company)) for company in all_companies], sep='\n')
        return self.menu('MAIN MENU')

    def t10(self, ind):
        fml = {'ne': 'net_debt / ebitda', 'roe': 'net_profit / equity', 'roa': 'net_profit / assets'}
        self.cur.execute(f"SELECT ticker, round({fml[ind]}, 2) as {ind} FROM financial ORDER BY {ind} DESC LIMIT 10;")
        t10 = self.cur.fetchall()
        print('TICKER', {'ne': 'ND/EBITDA', 'roe': 'ROE', 'roa': 'ROA'}[ind])
        for company in t10:
            print(company[0], company[1])
        return self.menu('MAIN MENU')

    def exit_cal(self):
        self.conn.close()
        print('Have a nice day!')
        exit()


CalculatorInvestors(f'investor.db').menu('MAIN MENU')
