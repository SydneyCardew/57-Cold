import time

def difficulty_dict():
    return {0: "quotidian",
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


def political_movement_strength_dict():
    return {0.1: "almost undetectable",
            0.2: "very weak",
            0.3: "weak",
            0.4: "small but noticeable",
            0.5: "noticeable",
            0.6: "very noticeable",
            0.7: "distinct",
            0.8: "strong",
            0.9: "very strong",
            1.0: "dramatic"}


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


def local_time_of_day_greeting():
    time_of_day = int(time.strftime('%H', time.localtime()))
    if time_of_day >= 0 and time_of_day <= 11:
        return "MORNING"
    elif time_of_day >= 12 and time_of_day <= 5:
        return "AFTERNOON"
    else:
        return "EVENING"
