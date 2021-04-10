from __future__ import annotations
from typing import Union, List, Dict
import datetime as dt


class Calculator:
    '''Базовый класс - калькулятор.'''

    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.records: List = []

    def add_record(self, record: Record) -> None:
        '''Добавляет новую запись в список.'''
        # переменная хранит одну запись в виде списка
        list_record: List = [record.amount, record.comment, record.date]
        # добавляю запись в список
        self.records.append(list_record)

    def get_today_stats(self) -> float:
        '''Возвращает количество за сегодня.'''

        self.count_today: float = 0
        # из списка берем отдельные записи в виде списка
        for i in self.records:
            if i[2].date() == dt.datetime.now().date():
                self.count_today += i[0]
        return self.count_today

    def get_week_stats(self) -> float:
        '''Возвращает количество за неделю.'''
        self.count_week: float = 0
        # количество дней недели
        week: dt.timedelta = dt.timedelta(days=7)
        for i in self.records:
            if i[2].date() >= (dt.datetime.now().date() - week):
                self.count_week += i[0]
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
            self.date = dt.datetime.strptime(date, date_format)


class CaloriesCalculator(Calculator):
    '''Класс подсчета каллорий.'''

    def get_calories_remained(self) -> float:
        '''Определяет, сколько еще можно съесть.'''
        self.total_value: float = 0
        self.diff_value: float = 0
        self.out_str: str = ''
        for i in self.records:
            if dt.datetime.now().date() == i[2].date():
                self.total_value += i[0]
        # определяем оставшееся количество
        self.diff_value = self.limit - self.total_value
        if self.diff_value > 0:
            self.out_str = (f'Сегодня можно съесть что-нибудь ещё, '
                            f'но с общей калорийностью не более '
                            f'{self.diff_value} кКал')
        else:
            self.out_str = 'Хватит есть!'
        return self.out_str


class CashCalculator(Calculator):
    '''Подсчитывает кол-во денег.'''
    USD_RATE: float = 77.0
    EURO_RATE: float = 91.7

    def get_today_cash_remained(self, currency: str):
        '''Определяет, сколько еще можно потратить.'''
        self.currency = currency
        # принимаемые валюты в виде списка и курсы
        self.cur: List = ['rub', 'usd', 'eur']
        # список для вывода валюты
        self.cur_dict: Dict = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        # если валюты нет в списке возвращаем None
        if self.currency not in self.cur:
            return None
        self.total_value: float = 0
        self.diff_value: float = 0
        self.out_str: str = ''
        # сколько потрачено за сегодня
        for i in self.records:
            if i[2].date() == dt.datetime.now().date():
                self.total_value += i[0]
        # определяем оставшееся количество
        # в зависимости от валюты
        if self.currency == self.cur[0]:
            self.diff_value = self.limit - self.total_value
        elif self.currency == self.cur[1]:
            self.diff_value = round(
                (self.limit - self.total_value) / self.USD_RATE, 2)
        elif self.currency == self.cur[2]:
            self.diff_value = round(
                (self.limit - self.total_value) / self.EURO_RATE, 2)
        # выводим запись о количестве
        if self.diff_value > 0:
            self.out_str = (f'На сегодня осталось '
                            f'{self.diff_value:.2f} {self.cur_dict[self.currency]}')
        elif self.diff_value == 0:
            self.out_str = 'Денег нет, держись'
        elif self.diff_value < 0:
            self.out_str = (f'Денег нет, держись: твой долг - '
                            f'{abs(self.diff_value):.2f} {self.cur_dict[self.currency]}')
        return self.out_str

#cash = CashCalculator(3000)
#cash.add_record(Record(400, 'sdf', '10.04.2021'))
#print(cash.get_today_cash_remained('usd'))