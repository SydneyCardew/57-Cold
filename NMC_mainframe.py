from import_export import importer
from error_handler import error_handler
from project_generator import generate_project_cards


def NMC(input, loaded):
    if not loaded:
        global game
        game = importer(input)
        return error_handler(0) if not game else ["LOADED"]
    else:
        match input.split():
            case ['ACTION' | 'ACT', *act_args]:
                return NMC_action(act_args)
            case ['ADVANCE' | 'ADV', *day_args]:
                return NMC_advance(day_args)
            case ['DATE' | 'DAT']:
                return NMC_date()
            case ['POLL']:
                return NMC_poll()
            case ['PROJECT' | 'PROJ']:
                return NMC_projects()
            case ['REACT', *react_args]:
                return NMC_react(react_args)
            case _:
                return ["INVALID INPUT"]


def NMC_action(args):
    """the ACTION keyword"""
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
                        return [f"{'PRESS RELEASE' if not secret else 'CONFIDENTIAL MEMO'}: {result.a_string}"]


def NMC_advance(args):
    if len(args) > 1:
        return error_handler(6)
    else:
        days = args[0]
        if not days.isdigit():
            return error_handler(7)
        else:
            days = int(days)
            date = NMC_date()[0]
            for day in range(days):
                game.tick()
            return [f"{date}\nADVANCING {days} DAYS", f"LOAD {days}"]


def NMC_date():
    time = game.world.clock.time
    return [f"CURRENT DATE: {time.date} {time.month['code']} {time.year}"]


def NMC_poll():
    return [game.poll()]


def NMC_projects():
    issue = game.computer.secret_project_counter
    generate_project_cards(issue)
    game.computer.secret_project_counter += 1
    return [f"GENERATED SECRET PROJECTS CARDS, ISSUE {issue}"]


def NMC_react(args):
    if len(args) < 2:
        return(error_handler(5))
    else:
        paper = args[0]
        approval = args[1]
        if paper not in game.press_dict.keys():
            return(error_handler(8))
        else:
            if approval not in ('Y', 'N'):
                return(error_handler(9))
            else:
                paper_obj = game.press_dict[paper]
                approval_bool = True if approval == 'Y' else False
                result = game.uk.political_drift(paper_obj, approval_bool)
                return [f"REPORT: {result.r_string}"]


def game_read():
    return f"{len(game.reg_dict.keys())} REGIONS, {len(game.min_dict)} MINISTERS, " \
           f"{len(game.dept_dict.keys())} DEPARTMENTS SUCCESSFULLY IMPORTED"


