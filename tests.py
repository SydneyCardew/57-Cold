from national_management_committee import Ministry
from statistics import mean
from random import seed
from random import randint


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


if __name__ == '__main__':
    rand_string()

