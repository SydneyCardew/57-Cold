from dataclasses import dataclass


class Clock:
    """This class handles all functions to do with storing, retrieving and calculating dates"""
    def __init__(self, year, day):
        self.year = year
        self.year_day = day
        self.week_days = ("Friday",
                          "Saturday",
                          "Sunday",
                          "Monday",
                          "Tuesday",
                          "Wednesday",
                          "Thursday")
        self.month_ids = {
            1: {'days': 31, 'name': 'January', 'code': 'JAN'},
            2: {'days': (28, 29), 'name': 'February', 'code': 'FEB'},
            3: {'days': 31, 'name': 'March', 'code': 'MAR'},
            4: {'days': 30, 'name': 'April', 'code': 'APR'},
            5: {'days': 31, 'name': 'May', 'code': 'MAY'},
            6: {'days': 30, 'name': 'June', 'code': 'JUN'},
            7: {'days': 31, 'name': 'July', 'code': 'JUL'},
            8: {'days': 31, 'name': 'August', 'code': 'AUG'},
            9: {'days': 30, 'name': 'September', 'code': 'SEP'},
            10: {'days': 31, 'name': 'October', 'code': 'OCT'},
            11: {'days': 30, 'name': 'November', 'code': 'NOV'},
            12: {'days': 31, 'name': 'December', 'code': 'DEC'}
            }
        self.month_number = 0
        self.year_calculation()
        self.date_calculation()
        self.time = self.get_date()

    def tick(self):
        """Advances the clock one day"""
        self.year_day += 1
        if self.year_day > self.year_day_maximum:
            self.year_day = 1
            self.year += 1
            self.year_calculation()
        self.time = self.get_date()

    def get_date(self):
        self.date_calculation()
        return Time(self.year_day, self.month_number, self.month, self.date, self.year)

    def date_calculation(self):
        """This function takes the day of the year (self.year_day)
        and calculates the date, month and day of the week"""
        month_finder = [(x, y['days']) if isinstance(y['days'], int)
                        else ((x, y['days'][1]) if self.leap_year
                        else (x, y['days'][0]))
                        for x, y in self.month_ids.items()]
        day_temp = self.year_day
        for months in month_finder:
            day_temp_two = day_temp
            day_temp -= months[1]
            if day_temp < 0:
                self.date = day_temp_two
                self.month = self.month_ids[months[0]]
                break
            self.month_number = months[0]
        day_index = self.jan_one_day
        for x in range(1, self.year_day):
            day_index += 1
            if day_index == 7:
                day_index = 0
        self.week_day = self.week_days[day_index]

    def year_calculation(self):
        """This routine works out if the current year is a leap year and what day of the week
        January 1st of the current year is, based on the Gregorian calendar."""
        leap_years_since_1582 = (i for i in range(1583, self.year) if i % 4 == 0 and i % 100 != 0 or i % 400 == 0)
        days_to_year_start = ((self.year - 1582) * 365) + len(list(leap_years_since_1582)) + 78
        self.jan_one_day = (days_to_year_start % 7) - 1
        self.leap_year = True if self.year % 4 == 0 and self.year % 100 != 0 or self.year % 400 == 0 else False
        self.year_day_maximum = 366 if self.leap_year else 365


@dataclass
class Time:
    year_day: int
    month_number: int
    month: None
    date: int
    year: int
