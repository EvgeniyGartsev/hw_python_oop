import datetime as dt
from typing import Union


class Calculator: 
    '''Базовый класс - калькулятор.'''

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record) -> None:
        '''Добавляет новую запись в список.'''

        # переменная хранит одну запись в виде списка
        list_record = [record.amount, record.comment, record.date]
        # добавляю запись в список
        self.records.append(list_record)

    def get_today_stats(self) -> float:
        '''Возвращает количество за сегодня.'''

        self.count_today: float = 0
        # из списка берем отдельные записи в виде списка
        for i in self.records:
            if dt.date.today() in i:
                self.count_today += i[0]
        return self.count_today
    
    def get_week_stats(self):
        '''Возвращает количество за неделю.'''
        
        self.count_week: float = 0
        # количество дней недели, 6 т.к. текущий день
        # плюс 6 получается 7
        week = dt.timedelta(days=6)
        for i in self.records:
            if i[1] >= (dt.date.today() - week):
                self.count_week += i[0]
        return self.count_week


class Record:
    '''Класс для записи данных.'''

    # формат в котором пользователь будет вводить данные
    _date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        if type(date) == dt.date:
            self.date = date 
        else:
            self.date = dt.date.strptime(date, _date_format)


class CaloriesCalculator(Calculator):
    '''Класс подсчета каллорий.'''

    def get_remained(self) -> float:
        '''Определяет, не превышен ли лимит.'''
    

