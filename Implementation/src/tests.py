import os

if __name__ == '__main__':
    try:
        tests = os.listdir('tests')
    except FileNotFoundError:
        exit('no tests directory')
    for t in tests:
        if t.startswith('test') and t.endswith('.py'):
            test = t[:-3]
            print ('\nTEST '+test+'\n')
            os.system('python3 -m unittest -v tests.'+test)
