import argparse
calc = argparse.ArgumentParser()
calc.add_argument("--type", type=str,
                  help="indicates the type of payment: 'annuity' or 'diff' (differentiated)")
calc.add_argument("-i", "--interest", type=float,
                  help="nominal interest rate (without percent sign). "
                       "accept a floating-point value. it must always be provided.")
calc.add_argument("-P", "--principal", type=float,
                  help="Principal. used for calculations of both types of payment")
calc.add_argument("-A", "--payment", type=float,
                  help="monthly payment amount. For --type=diff, the payment is different each month")
calc.add_argument("-n", "--periods", type=int,
                  help="number of months needed to repay the loan. ")
# loan = calc.parse_args("--type diff -i 7.8 -P 500000 -n 8".split())
# loan = calc.parse_args("--type diff -i 10 -P 1000000 -n 10".split())
# loan = calc.parse_args("--type annuity -i 5.6 -n 120 -A 8722".split())
# loan = calc.parse_args("--type annuity -i 10 -P 1000000 -n 60".split())
# loan = calc.parse_args("--type annuity -i 7.8 -P 500000 -A 23000".split())

# loan = calc.parse_args("--type shen -i 7.8 -P 500000 -A 23000".split())
# loan = calc.parse_args("--type diff -i 7.8 -P -500000 -A 23000".split())
# loan = calc.parse_args("--type diff -i 7.8 -P 500000".split())
# loan = calc.parse_args("--type diff -i 7.8 -P 500000 -A 23000".split())
# loan = calc.parse_args("--type annuity -P 500000 -A 23000".split())

i = loan.interest / 1200 if loan.interest is not None else None
P, n, A = loan.principal, loan.periods, loan.payment
parameters = [i, P, n, A]

if i is None or loan.type not in ['annuity', 'diff'] \
   or parameters.count(None) > 1 \
   or A is not None and loan.type == 'diff' \
   or any(parameter < 0 for parameter in parameters if parameter is not None):
    print('Incorrect parameters')

else:
    import math

    if loan.type == 'diff':
        Overpayment = 0
        for m in range(1, loan.periods + 1):
            Dm = math.ceil(P / n + i * (P - P * (m - 1) / n))
            print(f'Month {m}: payment is {math.ceil(Dm)}')
            Overpayment += math.ceil(Dm - P / n)
        print(f'Overpayment = {Overpayment}')

    if loan.type == 'annuity':
        for parameter in parameters:
            if parameter is not None:
                continue
            elif parameter == P:
                P = math.floor(A / (i * math.pow(1 + i, n) / (math.pow(1 + i, n) - 1)))
                print(f'Your loan principal = {P}!')
            elif parameter == A:
                A = math.ceil(P * i * math.pow(1 + i, n) / (math.pow(1 + i, n) - 1))
                print(f'Your monthly payment = {A}!')
            elif parameter == n:
                n = math.ceil(math.log(A / (A - i * P), 1 + i))
                print('It will take ', end='')
                print(f'1 year' if int(n // 12) == 1 else f'{int(n // 12)} years' if n >= 12 else '', end='')
                print(' and ' if n >= 12 and n % 12 != 0 else '', end='')
                print(f'1 month' if int(n % 12) == 1 else f'{int(n % 12)} months' if n % 12 != 0 else '', end='')
                print(' to repay the loan!')
            print(f'Overpayment = {round(A * n - P)}')
