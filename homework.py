import datetime as dt
from typing import Union


class Calculator:
    '''Базовый класс - калькулятор.'''

    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.records: list = []

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
            if i[2].date() == dt.datetime.now().date():
                self.count_today += i[0]
        return self.count_today

    def get_week_stats(self):
        '''Возвращает количество за неделю.'''
        self.count_week: float = 0
        # количество дней недели
        week = dt.timedelta(days=7)
        for i in self.records:
            if i[2].date() >= (dt.datetime.now().date() - week):
                self.count_week += i[0]
        return self.count_week


class Record:
    '''Класс для записи данных.'''

    def __init__(self, amount, comment, date=dt.datetime.now()):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
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
        for i in self.records:
            if dt.datetime.now().date() == i[2].date():
                self.total_value += i[0]     
        # определяем оставшееся количество
        self.diff_value = self.limit - self.total_value
        if self.diff_value > 0:
            self.out_str: str = (f'Сегодня можно съесть что-нибудь ещё, '
                           f'но с общей калорийностью не более '
                           f'{self.diff_value} кКал')
        else:
            self.out_str = f'Хватит есть!'
        
        return self.out_str


class CashCalculator(Calculator):
    '''Подсчитывает кол-во денег.'''
    USD_RATE: float = 77.0
    EURO_RATE: float = 91.7
    def get_today_cash_remained(self, currency: str):
        '''Определяет, сколько еще можно потратить.'''
        self.currency = currency
        # принимаемые валюты в виде списка и курсы
        cur = ['rub', 'usd', 'eur']
        # если валюты нет в списке возвращаем None
        if self.currency not in cur:
            return None  
        
        self.total_value: float = 0
        self.diff_value: float = 0
        # сколько потрачено за сегодня
        for i in self.records:
            if i[2].date() == dt.datetime.now().date():
                self.total_value += i[0]     
        # определяем оставшееся количество
        # в зависимости от валюты
        if self.currency == 'rub':
            self.diff_value = self.limit - self.total_value
        elif self.currency == 'usd': 
            self.diff_value = round((self.limit - self.total_value) / self.USD_RATE, 2)
        elif self.currency == 'eur': 
            self.diff_value = round((self.limit - self.total_value) / self.EURO_RATE, 2)
        # выводим запись о количестве
        if self.diff_value > 0:
            self.out_str: str = (f'На сегодня осталось '
                                 f'{self.diff_value} {self.currency}')
        elif self.diff_value == 0:
            self.out_str = 'Денег нет, держись'
        elif self.diff_value < 0:
            self.out_str = (f'Денег нет, держись: твой долг - '
                           f'{abs(self.diff_value)} {self.currency}')
        return self.out_str

##############################################проверка##########################################

calc = CashCalculator(2000)
r = Record(230, 'на велосипед', '08.04.2021')
calc.add_record(Record(230, 'на велосипед', '08.04.2021'))
calc.add_record(Record(400, 'на самолет', '09.04.2021'))
calc.add_record(Record(133, 'на пулемет', '09.04.2021'))
calc.add_record(Record(10, 'на трусики', '02.04.2021'))
calc.add_record(Record(133, 'на карты', '01.04.2021'))

#print(calc.get_week_stats())
#print(230+400+133+10)

#print(calc.get_today_cash_remained('rub'))
calc.add_record(Record(500, 'на авто', '10.04.2021'))
calc.add_record(Record(200, 'на дом', '10.04.2021'))
calc.add_record(Record(1300, 'на отпуск', '10.04.2021'))
calc.add_record(Record(1, 'на сигу', '10.04.2021'))

#print(calc.get_today_cash_remained('rub'))
#print(calc.get_today_cash_remained('eur'))
#print(calc.get_today_cash_remained('usd'))

#print(f'self.date = {r.date.date()}')
#print(f'Now = {dt.datetime.now().date()}')
#print(calc.get_today_stats())


#week = dt.timedelta(days=7)
#w = dt.datetime.now().date() - week
#print(dt.datetime.now().date() > w)


# проверяю калькулятор каллорий
kall = CaloriesCalculator(3000)
kall.add_record(Record(200, 'Печеньки', '02.04.2021'))
kall.add_record(Record(300, 'Тортик', '03.04.2021'))
kall.add_record(Record(100, 'Мяско', '04.04.2021'))
kall.add_record(Record(600, 'Рыбка', '10.04.2021'))
kall.add_record(Record(400, 'Чизкейк', '10.04.2021'))
kall.add_record(Record(333, 'Чизкейк', '10.04.2021'))
kall.add_record(Record(1800, 'Чизкейк', '10.04.2021'))

print(kall.get_today_stats())
print(kall.get_week_stats())
print(kall.get_calories_remained())