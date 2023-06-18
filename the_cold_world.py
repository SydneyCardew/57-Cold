from statistics import mean
from atomic_clock import Clock


class Game:
    """
    overall container for game objects
    """
    def __init__(self,
                 reg_dict,
                 min_dict,
                 dept_dict,
                 world,
                 uk,
                 computer,
                 press_dict,
                 force_dict,
                 code,
                 current_project_code='P1'
                 ):
        self.reg_dict = reg_dict
        self.min_dict = min_dict
        self.dept_dict = dept_dict
        self.world = world
        self.uk = uk
        self.computer = computer
        self.press_dict = press_dict
        self.force_dict = force_dict
        self.current_project_code = current_project_code
        self.code = code

    def tick(self):
        """
        This function is the first in a chain that advances the simulation
        state of many different game objects
        """
        self.world.tick()
        self.uk.tick()
        for region in self.reg_dict.values():
            region.tick(self.uk)
        for ministry in self.dept_dict.values():
            ministry.tick()

    def poll(self):
        """
        This function generates political opinion polls as a string.
        It begins by extracting local polling date from each region,
        then averages these out, weighting by the population of each
        region, before producing a final report.
        """
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

    def get_project_code(self):
        output_code = self.current_project_code
        project_number = int(self.current_project_code[1:])
        project_number += 1
        self.current_project_code = f"W{project_number}"
        return output_code


class World:
    """
    This class stores information about the global state
    """

    def __init__(self, year, day):
        self.year = year
        self.year_day = day
        self.clock = Clock(self.year, self.year_day)
        self.regions = {}
        self.navigation_graph = {}

    def tick(self):
        self.clock.tick()

    def csv_rep(self):
        return f"year,{self.year}\n" \
               f"day,{self.year_day}"

    def show_graph(self):
        """
        returns a string representation of the navigation graph (testing function)
        """
        graph_string = ''
        for key, value in self.navigation_graph.items():
            graph_string += f"{key}:{value}\n"
        return graph_string


class WorldMapRegion:
    """
    This class stores information about specific world map regions.
    """

    def __init__(self,
                 id,
                 name,
                 hemisphere,
                 climate,
                 terrain,
                 edges,
                 SV_dom,
                 US_dom,
                 UK_dom,
                 crisis_damage,
                 SV_fort,
                 US_fort,
                 UK_fort,
                 NA_fort
                 ):
        self.id = id
        self.name = name
        self.hemisphere = hemisphere.upper()
        self.climate = climate.upper()
        self.terrain = terrain.upper()
        self.edges = "".join(edges).split(",")
        self.SV_dom = int(SV_dom)
        self.US_dom = int(US_dom)
        self.UK_dom = int(UK_dom)
        self.NA_dom = 100 - (self.SV_dom + self.US_dom + self.UK_dom)
        self.dom_dict = {'SV': self.SV_dom,
                         'US': self.US_dom,
                         'UK': self.UK_dom,
                         'NA': self.NA_dom}
        self.crisis_damage = int(crisis_damage)
        self.SV_fort = int(SV_fort)
        self.US_fort = int(US_fort)
        self.UK_fort = int(UK_fort)
        self.NA_fort = int(NA_fort)
        self.fort_dict = {'SV': self.SV_fort,
                          'US': self.US_fort,
                          'UK': self.UK_fort,
                          'NA': self.NA_fort}

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.hemisphere}," \
               f"{self.climate}," \
               f"{self.terrain}," \
               f"{self.edge_rep()}," \
               f"{self.SV_dom}," \
               f"{self.US_dom}," \
               f"{self.UK_dom}," \
               f"{self.crisis_damage}," \
               f"{self.SV_fort}," \
               f"{self.US_fort}," \
               f"{self.UK_fort}," \
               f"{self.NA_fort}"

    def edge_rep(self):
        edge_string = '"'
        for i, edge in enumerate(self.edges):
            edge_string += edge
            if i < len(self.edges) - 1:
                edge_string += ","
            else:
                edge_string += '"'
        return edge_string


class Force:
    """
    Class storing information and functions related to military forces
    """

    def __init__(self,
                 id,
                 name,
                 land_power,
                 air_power,
                 sea_power,
                 morale,
                 experience,
                 quality,
                 allegiance,
                 location):
        self.id = id
        self.name = name
        self.land_power = int(land_power)
        self.air_power = int(air_power)
        self.sea_power = int(sea_power)
        self.morale = int(morale)
        self.experience = int(experience)
        self.quality = int(quality)
        self.allegiance = allegiance
        self.location = location
        self.destination = None
        self.path = None
        self.set_ocean_air_power()
        self.set_total_powers()

    def set_ocean_air_power(self):
        self.max_ocean_air_power = self.sea_power // 2
        self.ocean_air_power = self.air_power \
            if self.air_power <= self.max_ocean_air_power \
            else self.max_ocean_air_power

    def set_total_powers(self):
        self.oceanic_power = (self.ocean_air_power + self.sea_power) * self.quality
        self.littoral_power = (self.sea_power + self.land_power + self.air_power) * self.quality
        self.continental_power = (self.land_power + self.sea_power) * self.quality
        self.power_dict = {'OCEANIC': self.oceanic_power,
                           'LITTORAL': self.littoral_power,
                           'CONTINENTAL': self.continental_power}

    def fight(self, aggressor, terrain):
        attack_power = aggressor.power_dict[terrain] * aggressor.quality * (aggressor.morale / 100)
        defence_power = self.power_dict[terrain] * self.quality * (self.morale / 100)
        reduction = abs(attack_power - defence_power) / 2
        enemy_morale_boost = self.take_damage(reduction)
        return enemy_morale_boost

    def take_damage(self, damage):
        distro_dict = {'land': self.land_power,
                       'sea': self.sea_power,
                       'air': self.air_power}
        temp = sum(distro_dict.values())
        for key, val in distro_dict.items():
            distro_dict[key] = round((val / temp), 2)
        temp_land_power = self.land_power - (damage * distro_dict['land'])
        temp_sea_power = self.sea_power - (damage * distro_dict['sea'])
        temp_air_power = self.air_power - (damage * distro_dict['air'])
        land_p_reduction = ((self.land_power - temp_land_power) / self.land_power) * 100
        sea_p_reduction = ((self.sea_power - temp_sea_power) / self.sea_power) * 100
        air_p_reduction = ((self.air_power - temp_air_power) / self.air_power) * 100
        temp_morale = self.morale - mean([land_p_reduction, sea_p_reduction, air_p_reduction])
        morale_diff = abs(temp_morale - self.morale)
        self.morale = temp_morale
        self.quality -= morale_diff / 100
        self.quality = 1 if self.quality < 1 else self.quality
        self.land_power = temp_land_power
        self.sea_power = temp_sea_power
        self.air_power = temp_air_power
        self.set_ocean_air_power()
        self.set_total_powers()
        return morale_diff

    def power_report(self):
        return f"name: {self.name}. " \
               f"land power: {self.land_power}, " \
               f"sea power: {self.sea_power}, " \
               f"air power: {self.air_power}, " \
               f"morale: {self.morale}, " \
               f"quality: {self.quality}"

    def csv_rep(self):
        return f"{self.id}," \
               f"{self.name}," \
               f"{self.land_power}," \
               f"{self.air_power}," \
               f"{self.sea_power}," \
               f"{self.morale}," \
               f"{self.experience}," \
               f"{self.quality}," \
               f"{self.allegiance}," \
               f"{self.location}"


class Conflict:

    def __init__(self,
                 attack_force,
                 defence_force,
                 battleground
                 ):
        self.attack_force = attack_force
        self.defence_force = defence_force
        self.battleground = battleground
        self.historical = False
        self.timer = 0

    def tick(self):
        self.timer += 1
        self.attack_force.morale += self.defence_force.fight(self.attack_force, self.battleground.terrain)
        self.defence_force.morale += self.attack_force.fight(self.defence_force, self.battleground.terrain)

    def disengage_check(self):
        pass
