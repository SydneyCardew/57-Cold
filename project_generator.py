import json
from random import seed, shuffle, randint, choice
import string

seed()
with open(".\\data\\operation_names.json") as name_file:
    data = json.load(name_file)
    first, second = data['first part'], data['second part']
    black_list = []
    for x in range(100):
        op_list = []
        first_local, second_local = first.copy(), second.copy()
        for y in range(6):
            shuffle(first_local)
            shuffle(second_local)
            check_switch = True
            while check_switch:
                project_name = (f"PROJECT+"
                                f"{first_local.pop(0).upper()}"
                                f"+{second_local.pop(0).upper()}")
                if project_name not in black_list:
                    black_list.append((project_name))
                    op_list.append(project_name)
                    check_switch = False
        card_number = str(x).zfill(3)
        with open(f".\\experiments\projects-{card_number}.txt", "w") as card_file:
            card_file.write(f"+NATIONAL+MANAGEMENT+COMPUTER+++++++++++\n"
                            f"[1957 PROJ CODES ISS. 01]+[GROUP {card_number}]+++\n"
                            f"----------------------------------------\n")
            for item in op_list:
                card_file.write(f"..*{item}{'.'* (40 - (len(item) + 3))}\n")
            card_file.write(f"----------------------------------------\n")
            code_string = ''
            punctmarks = '!?.+-=#~;:'
            alphabet = string.ascii_uppercase
            for char in range(40):
                dice_roll = randint(1, 5)
                if dice_roll <= 1:
                    code_string += choice(punctmarks)
                elif dice_roll >= 2 and dice_roll <= 3:
                    code_string += choice(alphabet)
                elif dice_roll >= 4:
                    code_string += str(randint(0, 9))
            card_file.write(code_string)



