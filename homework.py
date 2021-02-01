import datetime as dt

date_format = '%d.%m.%Y'
today_day = dt.datetime.now().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        sum = 0
        for rec in self.records:
            if rec.date == today_day:
                sum += rec.amount
        return sum

    def get_week_stats(self):
        period = dt.timedelta(days=7)
        seven_period = today_day - period
        sum = 0
        for rec in self.records:
            if seven_period < rec.date <= today_day:
                sum += rec.amount
        return sum

    # def show_rec(self):
    #     for record in self.records:
    #         record.show()
    #     print(self.records)


class Record:
    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        if type(date) == dt.date:
            self.date = date
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 92.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        cur_rate_dict = {
            'rub': ['руб', CashCalculator.RUB_RATE],
            'usd': ['USD', CashCalculator.USD_RATE],
            'eur': ['Euro', CashCalculator.EURO_RATE]
        }
        spent_today = self.get_today_stats()
        result = (self.limit - spent_today) / cur_rate_dict[currency][1]
        result_fl = float("{:.2f}".format(result))
        debt = (spent_today - self.limit) / cur_rate_dict[currency][1]
        debt_fl = float("{:.2f}".format(debt))
        if result > 0:
            return (f"На сегодня осталось {result_fl} "
                    f"{cur_rate_dict[currency][0]}")
        elif result == 0:
            return "Денег нет, держись"
        else:
            return (f"Денег нет, держись: твой долг - "
                    f"{debt_fl} {cur_rate_dict[currency][0]}")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        consumed_today = self.get_today_stats()
        result = self.limit - consumed_today
        if result > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {result} кКал")
        else:
            return "Хватит есть!"


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
