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
                 current_project_code='P1',
                 session_id=0):
        self.reg_dict = reg_dict
        self.min_dict = min_dict
        self.dept_dict = dept_dict
        self.world = world
        self.uk = uk
        self.computer = computer
        self.press_dict = press_dict
        self.force_dict = force_dict
        self.current_project_code = current_project_code
        self.session_id = session_id

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
        self.regions = []
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
        self.edges = edges
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
        self.land_power = land_power
        self.air_power = air_power
        self.sea_power = sea_power
        self.morale = morale
        self.experience = experience
        self.quality = quality
        self.allegience = allegiance
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
        self.oceanic_power = self.ocean_air_power + self.sea_power
        self.littoral_power = self.sea_power + self.land_power + self.air_power
        self.continental_power = self.land_power + self.sea_power
        self.power_dict = {'OCEANIC': self.oceanic_power,
                           'LITTORAL': self.littoral_power,
                           'CONTINENTAL': self.continental_power}