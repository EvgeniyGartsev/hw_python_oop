import datetime as dt

date = '10.05.2020'
whatis = 'Datetime type' if type(date) == dt.datetime else 'string type'
print(whatis)
date_format = '%d.%m.%Y'
d = dt.datetime.strptime(date,date_format)
print(dt.date.today())