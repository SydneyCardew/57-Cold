import os
import csv
import national_management_committee as nmc


def importer(code):
    """This code reads the csv files and turns them into game objects"""
    if code not in code_list():
        return None
    else:
        with open(f".\\games\\GAME SESSION {code}\\BEGIN\\regions.csv") as reg_csv:
            reg_reader = csv.reader(reg_csv)
            reg_dict = {}
            for i, row in enumerate(reg_reader):
                if i > 0:
                    reg_dict[row[0]] = nmc.Region(row[0], row[1])
        with open(f".\\games\\GAME SESSION {code}\\BEGIN\\ministers.csv") as min_csv:
            min_reader = csv.reader(min_csv)
            min_dict = {}
            for number, row in enumerate(min_reader):
                if number > 0:
                    min_dict[row[0]] = nmc.Minister(row[0], row[1], row[2], reg_dict[row[3]])
        with open(f".\\games\\GAME SESSION {code}\\BEGIN\\ministries.csv") as dept_csv:
            dept_reader = csv.reader(dept_csv)
            dept_dict = {}
            for number, row in enumerate(dept_reader):
                if number > 0:
                    dept_dict[row[0]] = nmc.Ministry(row[0], row[1], row[2], min_dict[row[3]])
        return nmc.Game(reg_dict, min_dict, dept_dict)


def code_list():
    return [x.split()[2] for x in os.listdir(".\\games")]

