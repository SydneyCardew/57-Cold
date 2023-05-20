def NMC(input):
    match input.split():
        case ['action', *act_args]:
            return NMC_action(act_args)
        case _:
            return "INVALID INPUT"





def NMC_action(args):
    secret = False
    in_domain = True
    if not args[0].isdigit():
        return error_handler(1)
    else:
        if int(args[0]) <= -1 or int(args[0]) >= 11:
            return error_handler(2)
        else:
            if not args[1].isdigit():
                return error_handler(3)
            else:
                if "--xd" in args:
                    in_domain = False
                if "--s" in args:
                    secret = True





def error_handler(code):
    match code:
        case 1:
            return "ERROR: INVALID DIFFICULTY (NON-NUMERIC)"
        case 2:
            return "ERROR: INVALID DIFFICULTY (OUT OF RANGE)"
        case 3:
            return "ERROR: INVALID COST (NON-NUMERIC)"
