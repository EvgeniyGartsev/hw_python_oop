from __future__ import annotations
from typing import Union, List, Dict, Tuple, Optional
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
        count_today: float = sum(i.amount for i in self.records
                                 if i.date == dt.datetime.now().date())
        return count_today

    def get_diff_today(self) -> float:
        '''Возвращает оставшееся количество за сегодня'''
        total_value: float = self.get_today_stats()
        diff_value: float = 0
        # определяем оставшееся количество
        diff_value = self.limit - total_value
        return diff_value

    def get_week_stats(self) -> float:
        '''Возвращает количество за неделю.'''
        week: dt.timedelta = dt.timedelta(days=7)
        count_week: float = sum(i.amount for i in self.records
                                if (dt.datetime.now().date() >= i.date
                                    >= (dt.datetime.now().date() - week)))
        return count_week


class Record:
    '''Класс для записи данных.'''

    def __init__(self, amount: float, comment: str,
                 date: Union[str, None] = None) -> None:
        date_format: str = '%d.%m.%Y'
        date_priv = (dt.datetime.now().date() if date is None else
                     dt.datetime.strptime(date, date_format).date())
        self.amount = amount
        self.comment = comment
        self.date = date_priv


class CaloriesCalculator(Calculator):
    '''Класс подсчета каллорий.'''

    def get_calories_remained(self) -> str:
        '''Определяет, сколько еще можно съесть.'''
        diff_value = self.get_diff_today()
        # определяем оставшееся количество
        if diff_value > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{diff_value} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    '''Подсчитывает кол-во денег.'''
    RUB_RATE: float = 1.0
    USD_RATE: float = 60.0
    EURO_RATE: float = 70.0
    # в словаре храним валюты, курс и способ вывода
    cur_out: Dict[str, Tuple[float, str]]
    cur_out = {'rub': (RUB_RATE, 'руб'),
               'usd': (USD_RATE, 'USD'),
               'eur': (EURO_RATE, 'Euro')}

    def get_today_cash_remained(self, currency: str) -> Optional[str]:
        '''Определяет, сколько еще можно потратить.'''
        currency_priv = currency.lower()
        # если валюты нет в списке возвращаем None
        if currency_priv not in self.cur_out.keys():
            return None
        # распаковываем курс и способ вывода
        cur_rate, cur_name = self.cur_out[currency_priv]
        # определяем оставшееся количество
        # в зависимости от валюты
        diff_value = round(
            self.get_diff_today() / cur_rate, 2)
        # выводим запись о количестве
        if diff_value == 0:
            return 'Денег нет, держись'
        if diff_value > 0:
            return (f'На сегодня осталось '
                    f'{diff_value:.2f} '
                    f'{cur_name}')
        return (f'Денег нет, держись: твой долг - '
                f'{abs(diff_value):.2f} '
                f'{cur_name}')
