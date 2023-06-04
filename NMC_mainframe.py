from import_export import importer
from error_handler import error_handler
from project_generator import generate_project_cards
import re

hr = "----------------------------------------"


def NMC(input, loaded):
    """
    This is the main parser for command inputs
    """
    if not loaded:
        # special case where no game is loaded
        global game
        game = importer(input)
        return error_handler(0) if not game else ["LOADED"]
    else:
        # This section handles various commands which contain strings in quotations as arguments
        if len(input.split()) > 0:
            in_args = " ".join(input.split()[1:])
            in_key = input.split()[0]
            in_match = re.match(r'(\S+)\s+(\".*?\")\s+(.*)', in_args)
            if in_match:
                command = [in_key] + in_match.group(1).split() + [in_match.group(2)] + in_match.group(3).split()
            else:
                command = input.split()
        else:
            command = input.split()
        # main pattern matching
        match command:
            case ['ACTION' | 'ACT', *act_args]:
                return NMC_action(command[1:])
            case ['ADVANCE' | 'ADV', *day_args]:
                return NMC_advance(day_args)
            case ['DATE' | 'DAT']:
                return NMC_date()
            case ['POLL']:
                return NMC_poll()
            case ['PROJECT' | 'PROJ']:
                return NMC_projects()
            case ['REACTION' | 'REACT', *react_args]:
                return NMC_react(react_args)
            case ['QUICKBUDGET' | 'QB', *qb_args]:
                return NMC_quickbudget(qb_args)
            case ['QUIT']:
                return ["QUIT"]
            case _:
                return ["INVALID INPUT"]


def NMC_action(args):
    """
    The ACTION/ACT keyword. ACTION creates projects of a
    given cost, duration etc. and also runs a function
    in the Ministry class that generates a success rating
    for said action, applying various modifiers to a random
    roll.

    arguments:

    department -- the id code of the ministry taking the action
    name -- a string bounded by ' \" ', which names the project
    difficulty -- how hard the action is, from 0 ('quotidian') to 10 ('completely insane')
    cost -- the estimated cost in £M
    time =- the estimated time to completion in days
    --S -- optional flag that marks the project as being secret
    --XD -- optional flag that marks the projects as being 'out of domain'

    returns a string describing the outcome of the action as a list
    """
    secret = False
    in_domain = True
    #  error handling section
    if len(args) < 5:
        return error_handler(5)
    else:
        department = args[0]
        name = args[1]
        difficulty = args[2]
        cost = args[3]
        time = args[4]
        if department not in game.dept_dict.keys():
            return error_handler(1)
        elif name[0] != '"' or name[-1] != '"':
            return error_handler(10)
        elif not difficulty.isdigit():
            return error_handler(2)
        elif int(difficulty) <= -1 or int(difficulty) >= 11:
            return error_handler(3)
        elif not cost.isdigit():
            return error_handler(4)
        elif not time.isdigit():
            return error_handler(11)
        else:
            # if input is correct
            if "--XD" in args:
                in_domain = False
            if "--S" in args:
                secret = True
            id = game.get_project_code()
            result = game.dept_dict[department].action(name,
                                                       int(difficulty),
                                                       int(cost),
                                                       int(time),
                                                       secret,
                                                       in_domain,
                                                       id)
            return [f"{hr}\n{'PRESS RELEASE' if not secret else 'CONFIDENTIAL MEMO'}: {result.a_string}\n{hr}"]


def NMC_advance(args):
    """
    The ADVANCE/ADV keyword. ADVANCE moves the game simulation
    forward by a number of days. Calls a series of cascading 'tick'
    functions in various game objects that advances their simulation
    state.

    arguments:

    amount -- the number of days to advance

    returns a string and a subcommand that tells
    the simulation how many days to advance as a list
    """
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
            return [f"{date}\nADVANCING {days} DAYS", f"LOAD+ {days}"]


def NMC_date():
    """
    The DATE keyword. Returns a single line string which shows  the current date as a list
    """
    time = game.world.clock.time
    return [f"CURRENT DATE: {time.date} {time.month['code']} {time.year}"]


def NMC_poll():
    """
    The POLL keyword. Calls the poll() function
    of the Game object and returns the result as a list.
    """
    return [game.poll()]


def NMC_projects():
    """
    The PROJECT/PROJ keyword. Generates a new set of secret project
    name cards and returns a single line string as a list.
    """
    issue = game.computer.secret_project_counter
    generate_project_cards(issue)
    game.computer.secret_project_counter += 1
    return [f"GENERATED SECRET PROJECTS CARDS, ISSUE {issue}"]


def NMC_react(args):
    """
    The REACTION/REACT keyword. REACT applies the affect
    of the press's reaction to a press conference or
    statement. Tt calls the UK object's 'political_drift()' function
    with the given inputs, applying changes to the direction of
    national political opinion.

    arguments:
    paper -- id code of the paper
    approval -- boolean of the approval ('Y' or 'N')

    returns a string describing the result.
    """
    if len(args) < 2:
        return(error_handler(5))
    else:
        paper = args[0]
        approval = args[1]
        if paper not in game.press_dict.keys():
            return(error_handler(8))
        elif approval not in ('Y', 'N'):
            return(error_handler(9))
        else:
            paper_obj = game.press_dict[paper]
            approval_bool = True if approval == 'Y' else False
            result = game.uk.political_drift(paper_obj, approval_bool)
            return [f"REPORT: {result.r_string}"]


def NMC_quickbudget(args):
    """
    The QUICKBUDGET/QB Keyword.

    Returns a quick budget report as a string.

    """
    redacted = False
    if len(args) > 3:
        return error_handler(6)
    elif args[0] not in game.dept_dict.keys():
        return error_handler(1)
    else:
        if "--R" in args:
            redacted = True
        budget_dict = game.dept_dict[args[0]].quick_budget_report()
        time = game.world.clock.time
        report_string = f"{hr}\n" \
                        f"QUICK BUDGET REPORT - {budget_dict['name']}\n" \
                        f"{time.date} {time.month['code']} {time.year}\n" \
                        f"ANNUAL BUDGET: £{budget_dict['annual budget']}M\n" \
                        f"CURRENT REMAINING: £{'%.2f' % budget_dict['current budget']}M\n" \
                        f"DAILY OPERATING COSTS: £{'%.2f' % budget_dict['daily operating cost']}M\n{hr}\n\n" \
                        f"CURRENT PUBLIC PROJECTS:\n\n"
        if len(budget_dict['active projects']) == 0:
            report_string += "[NONE]\n\n"
        else:
            #  iterates through active public projects
            total_project_cost = 0
            total_remaining_cost = 0
            total_daily_cost = 0
            for project in budget_dict['active projects']:
                project_dict = project.quick_budget_report()
                report_string += project_block(project_dict)
                total_project_cost += project_dict['estimated cost']
                total_remaining_cost += project_dict['estimated remaining cost']
                total_daily_cost += project_dict['actual daily cost']

            report_string += project_total_block(total_project_cost,
                                                 total_remaining_cost,
                                                 total_daily_cost)
        report_string += "CURRENT SECRET PROJECTS:\n\n"
        if redacted:
            report_string += "[+REDACTED+]"
        elif not redacted and len(budget_dict['active secret projects']) == 0:
            report_string += "[NONE]\n\n"
        else:
            #  iterates through active secret projects
            total_project_cost = 0
            total_remaining_cost = 0
            total_daily_cost = 0
            for project in budget_dict['active secret projects']:
                project_dict = project.quick_budget_report()
                report_string += project_block(project_dict)
                total_project_cost += project_dict['estimated cost']
                total_remaining_cost += project_dict['estimated remaining cost']
                total_daily_cost += project_dict['actual daily cost']
            report_string += project_total_block(total_project_cost,
                                                 total_remaining_cost,
                                                 total_daily_cost)

        return [report_string]


def project_total_block(total_project_cost, total_remaining_cost, total_daily_cost):
    # function for quick budget reports
    return f"TOTAL COST (EST.): £{'%.2f' % total_project_cost}M\n" \
           f"TOTAL REMAINING COST (EST.): £{'%.2f' % total_remaining_cost}M\n" \
           f"TOTAL DAILY COST (ACTUAL): £{'%.2f' % total_daily_cost}M\n\n{hr}\n"


def project_block(project_dict):
    # function for quick budget reports
    return f"{project_dict['name']} - ETA: {project_dict['eta']} DAYS\n" \
           f"ESTIMATED TOTAL COST: £{project_dict['estimated cost']}M\n" \
           f"ESTIMATED DAILY COST: £{'%.2f' % project_dict['estimated daily cost']}M\n" \
           f"ACTUAL DAILY COST: £{'%.2f' % project_dict['actual daily cost']}M\n" \
           f"TOTAL COST TO DATE: £{'%.2f' % project_dict['total cost to date']}M\n" \
           f"ESTIMATED REMAINING COST: £{'%.2f' % project_dict['estimated remaining cost']}M\n\n"


def game_read():
    return f"{len(game.reg_dict.keys())} REGIONS, {len(game.min_dict)} MINISTERS, " \
           f"{len(game.dept_dict.keys())} DEPARTMENTS SUCCESSFULLY IMPORTED"

