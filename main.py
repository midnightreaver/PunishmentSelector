#!/usr/bin/env python
"""Manage and select random user-generated punishments

PunishGen uses a text file of user-generated, level-based punishments.
PunishGen features listing, addition and removal of punishments as
well as a selected level-based punishment selector.
"""

import sys
from os.path import exists
from os import system, name
import re
import random
from time import sleep

__author__ = "MidnightReaver"
__copyright__ = "Copyright 2023, MidnightReaver"
__license__ = "MIT License"
__version__ = "1.0"

punishments_filename = "punishments.txt"


def list_file_exists():
    file_exists = exists(punishments_filename)

    if file_exists:
        return True
    else:
        return False


def exit_generator():
    sys.exit("Exiting Random Punishment Generator!")


def banner():
    print("""
___  ____     _       _       _     _  ______                          _                        
|  \/  (_)   | |     (_)     | |   | | | ___ \                        ( )                       
| .  . |_  __| |_ __  _  __ _| |__ | |_| |_/ /___  __ ___   _____ _ __|/ ___                    
| |\/| | |/ _` | '_ \| |/ _` | '_ \| __|    // _ \/ _` \ \ / / _ \ '__| / __|                   
| |  | | | (_| | | | | | (_| | | | | |_| |\ \  __/ (_| |\ V /  __/ |    \__ \                   
\_|  |_/_|\__,_|_| |_|_|\__, |_| |_|\__\_| \_\___|\__,_| \_/ \___|_|    |___/                   
                     __/ |                                                                  
                    |___/                                                                   
______                _                  ______            _     _                          _   
| ___ \              | |                 | ___ \          (_)   | |                        | |  
| |_/ /__ _ _ __   __| | ___  _ __ ___   | |_/ /   _ _ __  _ ___| |__  _ __ ___   ___ _ __ | |_ 
|    // _` | '_ \ / _` |/ _ \| '_ ` _ \  |  __/ | | | '_ \| / __| '_ \| '_ ` _ \ / _ \ '_ \| __|
| |\ \ (_| | | | | (_| | (_) | | | | | | | |  | |_| | | | | \__ \ | | | | | | | |  __/ | | | |_ 
\_| \_\__,_|_| |_|\__,_|\___/|_| |_| |_| \_|   \__,_|_| |_|_|___/_| |_|_| |_| |_|\___|_| |_|\__|


_____                           _                                                              
|  __ \                         | |                                                             
| |  \/ ___ _ __   ___ _ __ __ _| |_ ___  _ __                                                  
| | __ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|                                                 
| |_\ \  __/ | | |  __/ | | (_| | || (_) | |                                                    
\____/\___|_| |_|\___|_|  \__,_|\__\___/|_|                                                    


    """)


def list_punishments():

    punishments_level = []  # begin with empty list
    punishments_content = []  # begin with empty list

    with open(punishments_filename, 'r') as punishment_file:
        lines = punishment_file.readlines()
        count = 1

        print("\n")  # extra spacing between lines
        for line in lines:
            match_level = re.search("(^\d.*\,)", line)  # extract punishment level
            match_level = match_level.group()
            punishment_level = match_level[:-1]  # strip off trailing comma
            match_text = re.search("([^\d.*\,].*)", line)  # extract punishment text
            match_text = match_text.group()
            punishment_text = match_text
            punishments_level.append(punishment_level)  # append level to array
            punishments_content.append(punishment_text)  # append line content to array

    # zip both arrays in order to sort by level
    zip_punishments = zip(punishments_level, punishments_content)
    zip_list = list(zip_punishments)
    sorted_punishments = sorted(zip_list, key=lambda x: x[0])

    # iterate through sorted
    for punishment in sorted_punishments:
        (level, text) = punishment
        print(f"Level {level}: {text}")


# clears the screen after a short delay
# https://www.geeksforgeeks.org/clear-screen-python/
def clear():

    # sleep for 2 seconds before clearing
    sleep(1)

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux (here, os.name is 'posix')
    else:
        _ = system('clear')


class PunishGen:

    file_is_open = False

    def __init__(self):
        banner()

        existing_list = list_file_exists()

        if existing_list:  # continue to main menu
            self.main_menu()
        else:  # continue to instructions for creating list
            self.init_punishment_list()

    def init_punishment_list(self):

        with open(punishments_filename, 'w+') as punishment_file:
            self.file_is_open = True
            first_punishment = input("Type the first punishment then press Enter: ")
            punishment_file.write(f"1,{first_punishment}\n")
        punishment_file.close()

        add_another_choice = input("Would you like to add another punishment or go to main menu? (a/m): ")

        clear()

        if add_another_choice.lower() == "m":
            self.main_menu()
        elif add_another_choice.lower() == "a":
            self.add_punishment()
        else:
            print("Please enter valid input only!")
            self.main_menu()

    def add_punishment(self):

        punishment_input = ""

        while punishment_input != "q":

            punishment_input = input("Add a punishment or return to main menu (a/q)?: ")
            clear()
            if punishment_input == "a":
                punishment_file = open(punishments_filename, 'a')
                add_punishment = input("Type the next punishment then press Enter: ")
                add_punishment_level = int(input("What level should this be (please enter numbers greater "
                                                 "than zero only)?: "))
                punishment_file.write(f"{add_punishment_level},{add_punishment}\n")
                punishment_file.close()
            elif punishment_input == "q":
                break
            else:
                print("Please choose a valid option!")
                self.add_punishment()

        self.main_menu()

    def main_menu(self):
        print("""
        1) Select Random Punishment
        2) Manage Punishments
        3) Quit
        """)
        choice = int(input("Select an option: "))

        valid_options = [1, 2, 3]

        while choice not in valid_options:
            print("Please select a valid option!")
            self.main_menu()

        if choice == 1:  # generate punishment
            clear()
            self.get_random_punishment()
        elif choice == 2:  # manage punishment file (add, update, delete)
            clear()
            self.manage_punishments()
        elif choice == 3:
            clear()
            exit_generator()

    def get_random_punishment(self):
        punishments_level = []  # begin with empty list
        punishments_content = []  # begin with empty list

        count_punishment_levels = 0
        levels_of_punishment = []

        with open(punishments_filename, 'r') as punishment_file:
            lines = punishment_file.readlines()
            count = 1

            print("\n")  # extra spacing between lines
            for line in lines:
                match_level = re.search("(^\d.*\,)", line)  # extract punishment level
                match_level = match_level.group()
                punishment_level = match_level[:-1]  # strip off trailing comma
                match_text = re.search("([^\d.*\,].*)", line)  # extract punishment text
                match_text = match_text.group()
                punishment_text = match_text
                punishments_level.append(punishment_level)  # append level to array
                punishments_content.append(punishment_text)  # append line content to array

                if punishment_level not in levels_of_punishment:
                    levels_of_punishment.append(punishment_level)
                    count_punishment_levels += 1

        # zip both arrays in order to sort by level
        zip_punishments = zip(punishments_level, punishments_content)
        zip_list = list(zip_punishments)
        sorted_punishments = sorted(zip_list, key=lambda x: x[0])

        select_levels = []
        select_puntext = []

        # iterate through sorted
        for punishment in sorted_punishments:
            (level, text) = punishment

            select_levels.append(level)
            select_puntext.append(text)

        unique_levels = []
        for lvl in select_levels:
            if lvl not in unique_levels:
                unique_levels.append(lvl)

        level_string = "( "

        for z in unique_levels:
            level_string += f"{z} "

        level_string += ")"
        clear()
        selected_level = input(f"Select your desired punishment level {level_string}: ")

        punishment_choices = []
        if selected_level not in select_levels:
            self.get_random_punishment()
        else:
            for lv in range(len(select_levels)):
                if select_levels[lv] == selected_level:
                    punishment_choices.append(select_puntext[lv])

        print("\n\nThe selected punishment is:\n\n"+ random.choice(punishment_choices))

    def manage_punishments(self):
        print("""
        1) List punishments
        2) Add punishment
        3) Delete punishment
        4) Back to Main Menu
        """)
        choice = int(input("Select an option: "))

        valid_options = [1, 2, 3, 4]

        while choice not in valid_options:
            print("Please select a valid option!")
            self.manage_punishments()

        if choice == 1:  # list punishments
            clear()
            list_punishments()
        elif choice == 2:  # add punishment
            clear()
            self.add_punishment()
        elif choice == 3:  # delete punishment
            clear()
            self.delete_punishment()
        elif choice == 4:  # go to main menu
            clear()
            self.main_menu()

    def delete_punishment(self):
        punishments_level = []  # begin with empty list
        punishments_content = []  # begin with empty list

        sorted_punishment_levels = []  # sorted list of above
        sorted_punishment_contents = []  # sorted list of above

        punish_dict = {}  # to hold final sorted dict
        clear()
        with open(punishments_filename, 'r') as punishment_file:
            lines = punishment_file.readlines()

            print("\n")  # extra spacing between lines
            for line in lines:
                match_level = re.search("(^\d.*\,)", line)  # extract punishment level
                match_level = match_level.group()
                punishment_level = match_level[:-1]  # strip off trailing comma
                match_text = re.search("([^\d.*\,].*)", line)  # extract punishment text
                match_text = match_text.group()
                punishment_text = match_text
                punishments_level.append(punishment_level)  # append level to array
                punishments_content.append(punishment_text)  # append line content to array

        # zip both arrays in order to sort by level
        zip_punishments = zip(punishments_level, punishments_content)
        zip_list = list(zip_punishments)
        sorted_punishments = sorted(zip_list, key=lambda x: x[0])

        count = 1

        # iterate through sorted
        for punishment in sorted_punishments:
            (level, text) = punishment
            sorted_punishment_levels.append(level)
            sorted_punishment_contents.append(text)
            punish_dict[count] = f"{text} (Level {level})"
            print(f"{count}) {text} (Level {level})")
            print("-" * 50)
            count += 1
        print(f"punish_dict count is: {len(punish_dict)}")

        to_delete = input("Select a number to delete or 'q' to return to the main menu: ")
        print(f"to_delete is: {to_delete}")

        if to_delete.isnumeric():
            removed = punish_dict.pop(int(to_delete))
            with open(punishments_filename, 'w') as punishment_file:
                index = 0
                for record in range(len(punish_dict)):
                    if index != removed:
                        try:
                            punishment_file.write(f"{sorted_punishment_levels[index]},{sorted_punishment_contents[index]}\n")
                        except KeyError:
                            print("Error! Invalid selection!")
                            self.delete_punishment()
                    index += 1
            clear()
            self.delete_punishment()
        elif to_delete == 'q':
            clear()
            self.main_menu()
        else:
            print("Please make a valid selection!")
            clear()
            self.delete_punishment()


if __name__ == "__main__":
    PunishGen()
