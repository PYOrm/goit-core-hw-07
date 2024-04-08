from typing import Callable
from classes import *

def main():

    phone_book = AddressBook()

    def input_error(func:Callable):                         
        def inner(*args,**kwargs):                          
            try:                                            
                return func(*args,**kwargs)                 
            except KeyError:                                
                return "Invalid command"
            except ValueError as err:
                return err.args[0]
            except IndexError:
                return "Contact not exist" 
        return inner                                        

    @input_error                                            
    def add_contact(data:list) -> str:                      
        name, number = data                                 
        record_name = phone_book.find(name)
        msg = "Record updated."
        if record_name is None:
            record_name = Record(name)
            record_name.add_phone(number)                           
            msg = "Record added."
        else:
            record_name.add_phone(number)
        phone_book.add_record(record_name)
        return msg                             

    @input_error                                            
    def change_contact(data:list) -> str:                   
        name, old_number, new_number = data                                 
        record = phone_book.get(name)
        if not record:                         
            raise IndexError()                              
        record.edit_phone(old_number, new_number)
        phone_book[name] = record                           
        return "Contact updated"                             

    @input_error                                           
    def show_phone(data:list) ->str:                        
        name, *_ = data                                     
        return str(phone_book[name])                        

    def show_all():                                         
        res = ""
        for name, record in phone_book.items():              
            res += str(record) + "\n"                         
        return res.removesuffix("\n")

    @input_error                                            
    def parse_input(user_input:str) -> list:                
        user_input = user_input.lower().strip().split()     
        return (user_input.pop(0), user_input)              

    @input_error
    def add_birthday(args) -> str:
        name, birthday = args
        record = phone_book[name]
        record.add_birthday(birthday)
        phone_book[name] = record
        return "Birthday set."
    
    @input_error
    def show_birthday(args):
        name, *_ = args
        record = phone_book[name]
        return str(record.birthday)

    @input_error
    def birthdays():
        return phone_book.get_upcoming_birthdays()

    print("Welcome to the assistant bot!")              #greeting
    while True:                                         #start unlimit cycle
        get_command, data = parse_input(input("Enter a command: ")) 
        match get_command:                              #select action for entered command
            case ("exit"|"close"):                      #terminate cycle 
                print("Good bye!")
                break
            case ("hello"):                             #communicate with user
                print("How can I help you?")
            case ("add"):                               #add contact
                print(add_contact(data))
            case ("change"):                            #change contact
                print(change_contact(data))
            case ("phone"):                             #show phone by name
                print(show_phone(data))
            case ("all"):                               #show all phone book
                print(show_all())
            case ("add-birthday"):                      #add birthday
                print(add_birthday(data))
            case ("show-birthday"):                     #show birthday
                print(show_birthday(data))
            case ("birthdays"):                         #show nearest birthdays 
                print(birthdays())
            case (_):                                   #unknown command
                print("Invalid command")

if __name__ == "__main__":
    main()