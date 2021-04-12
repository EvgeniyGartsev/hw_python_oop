from __future__ import annotations
from typing import Union, List, Dict
import datetime as dt


class Calculator:
    '''Базовый класс - калькулятор.'''

    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        '''Добавляет новую запись в список.'''
        # добавляю запись в список
        self.records.append(record)

    def get_today_stats(self) -> float:
        '''Возвращает количество за сегодня.'''

        self.count_today: float = 0
        # из списка берем отдельные записи
        for i in self.records:
            if i.date == dt.datetime.now().date():
                self.count_today += i.amount
        return self.count_today

    def get_week_stats(self) -> float:
        '''Возвращает количество за неделю.'''
        self.count_week: float = 0
        # количество дней недели
        week: dt.timedelta = dt.timedelta(days=7)
        for i in self.records:
            if (dt.datetime.now().date() >= i.date
               >= (dt.datetime.now().date() - week)):
                self.count_week += i.amount
        return self.count_week


class Record:
    '''Класс для записи данных.'''

    def __init__(self, amount: float, comment: str, date: Union[str,
                 dt.datetime] = dt.datetime.now()):
        self.amount = amount
        self.comment = comment
        date_format: str = '%d.%m.%Y'
        if type(date) == dt.datetime:
            self.date = date.date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class CaloriesCalculator(Calculator):
    '''Класс подсчета каллорий.'''

    def get_calories_remained(self) -> float:
        '''Определяет, сколько еще можно съесть.'''
        total_value: float = self.get_today_stats()
        diff_value: float = 0
        out_str: str = ''

        # определяем оставшееся количество
        diff_value = self.limit - total_value
        if diff_value > 0:
            out_str = (f'Сегодня можно съесть что-нибудь ещё, '
                       f'но с общей калорийностью не более '
                       f'{diff_value} кКал')
        else:
            out_str = 'Хватит есть!'
        return out_str


class CashCalculator(Calculator):
    '''Подсчитывает кол-во денег.'''
    USD_RATE: float = 77.0
    EURO_RATE: float = 91.7

    def get_today_cash_remained(self, currency: str):
        '''Определяет, сколько еще можно потратить.'''
        self.currency = currency.lower()
        # принимаемые валюты в виде списка и курсы
        self.cur: List = ['rub', 'usd', 'eur']
        # список для вывода валюты
        self.cur_dict: Dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        # если валюты нет в списке возвращаем None
        if self.currency not in self.cur:
            return None
        total_value: float = self.get_today_stats()
        diff_value: float = 0
        out_str: str = ''
        # определяем оставшееся количество
        # в зависимости от валюты
        if self.currency == self.cur[0]:
            diff_value = self.limit - total_value
        elif self.currency == self.cur[1]:
            diff_value = round(
                (self.limit - total_value) / self.USD_RATE, 2)
        elif self.currency == self.cur[2]:
            diff_value = round(
                (self.limit - total_value) / self.EURO_RATE, 2)
        # выводим запись о количестве
        if diff_value > 0:
            out_str = (f'На сегодня осталось '
                            f'{diff_value:.2f} '
                            f'{self.cur_dict[self.currency]}')
        elif diff_value == 0:
            out_str = 'Денег нет, держись'
        elif diff_value < 0:
            out_str = (f'Денег нет, держись: твой долг - '
                            f'{abs(diff_value):.2f} '
                            f'{self.cur_dict[self.currency]}')
        return out_str


kal = CaloriesCalculator(1000)
kal.add_record(Record(500, 'sss', '12.04.2021'))
kal.add_record(Record(200, 'sss', '12.04.2021'))
kal.add_record(Record(100, 'sss', '12.04.2021'))

print(kal.get_calories_remained())


cash = CashCalculator(2000)
cash.add_record(Record(300, 'fdd', '12.04.2021'))
cash.add_record(Record(300, 'fdd', '12.04.2021'))
cash.add_record(Record(300, 'fdd', '12.04.2021'))
print(cash.get_today_cash_remained('uSd'))