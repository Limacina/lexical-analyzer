from IO import IO_worker
from Analyser import Analyser
import pandas

while True:
    print('Enter text path: ')
    text = IO_worker(input()).read()
    if text:
        analyser = Analyser(text)
        analyser.analyse()
        print('No errors detected!')
        table = []
        for row in analyser.get_table():
            table.append(row.split(';'))
        df = pandas.DataFrame(table, columns=['Лексема', 'Тип лексемы', 'Значение'])
        print('Enter output file path: ')
        df.to_csv(input(), index=False, encoding='utf-8')
        print('Data written to csv, would you like to also watch it here? y/n: ')
        if input() == 'y':
            print(df)
    print('Continue? y/n: ')
    if input() != 'y':
        break
