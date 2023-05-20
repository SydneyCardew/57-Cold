from NMC_mainframe import NMC
from NMC_mainframe import game_read
from import_export import code_list


def main():
    print("NATIONAL MANAGEMENT COMPUTER\nCHOOSE SESSION TO IMPORT\nAVAILABLE SESSIONS:")
    print(code_list())
    loaded = False
    NMC_on = True
    while NMC_on:
        command = input(">: ")
        output = NMC(command.upper(), loaded)
        if output == "LOADED":
            loaded = True
            print(f"SESSION {command} SUCCESSFULLY LOADED\n{game_read()}")
        elif output == "QUIT":
            NMC_on = False
        else:
            print(output)


if __name__ == '__main__':
    main()
