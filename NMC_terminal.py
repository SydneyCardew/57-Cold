from NMC_parser import NMC
from import_export import importer
from import_export import code_list


def main():
    print("NATIONAL MANAGEMENT COMPUTER\nCHOOSE SESSION TO IMPORT\nAVAILABLE SESSIONS:")
    print(code_list())
    loaded = False
    NMC_on = True
    while NMC_on:
        command = input(">: ")
        if loaded:
            output = NMC(command.lower())
        else:
            output = importer(command.lower())
        if output == "LOADED":
            loaded = True
            print(f"SESSION {command.lower()} SUCCESSFULLY LOADED")
        elif output == "QUIT":
            NMC_on = False
        else:
            print(output)


if __name__ == '__main__':
    main()
