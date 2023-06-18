from random import seed, randint, uniform
from dataclasses import dataclass
import string_dicts as sd


class Computer:
    """
    This object stores values and functions related to the operation
    of the virtual National Management Computer
    """
    def __init__(self, secret_project_counter, runtime):
        self.secret_project_counter = secret_project_counter
        self.runtime = runtime

    def tick(self):
        self.runtime += 1

    def csv_rep(self):
        return f"secret project counter,{self.secret_project_counter}\n" \
               f"runtime,{self.runtime}"


class UK:
    """
    This class stores information and performs functions regarding the
    state of the UK as a whole.
    """

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
        self.political_movement = sd.political_movement_strength_dict()

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

    def csv_rep(self):
        return f"population,{self.population}\n" \
               f"population health,{self.population_health}\n" \
               f"stability,{self.stability}\n" \
               f"government,{self.government}\n" \
               f"monarch pronoun,{self.monarch_pronoun}"


class Region:
    """
    This class stores information about a UK region.
    """

    def __init__(self, id, name, pop_portion, hmg_pop, hmo_pop, lib_pop, mrwp_pop, mlwp_pop):
        self.id = id
        self.name = name
        self.pop_portion = int(pop_portion)
        self.hmg_pop = float(hmg_pop)
        self.hmo_pop = float(hmo_pop)
        self.lib_pop = float(lib_pop)
        self.mrwp_pop = float(mrwp_pop)
        self.mlwp_pop = float(mlwp_pop)

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

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.pop_portion}," \
               f"{self.hmg_pop}," \
               f"{self.hmo_pop}," \
               f"{self.lib_pop}," \
               f"{self.mrwp_pop}," \
               f"{self.mlwp_pop}"


class Minister:
    """
    This class stores information about a Minister (The PCs)
    """

    def __init__(self, id, name, p_name, region, popularity=0):
        self.id = id
        self.name = name
        self.p_name = p_name
        self.region = region
        self.pop = popularity
        self.pm = False

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.p_name}," \
               f"{self.region}"


class Ministry:
    """
    This class contains information and functions relating to ministerial departments.
    """

    def __init__(self,
                 id,
                 name,
                 title,
                 minister,
                 starting_morale,
                 budget,
                 operating_cost,
                 experience,
                 fatigue,
                 morale_drift,
                 active_projects,
                 active_secret_projects,
                 completed_projects,
                 completed_secret_projects):
        self.id = id
        self.name = name
        self.title = title
        self.morale = int(starting_morale)
        self.budget = int(budget)
        self.current_budget = self.budget
        self.operating_cost_annual = int(operating_cost)
        self.operating_cost_daily = self.operating_cost_annual / 365
        self.experience = int(experience)
        self.fatigue = int(fatigue)
        self.morale_drift = float(morale_drift)
        self.active_projects = active_projects
        self.active_secret_projects = active_secret_projects
        self.completed_projects = completed_projects
        self.completed_secret_projects = completed_secret_projects
        self.minister = minister
        self.minister.pm = True if self.id == "M10" else False
        self.minister.pop = self.minister.region.hmo_pop if self.id == "M1" \
            else self.minister.region.hmg_pop
        self.difficulties = sd.difficulty_dict()

    def action(self, name, difficulty, cost, time, secret, in_domain, id):
        seed()
        modifier = (difficulty * 10 + randint(-difficulty, 0)) - 10
        modifier += 10 if secret else 0
        modifier -= self.morale
        modifier -= self.experience
        modifier += self.fatigue
        modifier += (modifier * 0.5) if not in_domain else 0
        roll = (randint(1, 100) + modifier)

        outcome = sd.result(roll)
        outcome_score, outcome_string = outcome[0], outcome[1]

        morale_tuple = self.morale_update(roll, difficulty)
        morale_change, morale_string = morale_tuple[0], morale_tuple[1]
        self.morale_drift += (morale_change / 10)
        domain_string = "within" if in_domain else "outside"

        action_string = (f"The {self.name} attempts {name}, a {'secret' if secret else 'public'}"
                         f" action of {self.difficulties[difficulty]} difficulty. This action "
                         f"is {domain_string} the department's domain. The result is "
                         f"{outcome_string}. This has a{morale_string} effect on departmental morale. "
                         f"it will take at least {time} days for the action to complete.")

        action_project = Project(id, name, cost, time, outcome_score, secret)

        if secret:
            self.active_secret_projects.append(action_project)
        else:
            self.active_projects.append(action_project)

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

    def tick(self):
        self.morale += self.morale_drift
        daily_project_cost = 0
        for project in self.active_projects:
            if not project.completed:
                daily_project_cost += project.tick()
        for project in self.active_secret_projects:
            if not project.completed:
                daily_project_cost += project.tick()
        self.current_budget -= daily_project_cost
        self.current_budget -= self.operating_cost_daily

    def quick_budget_report(self):
        return {"name": self.name.upper(),
                "annual budget": self.budget,
                "current budget": self.current_budget,
                "daily operating cost": self.operating_cost_daily,
                "active projects": self.active_projects,
                "active secret projects": self.active_secret_projects}

    def audit(self):
        pass

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.title}," \
               f"{self.minister.id}," \
               f"{self.morale}," \
               f"{self.budget}," \
               f"{self.operating_cost_annual}," \
               f"{self.experience}," \
               f"{self.fatigue}," \
               f"{self.morale_drift}"


class Project:
    """class storing the ongoing costs of projects"""
    def __init__(self,
                 id,
                 name,
                 cost,
                 time,
                 outcome,
                 secret,
                 ministry,
                 completed=False,
                 imported=False,):
        self.id = id
        self.name = name
        self.cost = int(cost)
        self.estimated_cost = self.cost
        self.outcome = int(outcome)
        self.time = int(time)
        self.estimated_time = self.time
        self.timer = 0
        self.ministry = ministry
        self.estimated_cost_daily = self.estimated_cost / self.estimated_time
        self.running_cost = 0
        if not imported:
            if self.outcome == 4:
                self.cost += randint(0, self.cost // 10)
            elif self.outcome == 3:
                self.cost += (randint(0, self.cost // 8) + 5)
                self.time += randint(0, self.time // 10)
            elif self.outcome == 2:
                self.cost += (randint(0, self.cost // 6) + 10)
                self.time += (randint(0, self.time // 8) + 5)
            elif self.outcome == 1:
                self.cost += (randint(0, self.cost // 4) + 15)
                self.time += (randint(0, self.cost // 6) + 10)
            elif self.outcome == 0:
                self.cost += (randint(0, self.cost // 2) + 20)
                self.time += (randint(0, self.cost // 4) + 15)
            else:
                pass
        self.cost_daily = self.cost / self.time
        self.completed = completed
        self.secret = secret
        if not self.completed:
            self.status_string = "IN PROGRESS"
        else:
            self.status_string = "COMPLETED"

    def tick(self):
        self.timer += 1
        if self.timer == self.time:
            self.completed = True
            self.status_string = "COMPLETED"
        self.running_cost += self.cost_daily
        return self.cost_daily

    def quick_budget_report(self):
        return {"name": self.name.upper(),
                "eta": self.estimated_time - self.timer,
                "estimated cost": self.estimated_cost,
                "estimated daily cost": self.estimated_cost_daily,
                "actual daily cost": self.cost_daily,
                "total cost to date": self.running_cost,
                "estimated remaining cost": self.estimated_cost - self.running_cost}

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.cost}," \
               f"{self.time}," \
               f"{self.outcome}," \
               f"{'Y' if self.secret else 'N'}," \
               f"{'Y' if self.completed else 'N'}," \
               f"{self.ministry}"


class Paper:
    """class storing the positions of papers"""
    def __init__(self,
                 id,
                 name,
                 ideology,
                 endorsement):
        self.id = id
        self.name = name
        self. ideology = ideology
        self. endorsement = endorsement

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.ideology}," \
               f"{self.endorsement}"


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
class Reaction:
    """class storing the reaction to conference"""
    lr_drift: float
    go_drift: float
    r_string: str
