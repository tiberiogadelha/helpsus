from datetime import date

def calculate_age(birth_date):
    today = date.today()
    diff_in_days = today - birth_date
    DAYS_IN_YEAR = 365
    age = diff_in_days.days/DAYS_IN_YEAR
    return int(age)
