from random import seed, randint
from dataclasses import dataclass


class Game:
    """overall container for game objects"""

    def __init__(self, reg_dict, min_dict, dept_dict):
        self.reg_dict = reg_dict
        self.min_dict = min_dict
        self.dept_dict = dept_dict


class UK:

    def __init__(self, population):
        self.population = population


class Region:

    def __init__(self, id, name, hmg_pop=40, hmo_pop=30, lib_pop=20, mrwp_pop=5, mlwp_pop=5):
        self.id = id
        self.name = name
        self.hmg_pop = hmg_pop
        self.hmo_pop = hmo_pop
        self.lib_pop = lib_pop
        self.mrwp_pop = mrwp_pop
        self.mlwp_pop = mlwp_pop
        self.party_popularity = {"Her Majesty's Government": hmg_pop,
                                 "Her Majesty's Opposition": hmo_pop,
                                 "Liberal Party": lib_pop,
                                 "Minor Parties of the Right": mrwp_pop,
                                 "Minor Parties of the Left:": mlwp_pop}


class Minister:

    def __init__(self, id, name, p_name, region):
        self.id = id
        self.name = name
        self.p_name = p_name
        self.region = region
        self.pop = 0
        self.pm = False

    def csv_rep(self):
        return f"{self.id},{self.name},{self.p_name},{self.region}"


class Ministry:

    def __init__(self, id, name, title, minister, starting_morale=70, f_budget=100, e_budget=20, s_budget=20):
        self.id = id
        self.name = name
        self.title = title
        self.morale = starting_morale
        self.f_budget = f_budget
        self.e_budget = e_budget
        self.s_budget = s_budget
        self.experience = 0
        self.fatigue = 0
        self.e_projects = []
        self.s_projects = []
        self.minister = minister
        self.minister.pm = True if self.id == "M10" else False
        self.minister.pop = self.minister.region.hmo_pop if self.id == "M1" \
            else self.minister.region.hmg_pop
        self.difficulties = {0: "quotidian",
                             1: "facile",
                             2: "ordinary",
                             3: "uncommon",
                             4: "challenging",
                             5: "fiendish",
                             6: "daunting",
                             7: "awesome",
                             8: "ridiculous",
                             9: "utterly absurd",
                             10: "completely insane"
                             }

    def action(self, difficulty, cost, secret, in_domain):
        seed()
        modifier = (difficulty * 10 + randint(-difficulty, 0)) - 10
        a_budget = self.s_budget if secret else self.e_budget
        a_budget -= cost
        self.s_budget -= cost if secret else 0
        self.e_budget -= cost if secret else 0
        modifier -= (a_budget - difficulty * 5) if a_budget < 0 else 0
        modifier += 10 if secret else 0
        modifier -= self.morale
        modifier -= self.experience
        modifier += self.fatigue
        modifier += (modifier * 0.5) if not in_domain else 0
        roll = (randint(1, 100) + modifier)

        outcome = self.result(roll)
        outcome_score, outcome_string = outcome[0], outcome[1]

        morale_tuple = self.morale_update(roll, difficulty)
        morale_change, morale_string = morale_tuple[0], morale_tuple[1]
        self.morale += morale_change
        domain_string = "within" if in_domain else "outside"

        action_string = (f"The {self.name} attempts a {'secret' if secret else 'public'}"
                         f" action of {self.difficulties[difficulty]} difficulty. This action "
                         f"is within the department's domain. The result is "
                         f"{outcome_string}. This has a{morale_string} effect on departmental morale.")
        return Outcome(difficulty, cost, secret, roll, morale_change, outcome_score, action_string)

    def morale_update(self, score, difficulty):
        if score < 0:
            modifier = randint(10, 15) + difficulty
            return (modifier, " highly positive")
        elif score >= 1 and score <= 25:
            modifier = randint(5, 10) + difficulty
            return (modifier, " positive")
        elif score >= 26 and score <= 50:
            modifier = randint(-5, 5)
            return (modifier, "n unclear")
        elif score >= 51 and score <= 75:
            modifier = randint(-15, -5)
            return (modifier, " negative")
        elif score >= 76 and score <= 100:
            modifier = randint(-25, -15)
            return (modifier, " highly negative")
        else:
            modifier = (randint(-35, -25))
            return (modifier, "n appalling")

    def result(self, score):
        if score < 0:
            return 5, "an unqualified success. The orders are carried out " \
                   "to the letter, on time, and on budget"
        elif score >= 1 and score <= 25:
            return 4, "an almost total success. Perhaps a few minor objectives " \
                   "are not fully achieved, or it runs slightly over budget," \
                   "but overall a good result"
        elif score >= 26 and score <= 50:
            return 3, "decidedly mixed. Success is either partial, or there are " \
                   "unforseen negative outcomes"
        elif score >= 51 and score <= 75:
            return 2, "very poor. Some progress is made, a few minor objectives achieved, " \
                   "but overall, the action is a failure"
        elif score >= 76 and score <= 100:
            return 1, "an almost total failure. The objectives are not achieved, and there " \
                   "are serious negative ramifications"
        else:
            return 0, "an utter disaster. Not only does the action fail, " \
                   "it backfires spectacularly"

    def audit(self):
        pass


@dataclass()
class Project:
    """class storing the ongoing costs of projects"""
    name: str
    cost: int


@dataclass
class Outcome:
    """class storing the outcomes of actions"""
    difficulty: int
    cost: int
    secret: bool
    roll: int
    morale_change: int
    outcome_score: int
    a_string: str







