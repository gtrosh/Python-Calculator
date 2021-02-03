import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.now().date()
        return sum(rec.amount for rec in self.records if rec.date == today)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        date_week_ago = today - dt.timedelta(days=7)
        # (sum(rec.amount for rec in self.records if date_week_ago
        #      < rec.date <= today))
        return sum(rec.amount for rec in self.records if date_week_ago
                   < rec.date <= today)


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 92.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        cur_rate_dict = {
            'cur_dict': {
                'rub': 'руб',
                'usd': 'USD',
                'eur': 'Euro'
            },
            'rate_dict': {
                'rub': self.RUB_RATE,
                'usd': self.USD_RATE,
                'eur': self.EURO_RATE
            }
        }
        spent_today = self.get_today_stats()
        currency_left = round((self.limit - spent_today) / cur_rate_dict[
            'rate_dict'][currency], 2)
        if currency_left > 0:
            return (f"На сегодня осталось {currency_left} "
                    f"{cur_rate_dict['cur_dict'][currency]}")
        elif currency_left == 0:
            return "Денег нет, держись"
        else:
            return (f"Денег нет, держись: твой долг - "
                    f"{abs(currency_left)} "
                    f"{cur_rate_dict['cur_dict'][currency]}")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        consumed_today = self.get_today_stats()
        currency_remained = self.limit - consumed_today
        if currency_remained > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {currency_remained} кКал")
        else:
            return "Хватит есть!"


if __name__ == '__main__':
    c1 = Calculator(1000)
    c2 = CashCalculator(5000)
    c3 = CaloriesCalculator(2800)
    r1 = Record(amount=120, comment="бла-бла")
    r2 = Record(amount=50, comment="тратим")
    r3 = Record(amount=700, comment="тратим", date="27.01.2021")
    r4 = Record(amount=2500,
                comment='Кусок тортика. И ещё один.')
    r5 = Record(amount=84, comment='Йогурт.', date='23.02.2019')
    r6 = Record(amount=1140, comment='Баночка чипсов.', date='24.02.2019')

    c1.add_record(r1)
    c1.add_record(r2)
    c1.add_record(r3)

    c2.add_record(r1)
    c2.add_record(r2)
    c2.add_record(r3)

    c1.get_today_stats()
    c1.get_week_stats()
    c3.add_record(r4)
    c3.add_record(r5)
    c3.add_record(r6)

    print(c2.get_today_cash_remained('eur'))
    print(c3.get_calories_remained())
