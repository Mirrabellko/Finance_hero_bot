from datetime import date

def count_period():
    today = date.today()
    
    new_month = today.month
    new_year = today.year
    
    new_month = new_month + 1

    if new_month == 13:
        new_month = new_month - 12
        new_year += 1

    data = today.replace(year=new_year, month=new_month)
    return data



print(count_period())