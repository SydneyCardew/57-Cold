import os
import csv
import national_management_committee as nmc
import the_cold_world as tcw


def importer(code):
    target = last_session(code)
    """This code reads the csv files and turns them into game objects"""
    if code not in code_list():
        return None

    else:
        with open(f"./games/GAME SESSION {code}/{target}/regions.csv") as reg_csv:
            reg_reader = csv.reader(reg_csv)
            reg_dict = {}
            for i, row in enumerate(reg_reader):
                if i > 0:
                    reg_dict[row[0]] = nmc.Region(row[0],
                                                  row[1],
                                                  row[2],
                                                  row[3],
                                                  row[4],
                                                  row[5],
                                                  row[6],
                                                  row[7])

        with open(f"./games/GAME SESSION {code}/{target}/ministers.csv") as min_csv:
            min_reader = csv.reader(min_csv)
            min_dict = {}
            for i, row in enumerate(min_reader):
                if i > 0:
                    min_dict[row[0]] = nmc.Minister(row[0], row[1], row[2], reg_dict[row[3]])

        with open(f"./games/GAME SESSION {code}/{target}/projects.csv") as proj_csv:
            proj_reader = csv.reader(proj_csv)
            combined_proj_dict = {}
            for i, row in enumerate(proj_reader):
                if i > 0:
                    combined_proj_dict[row[7]] = nmc.Project(row[0],
                                                             row[1],
                                                             row[2],
                                                             row[3],
                                                             row[4],
                                                             True if row[5] == 'Y' else False,
                                                             row[7],
                                                             True if row[6] == 'Y' else False,
                                                             True)

        with open(f"./games/GAME SESSION {code}/{target}/ministries.csv") as dept_csv:
            dept_reader = csv.reader(dept_csv)
            dept_dict = {}

            for i, row in enumerate(dept_reader):
                if i > 0:
                    public_proj_active = [x for x in [combined_proj_dict[row[0]]]
                                          if not x.secret and not x.completed]
                    secret_proj_active = [x for x in [combined_proj_dict[row[0]]]
                                          if x.secret and not x.completed]
                    public_proj_complete = [x for x in [combined_proj_dict[row[0]]]
                                            if not x.secret and x.completed]
                    secret_proj_complete = [x for x in [combined_proj_dict[row[0]]]
                                            if x.secret and x.completed]
                    dept_dict[row[0]] = nmc.Ministry(row[0],
                                                     row[1],
                                                     row[2],
                                                     min_dict[row[3]],
                                                     row[4],
                                                     row[5],
                                                     row[6],
                                                     row[7],
                                                     row[8],
                                                     row[9],
                                                     public_proj_active,
                                                     secret_proj_active,
                                                     public_proj_complete,
                                                     secret_proj_complete)

        with open(f"./games/GAME SESSION {code}/{target}/world_situation.csv") as worldsit_csv:
            worldsit_reader = csv.reader(worldsit_csv)
            worldsit_dict = {}
            for row in worldsit_reader:
                worldsit_dict[row[0]] = row[1]
            world = tcw.World(int(worldsit_dict['year']),
                              int(worldsit_dict['day']))

        with open(f"./games/GAME SESSION {code}/{target}/national_situation.csv") as natsit_csv:
            natsit_reader = csv.reader(natsit_csv)
            natsit_dict = {}
            for row in natsit_reader:
                natsit_dict[row[0]] = row[1]
            uk = nmc.UK(natsit_dict['population'],
                        natsit_dict['population health'],
                        natsit_dict['stability'],
                        natsit_dict['government'],
                        natsit_dict['monarch pronoun'])

        with open(f"./games/GAME SESSION {code}/{target}/comp_stats.csv") as comp_csv:
            comp_reader = csv.reader(comp_csv)
            comp_dict = {}
            for row in comp_reader:
                comp_dict[row[0]] = row[1]
            computer = nmc.Computer(comp_dict['secret project counter'],
                                    comp_dict['runtime'])

        with open(f"./games/GAME SESSION {code}/{target}/the_press.csv") as press_csv:
            press_reader = csv.reader(press_csv)
            press_dict = {}
            for i, row in enumerate(press_reader):
                if i > 0:
                    press_dict[row[0]] = nmc.Paper(row[0], row[1], row[2], row[3])

        with open(f"./games/GAME SESSION {code}/{target}/world_map.csv") as map_csv:
            map_reader = csv.reader(map_csv)
            map_dict = {}
            for i, row in enumerate(map_reader):
                if i > 0:
                    map_dict[row[0]] = tcw.WorldMapRegion(row[0],
                                                          row[1],
                                                          row[2],
                                                          row[3],
                                                          row[4],
                                                          list(row[5]),
                                                          row[6],
                                                          row[7],
                                                          row[8],
                                                          row[9],
                                                          row[10],
                                                          row[11],
                                                          row[12],
                                                          row[13]
                                                          )
        for key, value in map_dict.items():
            world.regions[key] = value
            world.navigation_graph[value.id] = value.edges

        with open(f"./games/GAME SESSION {code}/{target}/forces.csv") as force_csv:
            force_reader = csv.reader(force_csv)
            force_dict = {}
            for i, row in enumerate(force_reader):
                if i > 0:
                    force_dict[row[0]] = tcw.Force(row[0],
                                                   row[1],
                                                   row[2],
                                                   row[3],
                                                   row[4],
                                                   row[5],
                                                   row[6],
                                                   row[7],
                                                   row[8],
                                                   row[9])

        return tcw.Game(reg_dict, min_dict, dept_dict, world, uk, computer, press_dict, force_dict, code)


def exporter(game, code, clone=False):
    if clone:
        new_session = '00'
    else:
        new_session = str(int(last_session(code)) + 1).zfill(2)

    if clone:
        old_session = last_session(str(int(code) - 1).zfill(2))
    else:
        old_session = last_session(code)

    if clone:
        clone_code = str(int(code) - 1).zfill(2)
    else:
        clone_code = None

    os.mkdir(f"./games/GAME SESSION {code}/{new_session}")

    with open(f"./games/GAME SESSION {code}/{new_session}/regions.csv", "w") as reg_csv:
        reg_csv.write(f"id code,region name,population portion,government%,"
                      f"opposition%,liberal%,minor right%,minor left%\n")
        for i, entry in enumerate(game.reg_dict.values()):
            reg_csv.write(f"{entry.csv_rep()}")
            if i < len(game.reg_dict.values()) - 1:
                reg_csv.write("\n")

    if clone:
        min_code = clone_code
    else:
        min_code = code

    with open(f"./games/GAME SESSION {min_code}/{old_session}/ministers.csv") as old_min_csv:
        with open(f"./games/GAME SESSION {code}/{new_session}/ministers.csv", "w") as new_min_csv:
            for row in old_min_csv:
                new_min_csv.write(f"{str(row)}")

    with open(f"./games/GAME SESSION {code}/{new_session}/projects.csv", "w") as proj_csv:
        proj_csv.write(f"project id,project name,total cost,"
                       f"time remaining,outcome,secret?,completed?,ministry\n")
        master_project_list = []
        for dept in game.dept_dict.values():
            combined_projects = dept.active_projects + \
                                dept.active_secret_projects + \
                                dept.completed_projects + \
                                dept.completed_secret_projects
            master_project_list.extend(combined_projects)
        for i, project in enumerate(master_project_list):
            proj_csv.write(f"{project.csv_rep()}")
            if i < len(master_project_list) - 1:
                proj_csv.write("\n")

    with open(f"./games/GAME SESSION {code}/{new_session}/ministries.csv", "w") as dept_csv:
        dept_csv.write(f"id code,ministry name,minister title,minister,"
                       f"morale,budget,operating cost,experience,fatigue,morale drift")
        for i, entry in enumerate(game.dept_dict.values()):
            dept_csv.write(f"{entry.csv_rep()}")
            if i < len(game.dept_dict.values()) - 1:
                dept_csv.write("\n")

    with open(f"./games/GAME SESSION {code}/{new_session}/world_situation.csv", "w") as worldsit_csv:
        worldsit_csv.write(f"year,{game.world.year}\n"
                           f"day,{game.world.year_day}")

    with open(f"./games/GAME SESSION {code}/{new_session}/national_situation.csv", "w") as natsit_csv:
        natsit_csv.write(f"population,{game.uk.population}\n"
                         f"population health,{game.uk.population_health}\n"
                         f"stability,{game.uk.stability}\n"
                         f"government,{game.uk.government}\n"
                         f"monarch pronoun,{game.uk.monarch_pronoun}")

    with open(f"./games/GAME SESSION {code}/{new_session}/comp_stats.csv", "w") as comp_csv:
        comp_csv.write(f"secret project counter,{game.computer.secret_project_counter}\n"
                       f"runtime,{game.computer.runtime}")

    with open(f"./games/GAME SESSION {code}/{new_session}/the_press.csv", "w") as press_csv:
        press_csv.write(f"id,paper name,ideology,endorsement")
        for i, entry in enumerate(game.press_dict.values()):
            press_csv.write(f"{entry.csv_rep()}")
            if i < len(game.press_dict.values()) - 1:
                press_csv.write("\n")

    with open(f"./games/GAME SESSION {code}/{new_session}/world_map.csv", "w") as map_csv:
        map_csv.write(f"0 region code,1 region name,2 hemisphere,3 climate,4 terrain,5 borders,"
                      f"6 soviet dominance,7 US dominance,8 british dominance,9 crisis damage,"
                      f"10 soviet fortification,11 US fortification,"
                      f"12 UK fortification,13 ind fortification\n")
        for i, entry in enumerate(game.world.regions.values()):
            map_csv.write(f"{entry.csv_rep()}")
            if i < len(game.world.regions.values()) - 1:
                map_csv.write("\n")

    with open(f"./games/GAME SESSION {code}/{new_session}/forces.csv", "w") as force_csv:
        force_csv.write(f"force id,force name,land power,air power,"
                        f"sea power,morale,experience,quality,allegiance,location")
        for i, entry in enumerate(game.force_dict.values()):
            force_csv.write(f"{entry.csv_rep()}")
            if i < len(game.force_dict.values()) - 1:
                force_csv.write("\n")

    return [f"SESSION {code} SAVE {new_session} CREATED"]


def cloner(old_code, new_code):
    temp_game = importer(old_code)
    os.mkdir(f"./games/GAME SESSION {new_code}")
    save_string = exporter(temp_game, new_code, True)
    return [f"SESSION {new_code} CLONED FROM SESSION {old_code}\n{save_string}"]


def code_list():
    return [x.split()[2] for x in os.listdir("./games")]


def last_session(code):
    print(code)
    return str(max([int(x) for x in os.listdir(f"./games/GAME SESSION {code}")])).zfill(2)

