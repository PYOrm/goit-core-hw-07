# У межах вашої організації, ви відповідаєте за організацію привітань колег з днем народження. 
# Щоб оптимізувати цей процес, вам потрібно створити функцію get_upcoming_birthdays, 
# яка допоможе вам визначати, кого з колег потрібно привітати.

# У вашому розпорядженні є список users, 
# кожен елемент якого містить інформацію про ім'я користувача та його день народження. 
# Оскільки дні народження колег можуть припадати на вихідні, 
# ваша функція також повинна враховувати це та переносити дату привітання на наступний робочий день, якщо необхідно.

# Вимоги до завдання:
# 1.Параметр функції users - це список словників, 
# де кожен словник містить ключі name (ім'я користувача, рядок) та birthday (день народження, рядок у форматі 'рік.місяць.дата').
# 2.Функція має визначати, чиї дні народження випадають вперед на 7 днів включаючи поточний день. 
# Якщо день народження припадає на вихідний, дата привітання переноситься на наступний понеділок.
# 3.Функція повертає список словників, де кожен словник містить інформацію про користувача 
# (ключ name) та дату привітання (ключ congratulation_date, дані якого у форматі рядка 'рік.місяць.дата').

import datetime

def get_upcoming_birthdays(users:list) -> list:
    nearest_birthdays = []                          # create empty list for result
    today = datetime.datetime.today().date()        # get current date
    for user in users:                              # iterate by list of dictionarys
        if isinstance(user,dict):                   # check if record is dictionary 
            birthday = user.get("birthday")         # get string with birthday value  
            birthday_date = datetime.datetime.strptime(birthday,"%Y.%m.%d").date()  # convert string to datetime and get date
            birthday_date_in_year = datetime.date.replace(birthday_date, year=today.year) # change year for current 

            if 0 > (birthday_date_in_year - today).days:    # check if birthday already gone in this year 
                birthday_date_in_year = datetime.date.replace(birthday_date, year=today.year + 1) #update date for next year
                
            if (birthday_date_in_year - today).days <= 7:   # check if birthday in nearest 7 day.
                greeting_day = birthday_date_in_year + datetime.timedelta(days=float([0,0,0,0,0,2,1][birthday_date_in_year.weekday()]))  # if birthday in weekend set greeting to next work day
                nearest_birthdays.append({"name":user.get("name"), "congratulation_date":datetime.datetime.strftime(greeting_day,"%Y.%m.%d")}) # include record in result in required format
    return nearest_birthdays
