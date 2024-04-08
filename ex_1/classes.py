# Розробіть систему для управління адресною книгою.

# Сутності:
# Field: Базовий клас для полів запису.
# Name: Клас для зберігання імені контакту. Обов'язкове поле.
# Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# AddressBook: Клас для зберігання та управління записами.

# Функціональність:
# AddressBook:Додавання записів.
# Пошук записів за іменем.
# Видалення записів за іменем.
# Record:Додавання телефонів.
# Видалення телефонів.
# Редагування телефонів.
# Пошук телефону.

from collections import UserDict
from typing import Any
from datetime import datetime, date


class Field():
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name:str):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone:str):
        if not self.is_valid(phone):
           raise ValueError
        super().__init__(phone) 

    def is_valid(self, phone):
        return len(phone)==10 and str(phone).isdigit()

class Birthday(Field):
    def __init__(self, birthday:str):
        try:
            bday = datetime.strptime(birthday, "DD.MM.YYYY")
            super().__init__(bday)
        except Exception:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        
class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.items = []
        self.birthday = None
    
    def add_phone(self, phone):
        ph = Phone(phone)
        self.items.append(ph)
        return ph

    def find_phone(self, phone):
        return list(filter(lambda x:x.value == phone, self.items))[0]

    def remove_phone(self, phone):
        ph = self.find_phone(phone)
        if ph:
            self.items.remove(ph)
        return ph
    
    def edit_phone(self, old_phone, new_phone):                     
        if len(self.find_phone(old_phone))==0:
            raise ValueError
        self.add_phone(new_phone)
        self.remove_phone(old_phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.items)}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
    
    def add_record(self, record:Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return {key:val for key,val in self.data.items() if key == name}.get(name)

    def delete(self, name):
        return self.data.pop(name, None)
    
    def get_upcoming_birthdays(self) -> list:
        nearest_birthdays = []                          
        today = datetime.datetime.today().date()        
        for key,val in self.data.items():               
            if isinstance(val, Record):                   
                birthday = val.birthday.value           
                #birthday_date = datetime.datetime.strptime(birthday,"%Y.%m.%d").date()  # convert string to datetime and get date
                birthday_date_in_year = datetime.date.replace(birthday, year=today.year) 

                if 0 > (birthday_date_in_year - today).days:    
                    birthday_date_in_year = datetime.date.replace(birthday, year=today.year + 1) 
                    
                if (birthday_date_in_year - today).days <= 7:   
                    greeting_day = birthday_date_in_year + datetime.timedelta(days=float([0,0,0,0,0,2,1][birthday_date_in_year.weekday()]))  
                    nearest_birthdays.append({"name":val.name.value, "congratulation_date":datetime.datetime.strftime(greeting_day,"%Y.%m.%d")}) 
        return nearest_birthdays
    
