from national_management_committee import Ministry
from national_management_committee import World
from national_management_committee import WorldMapRegion
from military_systems import breadth_first_search
from statistics import mean
from random import seed, randint, choice
import re
import time
import csv


def spread():
    results_dict = {x: {y: [] for y in range(11)} for x in range(1, 101)}
    for repeats in range(100):
        for morale in range(100, 0, -1):
            for diff in range(11):
                test_ministry = Ministry('Department of Testing', morale, 500, 20, 20)
                outcome = test_ministry.action(diff, 10, True, True)
                results_dict[morale][diff].append(outcome.outcome_score)
    aggregate = {x: {y: [round(mean(results_dict[x][y]))] for y in results_dict[x]} for x in results_dict}
    with open('.\\experiments\\test.csv', "w") as csv_test:
        csv_test.write(f",0,1,2,3,4,5,6,7,8,9,10,\n")
        for morale, results in aggregate.items():
            new_row = f"{morale},"
            for entry in results.values():
                new_row += f"{str(entry[0])},"
            csv_test.write(f"{new_row}\n")


def rand_string():
    seed()
    test_ministry = Ministry('Department of Testing', 75, 500, 20, 20)
    outcome = test_ministry.action(randint(0, 10), 10, True, True)
    print(outcome.a_string)


def command_split():
    comstring = 'act d6 "test project description" 5 30 50 --xd'
    in_args = " ".join(comstring.split()[1:])
    match = re.match(r'(\S+)\s+(\".*?\")\s+(.*)', in_args)
    if match:
        result = [match.group(1).split() + [match.group(2)] + match.group(3).split()]
        print(result)
    else:
        print(comstring.split())


def time_string():
    print(time.strftime('%H', time.localtime()))


def graph_test():
    with open(f".\\games\\GAME SESSION 00\\00\\world_situation.csv") as worldsit_csv:
        worldsit_reader = csv.reader(worldsit_csv)
        worldsit_dict = {}
        for row in worldsit_reader:
            worldsit_dict[row[0]] = row[1]
        world = World(int(worldsit_dict['year']),
                      int(worldsit_dict['day']))
        with open(f".\\games\\GAME SESSION 00\\00\\world_map.csv") as map_csv:
            map_reader = csv.reader(map_csv)
            map_dict = {}
            for i, row in enumerate(map_reader):
                if i > 0:
                    map_dict[row[0]] = WorldMapRegion(row[0],
                                                      row[1],
                                                      row[2],
                                                      row[3],
                                                      row[4],
                                                      list(row[5]),
                                                      row[6],
                                                      row[7],
                                                      row[8],
                                                      row[9]
                                                      )
        for key, value in map_dict.items():
            world.regions.append(value)
            world.navigation_graph[value.id] = "".join(value.edges).split(",")
    cell_list = [x for x in map_dict.keys()]
    for x in range(20):
        start = choice(cell_list)
        destination = choice(cell_list)
        print(start, destination)
        print(breadth_first_search(world.navigation_graph, start, destination))


if __name__ == '__main__':
    graph_test()
