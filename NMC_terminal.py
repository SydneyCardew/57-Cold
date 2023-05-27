from NMC_mainframe import NMC
from NMC_mainframe import game_read
from import_export import code_list
import time


def main():
    print("NATIONAL MANAGEMENT COMPUTER\nCHOOSE SESSION TO IMPORT\nAVAILABLE SESSIONS:")
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
            if sub_command[0] == "LOAD":
                print(output[0])
                loading_bar(int(sub_command[1]))
        elif len(output) == 1:
            print(output[0])


def loading_bar(length):
    for bar in range(length):
        print("|", end='', flush=True)
        time.sleep(0.07)
    print("\n", end='')


if __name__ == '__main__':
    main()
