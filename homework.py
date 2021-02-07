import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record():
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator():
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def today_balance(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        today = dt.date.today()
        date_week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if date_week_ago < record.date <= today)


class CashCalculator(Calculator):
    USD_RATE = 78.0
    EURO_RATE = 92.0

    def get_today_cash_remained(self, currency):
        currency_dict = {
            'rub': {
                'cur_name': 'руб',
                'cur_rate': 1
            },
            'usd': {
                'cur_name': 'USD',
                'cur_rate': self.USD_RATE
            },
            'eur': {
                'cur_name': 'Euro',
                'cur_rate': self.EURO_RATE
            }
        }
        today_remainder = round(self.today_balance() /
                                currency_dict[currency]['cur_rate'], 2)
        if self.today_balance() > 0:
            return (f"На сегодня осталось {today_remainder} "
                    f"{currency_dict[currency]['cur_name']}")
        elif self.today_balance() == 0:
            return 'Денег нет, держись'
        else:
            return (f"Денег нет, держись: твой долг - {abs(today_remainder)} "
                    f"{currency_dict[currency]['cur_name']}")


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.today_balance() > 0:
            return ("Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {self.today_balance()} кКал")
        else:
            return 'Хватит есть!'


if __name__ == '__main__':
    # для CashCalculator
    r1 = Record(amount=145, comment='Безудержный шопинг')
    r2 = Record(amount=1568,
                comment='Наполнение потребительской корзины',
                date='09.03.2019')
    r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

    # для CaloriesCalculator
    r4 = Record(amount=1186,
                comment='Кусок тортика. И ещё один.',
                date='24.02.2019')
    r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
    r6 = Record(amount=2500, comment='Баночка чипсов.')

    cash_calc = CashCalculator(1000)

    cash_calc.add_record(r1)
    cash_calc.add_record(r2)
    cash_calc.add_record(r3)

    print(cash_calc.get_today_cash_remained('rub'))
    print(cash_calc.get_today_cash_remained('usd'))
    print(cash_calc.get_today_cash_remained('eur'))
    print(cash_calc.get_week_stats())

    calory_calc = CaloriesCalculator(2500)
    calory_calc.add_record(r4)
    calory_calc.add_record(r5)
    calory_calc.add_record(r6)

    print(calory_calc.get_calories_remained())
