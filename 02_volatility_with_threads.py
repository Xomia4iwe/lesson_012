# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
import csv
import threading
from utils import time_track, get_file_path


class Volatility(threading.Thread):

    def __init__(self, file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.volatility = None
        self.tiker_secid = None

    def run(self):
        max_number = float(0)
        min_number = float(999999999999)
        with open(file=self.file, encoding='utf-8') as r_file:
            file_reader = csv.DictReader(r_file, delimiter=",")
            for row in file_reader:
                if float(row["PRICE"]) > max_number:
                    max_number = float(row["PRICE"])
                if float(row["PRICE"]) < min_number:
                    min_number = float(row["PRICE"])
            average_price = (max_number + min_number) / 2
            self.volatility = (max_number - min_number) / average_price * 100
            self.tiker_secid = row["SECID"]


scan_folder = '/home/xomia4iwe/projects/My_Projects/lesson_012/trades/'
files = get_file_path(scan_folder=scan_folder)


@time_track
def main():
    zero_volatility = []
    volatility_list = []
    volatilitys = [Volatility(file=file) for file in files]
    for volatylity in volatilitys:
        volatylity.start()
    for volatylity in volatilitys:
        volatylity.join()
        if volatylity.volatility == 0:
            zero_volatility.append(volatylity.tiker_secid)
        else:
            volatility_list.append([volatylity.tiker_secid, volatylity.volatility])
    volatility_list.sort(key=lambda x: x[1], reverse=True)
    print('Максимальная волатильность:')
    for i in range(3):
        print(f'{volatility_list[i][0]}  -  {round(volatility_list[i][1], 2)} %')
    print('Минимальная волатильность:')
    for i in range(-3, 0):
        print(f'{volatility_list[i][0]}  -  {round(volatility_list[i][1], 2)} %')
    print('Нулевая волатильность:')
    for i in range(len(zero_volatility)):
        print(f'{zero_volatility[i]}', end=', ')


if __name__ == '__main__':
    main()
