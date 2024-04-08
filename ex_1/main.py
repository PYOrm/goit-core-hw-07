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
            except ValueError:
                return "Wrong command format"
            except IndexError:
                return "Contact not exist" 
        return inner                                        #return inner function

    @input_error                                            #use decorator
    def add_contact(data:list, book:AddressBook) -> str:                      #define function for add contact
        name, number, _ = data                                 #unpack data
        recordName = book.find(name)
        if recordName is None:
            
            book.add_record(Record(name))
            book[name] = number                           #add record to dictionary
        return "Record added."                              #return confirm 

    @input_error                                            #use decorator
    def change_contact(data:list) -> str:                   #define function for change contact
        name, number = data                                 #unpack data
        if not phone_book.get(name):                        #if record not exist 
            raise IndexError()                              #rise exception
        phone_book[name] = number                           #update dictionary
        return "Contact updated"                            #return confirm 

    @input_error                                            #use decorator
    def show_phone(data:list) ->str:                        #define function for show number
        name, *_ = data                                     #unpack data
        return phone_book[name]                             #try return phone by given name

    def show_all():                                         #define function for show all phone book
        res = ""
        for name, phone in phone_book.items():              #each record display
            res += f"{name:<30}{phone:>15}\n"               #with format 
        return res.removesuffix("\n")

    @input_error                                            #use decorator
    def parse_input(user_input:str) -> list:                #define function to parse command
        user_input = user_input.lower().strip().split()     #split input string by " "
        return (user_input.pop(0), user_input)              #return command and left data

    @input_error
    def add_birthday(args, book):
        # реалізація

    @input_error
    def show_birthday(args, book):
        # реалізація

    @input_error
    def birthdays(args, book):
        # реалізація

    def main():                                             #define main function
        print("Welcome to the assistant bot!")              #greeting
        while True:                                         #start unlimit cycle
            get_command, data = parse_input(input("Enter a command: ")) #parse data from user
            match get_command:                              #select action for entered command
                case ("exit"|"close"):                      #terminate cycle 
                    print("Good bye!")
                    break
                case ("hello"):                             #communicate with user
                    print("How can I help you?")
                case ("add", phone_book):                               #add contact
                    print(add_contact(data))
                case ("change", phone_book):                            #change contact
                    print(change_contact(data))
                case ("phone", phone_book):                             #show phone by name
                    print(show_phone(data))
                case ("all", phone_book):                               #show all phone book
                    print(show_all())
                case ("add-birthday", phone_book):                      #add birthday
                    print(show_all())
                case ("show-birthday", phone_book):                     #show birthday
                    print(show_all())
                case ("birthdays", phone_book):                         #show nearest birthdays 
                    print(show_all())
                case (_):                                   #unknown command
                    print("Invalid command")

if __name__ == "__main__":
    main()