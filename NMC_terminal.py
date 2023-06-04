from NMC_mainframe import NMC
from NMC_mainframe import game_read
from NMC_mainframe import NMC_date
from import_export import code_list
import string_dicts as sd
import time


def main():
    salutatation_time = sd.local_time_of_day_greeting()
    print(f"NATIONAL MANAGEMENT COMPUTER\n"
          f"----------------------------------------")
    loading_bar(40, False, True)
    print(f"----------------------------------------\n"
          f"GOOD {salutatation_time}, TECHNICIAN\n\n"
          f"CHOOSE SESSION TO IMPORT\n"
          f"AVAILABLE SESSIONS:")
    print(code_list())
    loaded = False
    NMC_on = True
    while NMC_on:
        command = input(">: ")
        output = NMC(command.upper(), loaded)
        if output[0] == "LOADED":
            loaded = True
            print(f"SESSION {command} SUCCESSFULLY LOADED\n{game_read()}")
        elif output[0] == "QUIT":
            NMC_on = False
        elif len(output) > 1:
            sub_command = output[1].split()
            if sub_command[0] == "LOAD+":
                print(output[0])
                loading_bar(int(sub_command[1]), True)
        elif len(output) == 1:
            print(output[0])


def loading_bar(length, date_after=False, fast=False):
    for bar in range(length):
        print("|", end='', flush=True)
        time.sleep(0.07 if not fast else 0.02)
    print("\n", end='')
    if date_after:
        print(NMC_date()[0])


if __name__ == '__main__':
    main()
