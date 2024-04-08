from typing import Callable
from classes import *

def main():

    phone_book = AddressBook()

    def input_error(func:Callable):                         #define decorator
        def inner(*args,**kwargs):                          #inner function wich catch exceprions
            try:                                            #try execute decorated function
                return func(*args,**kwargs)                 #return result of execution
            except KeyError:                                
                return "Invalid command"
            except ValueError as err:
                return err.args[0]
            except IndexError:
                return "Contact not exist" 
        return inner                                        #return inner function

    @input_error                                            #use decorator
    def add_contact(data:list) -> str:                      #define function for add contact
        name, number = data                                 #unpack data
        record_name = phone_book.find(name)
        msg = "Record updated."
        if record_name is None:
            record_name = Record(name)
            record_name.add_phone(number)                           #add record to dictionary
            msg = "Record added."
        else:
            record_name.add_phone(number)
        phone_book.add_record(record_name)
        return msg                              #return confirm 

    @input_error                                            #use decorator
    def change_contact(data:list) -> str:                   #define function for change contact
        name, old_number, new_number = data                                 #unpack data
        record = phone_book.get(name)
        if not record:                        #if record not exist 
            raise IndexError()                              #rise exception
        record.edit_phone(old_number, new_number)
        phone_book[name] = record                           #update dictionary
        return "Contact updated"                            #return confirm 

    @input_error                                            #use decorator
    def show_phone(data:list) ->str:                        #define function for show number
        name, *_ = data                                     #unpack data
        return str(phone_book[name])                            #try return phone by given name

    def show_all():                                         #define function for show all phone book
        res = ""
        for name, record in phone_book.items():              #each record display
            res += str(record) + "\n"               #with format 
        return res.removesuffix("\n")

    @input_error                                            #use decorator
    def parse_input(user_input:str) -> list:                #define function to parse command
        user_input = user_input.lower().strip().split()     #split input string by " "
        return (user_input.pop(0), user_input)              #return command and left data

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
                                                 #define main function
    print("Welcome to the assistant bot!")              #greeting
    while True:                                         #start unlimit cycle
        get_command, data = parse_input(input("Enter a command: ")) #parse data from user
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