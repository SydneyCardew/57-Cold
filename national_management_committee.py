from random import seed, randint, uniform
from statistics import mean
from dataclasses import dataclass
from atomic_clock import Clock


class Game:
    """overall container for game objects"""

    def __init__(self, reg_dict, min_dict, dept_dict, world, uk, computer, press_dict):
        self.reg_dict = reg_dict
        self.min_dict = min_dict
        self.dept_dict = dept_dict
        self.world = world
        self.uk = uk
        self.computer = computer
        self.press_dict = press_dict

    def tick(self):
        self.world.tick()
        self.uk.tick()
        for region in self.reg_dict.values():
            region.tick(self.uk)

    def poll(self):
        hmg_pops = []
        hmo_pops = []
        lib_pops = []
        mlwp_pops = []
        mrwp_pops = []
        for region in self.reg_dict.values():
            hmg_pops.extend([region.hmg_pop] * region.pop_portion)
            hmo_pops.extend([region.hmo_pop] * region.pop_portion)
            lib_pops.extend([region.lib_pop] * region.pop_portion)
            mlwp_pops.extend([region.mlwp_pop] * region.pop_portion)
            mrwp_pops.extend([region.mrwp_pop] * region.pop_portion)
        hmg_pop = mean(hmg_pops)
        hmo_pop = mean(hmo_pops)
        lib_pop = mean(lib_pops)
        mlwp_pop = mean(mlwp_pops)
        mrwp_pop = mean(mrwp_pops)
        return f"CURRENT POLLING:\n" \
               f"{self.uk.monarch_pronoun} MAJESTY'S GOVERNMENT: {round(hmg_pop, 2)}%\n" \
               f"{self.uk.monarch_pronoun} MAJESTY'S OPPOSITION: {round(hmo_pop, 2)}%\n" \
               f"LIBERALS: {round(lib_pop, 2)}%\n" \
               f"MINOR PARTIES OF THE LEFT: {round(mlwp_pop, 2)}%\n" \
               f"MINOR PARTIES OF THE RIGHT: {round(mrwp_pop, 2)}%"




class Computer:

    def __init__(self, secret_project_counter, runtime):
        self.secret_project_counter = secret_project_counter
        self.runtime = runtime

    def tick(self):
        self.runtime += 1


class World:

    def __init__(self, year, day):
        self.year = year
        self.year_day = day
        self.clock = Clock(self.year, self.year_day)

    def tick(self):
        self.clock.tick()


class WorldMap:

    def __init__(self):
        pass


class UK:

    def __init__(self, population,
                 population_health,
                 stability, government,
                 monarch_pronoun):

        self.population = int(population)
        self.population_health = int(population_health)
        self.stability = int(stability)
        self.government = government
        self.monarch_pronoun = monarch_pronoun.upper()
        self.political_drift_lr = 0
        self.political_drift_go = 0
        self.political_movement = {0.1: "almost undetectable",
                                   0.2: "very weak",
                                   0.3: "weak",
                                   0.4: "small but noticeable",
                                   0.5: "noticeable",
                                   0.6: "very noticeable",
                                   0.7: "distinct",
                                   0.8: "strong",
                                   0.9: "very strong",
                                   1.0: "dramatic"}

    def political_drift(self, paper, approval):
        """this function transforms the press's reaction to press conferences and statements into opihion vectors"""

        # sf is the 'stability factor'. The less stable the nation the wilder the political swings will be
        sf = (100 - self.stability) / 10

        if approval:
            right_approval = 1 if paper.ideology == 'right' else 0
            left_approval = 1 if paper.ideology == 'left' else 0
            centre_approval = 1 if paper.ideology == 'center' else 0
            gov_approval = 1 if paper.endorsement == 'government' else 0
            opp_approval = 1 if paper.endorsement == 'opposition' else 0
            ind_approval = 1 if paper.endorsement == 'independent' else 0
        else:
            right_approval = -1 if paper.ideology == 'right' else 0
            left_approval = -1 if paper.ideology == 'left' else 0
            centre_approval = -1 if paper.ideology == 'center' else 0
            gov_approval = -1 if paper.endorsement == 'government' else 0
            opp_approval = -1 if paper.endorsement == 'opposition' else 0
            ind_approval = -1 if paper.endorsement == 'independent' else 0

        if gov_approval > 0:
            shift = (uniform(0.1, 0.2) * sf)
            self.political_drift_go += shift
            self.political_drift_lr += shift if self.government == 'right' else -shift
        elif gov_approval < 0:
            shift = (uniform(0.1, 0.2) * sf)
            self.political_drift_go -= shift
            self.political_drift_lr += -shift if self.government == 'right' else shift
        else:
            self.political_drift_go += (uniform(-0.04, 0.05) * sf)

        if opp_approval > 0:
            shift = (uniform(0.1, 0.2) * sf)
            self.political_drift_go -= shift
            self.political_drift_lr += -shift if self.government == 'right' else shift
        elif opp_approval < 0:
            shift = (uniform(0.1, 0.2) * sf)
            self.political_drift_go += shift
            self.political_drift_lr += shift if self.government == 'right' else -shift
        else:
            self.political_drift_go += (uniform(-0.04, 0.05) * sf)

        if ind_approval > 0:
            self.political_drift_go += (uniform(0.1, 0.2) * sf) if self.political_drift_go < 0 \
                else (uniform(-0.2, -0.1) * sf)
        elif ind_approval < 0:
            self.political_drift_go += (uniform(0.1, 0.2) * sf) if self.political_drift_go > 0 \
                else (uniform(-0.2, -0.1) * sf)
        else:
            self.political_drift_go += (uniform(-0.04, 0.05) * sf)

        if right_approval > 0:
            self.political_drift_lr += (uniform(0.01, 0.05) * sf)
        elif right_approval < 0:
            self.political_drift_lr -= (uniform(0.01, 0.05) * sf)
        else:
            self.political_drift_lr += (uniform(-0.01, 0.01) * sf)

        if left_approval > 0:
            self.political_drift_lr -= (uniform(0.01, 0.05) * sf)
        elif left_approval < 0:
            self.political_drift_lr += (uniform(0.01, 0.05) * sf)
        else:
            self.political_drift_lr += (uniform(-0.01, 0.01) * sf)

        if centre_approval > 0:
            self.political_drift_lr += (uniform(0.01, 0.05) * sf) if self.political_drift_lr < 0 \
                else (uniform(-0.05, -0.01) * sf)
        elif centre_approval < 0:
            self.political_drift_lr += (uniform(0.01, 0.05) * sf) if self.political_drift_lr > 0 \
                else (uniform(-0.05, -0.01) * sf)
        else:
            self.political_drift_lr += (uniform(-0.01, 0.01) * sf)

        lr_drift_amount = abs(round(self.political_drift_lr, 1))
        if lr_drift_amount > 1.0:
            lr_drift_amount = 1.0

        if self.political_drift_lr < -0.05:
            lr_drift_direction = f'showing a {self.political_movement[lr_drift_amount]} shift to the left'
        elif self.political_drift_lr > 0.05:
            lr_drift_direction = f'showing a {self.political_movement[lr_drift_amount]} shift to the right'
        else:
            lr_drift_direction = 'showing no clear change'

        go_drift_amount = abs(round(self.political_drift_go, 1))
        if go_drift_amount > 1.0:
            go_drift_amount = 1.0

        if self.political_drift_go < -0.05:
            go_drift_direction = f'showing a {self.political_movement[go_drift_amount]} shift towards the opposition'
        elif self.political_drift_go > 0.05:
            go_drift_direction = f'showing a {self.political_movement[go_drift_amount]} shift towards the government'
        else:
            go_drift_direction = 'showing no clear change'

        r_string = f"The readers of {paper.name} absorb that paper's " \
                   f"{'positive' if approval else 'negative'} coverage of the recent statements.\n" \
                   f"Preliminary polling shows the nation is {lr_drift_direction} ideologically,\n" \
                   f"and that the sentiment of voters is {go_drift_direction}."

        return Reaction(self.political_drift_lr, self.political_drift_go, r_string)

    def tick(self):
        pass


class Region:

    def __init__(self, id, name, pop_portion, hmg_pop=40, hmo_pop=30, lib_pop=20, mrwp_pop=5, mlwp_pop=5):
        self.id = id
        self.name = name
        self.pop_portion = int(pop_portion)
        self.hmg_pop = hmg_pop
        self.hmo_pop = hmo_pop
        self.lib_pop = lib_pop
        self.mrwp_pop = mrwp_pop
        self.mlwp_pop = mlwp_pop
        self.party_pop()

    def party_pop(self):
        self.party_popularity = {"Her Majesty's Government": self.hmg_pop,
                                 "Her Majesty's Opposition": self.hmo_pop,
                                 "Liberal Party": self.lib_pop,
                                 "Minor Parties of the Right": self.mrwp_pop,
                                 "Minor Parties of the Left:": self.mlwp_pop}

    def tick(self, uk):
        self.hmg_pop += uk.political_drift_go / 2
        self.hmo_pop -= uk.political_drift_go / 2
        self.lib_pop += abs(uk.political_drift_go / 2)
        self.lib_pop -= abs(uk.political_drift_lr)
        self.mrwp_pop += uk.political_drift_lr / 2
        self.mlwp_pop -= uk.political_drift_lr / 2
        if uk.government == 'right':
            self.hmg_pop += uk.political_drift_lr / 2
            self.hmo_pop -= uk.political_drift_lr / 2
        elif uk.government == 'left':
            self.hmg_pop -= uk.political_drift_lr / 2
            self.hmo_pop += uk.political_drift_lr / 2
        else:
            self.mrwp_pop += uk.political_drift_lr / 2
            self.mlwp_pop -= uk.political_drift_lr / 2



class WorldRegion:

    def __init__(self):
        pass


class Minister:

    def __init__(self, id, name, p_name, region, popularity=0):
        self.id = id
        self.name = name
        self.p_name = p_name
        self.region = region
        self.pop = popularity
        self.pm = False

    def csv_rep(self):
        return f"{self.id},{self.name},{self.p_name},{self.region}"


class Ministry:
    """This class contains information and methods relating to Ministries"""

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


@dataclass
class Paper:
    """class storing the positions of papers"""
    id: str
    name: str
    ideology: str
    endorsement: str


@dataclass
class Reaction:
    """class storing the reaction to conference"""
    lr_drift: float
    go_drift: float
    r_string: str







