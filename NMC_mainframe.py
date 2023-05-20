from import_export import importer


def NMC(input, loaded):
    if not loaded:
        global game
        game = importer(input)
        return error_handler(0) if not game else "LOADED"
    else:
        match input.split():
            case ['ACTION', *act_args]:
                return NMC_action(act_args)
            case _:
                return "INVALID INPUT"


def game_read():
    return f"{len(game.reg_dict.keys())} REGIONS, {len(game.min_dict)} MINISTERS, " \
           f"{len(game.dept_dict.keys())} DEPARTMENTS SUCCESSFULLY IMPORTED"


def NMC_action(args):
    secret = False
    in_domain = True
    if len(args) < 3:
        return error_handler(5)
    else:
        department = args[0]
        difficulty = args[1]
        cost = args[2]
        if department not in game.dept_dict.keys():
            return error_handler(1)
        else:
            if not difficulty.isdigit():
                return error_handler(2)
            else:
                if int(difficulty) <= -1 or int(difficulty) >= 11:
                    return error_handler(3)
                else:
                    if not cost.isdigit():
                        return error_handler(4)
                    else:
                        if "--XD" in args:
                            in_domain = False
                        if "--S" in args:
                            secret = True
                        result = game.dept_dict[department].action(int(difficulty), int(cost), secret, in_domain)
                        return f"{'PRESS RELEASE' if not secret else 'CONFIDENTIAL MEMO'}: {result.a_string}"


def error_handler(code):
    match code:
        case 0:
            return "ERROR: INVALID SESSION ID"
        case 1:
            return "ERROR: INVALID MINISTRY ID"
        case 2:
            return "ERROR: INVALID DIFFICULTY (NON-NUMERIC)"
        case 3:
            return "ERROR: INVALID DIFFICULTY (OUT OF RANGE)"
        case 4:
            return "ERROR: INVALID COST (NON-NUMERIC)"
        case 5:
            return "ERROR: NOT ALL ARGUMENTS PRESENT"
