import os
import csv
import national_management_committee as nmc
import the_cold_world as tcw


def importer(code):
    """This code reads the csv files and turns them into game objects"""
    if code not in code_list():
        return None
    else:

        with open(f".\\games\\GAME SESSION {code}\\00\\regions.csv") as reg_csv:
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

        with open(f".\\games\\GAME SESSION {code}\\00\\ministers.csv") as min_csv:
            min_reader = csv.reader(min_csv)
            min_dict = {}
            for i, row in enumerate(min_reader):
                if i > 0:
                    min_dict[row[0]] = nmc.Minister(row[0], row[1], row[2], reg_dict[row[3]])

        with open(f".\\games\\GAME SESSION {code}\\00\\projects.csv") as proj_csv:
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
                                                             True if row[6] == 'Y' else False,
                                                             True)

        with open(f".\\games\\GAME SESSION {code}\\00\\ministries.csv") as dept_csv:
            dept_reader = csv.reader(dept_csv)
            dept_dict = {}

            for i, row in enumerate(dept_reader):
                if i > 0:
                    public_proj_active = [x for x in [combined_proj_dict[row[0]]] if not x.secret and not x.completed]
                    secret_proj_active = [x for x in [combined_proj_dict[row[0]]] if x.secret and not x.completed]
                    public_proj_complete = [x for x in [combined_proj_dict[row[0]]] if not x.secret and x.completed]
                    secret_proj_complete = [x for x in [combined_proj_dict[row[0]]] if x.secret and x.completed]
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

        with open(f".\\games\\GAME SESSION {code}\\00\\world_situation.csv") as worldsit_csv:
            worldsit_reader = csv.reader(worldsit_csv)
            worldsit_dict = {}
            for row in worldsit_reader:
                worldsit_dict[row[0]] = row[1]
            world = tcw.World(int(worldsit_dict['year']),
                              int(worldsit_dict['day']))

        with open(f".\\games\\GAME SESSION {code}\\00\\national_situation.csv") as natsit_csv:
            natsit_reader = csv.reader(natsit_csv)
            natsit_dict = {}
            for row in natsit_reader:
                natsit_dict[row[0]] = row[1]
            uk = nmc.UK(natsit_dict['population'],
                        natsit_dict['population health'],
                        natsit_dict['stability'],
                        natsit_dict['government'],
                        natsit_dict['monarch pronoun'])

        with open(f".\\games\\GAME SESSION {code}\\00\\comp_stats.csv") as comp_csv:
            comp_reader = csv.reader(comp_csv)
            comp_dict = {}
            for row in comp_reader:
                comp_dict[row[0]] = row[1]
            computer = nmc.Computer(comp_dict['secret project counter'],
                                    comp_dict['runtime'])

        with open(f".\\games\\GAME SESSION {code}\\00\\the_press.csv") as press_csv:
            press_reader = csv.reader(press_csv)
            press_dict = {}
            for i, row in enumerate(press_reader):
                if i > 0:
                    press_dict[row[0]] = nmc.Paper(row[0], row[1], row[2], row[3])

        with open(f".\\games\\GAME SESSION {code}\\00\\world_map.csv") as map_csv:
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
            world.regions.append(value)
            world.navigation_graph[value.id] = "".join(value.edges).split(",")

        with open(f".\\games\\GAME SESSION {code}\\00\\forces.csv") as force_csv:
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

        return tcw.Game(reg_dict, min_dict, dept_dict, world, uk, computer, press_dict, force_dict)


def exporter(game):
    pass


def code_list():
    return [x.split()[2] for x in os.listdir(".\\games")]


def last_session(code):
    return str(max([int(x) for x in os.listdir(f".\\games\\GAME SESSION {code}")])).zfill(2)

