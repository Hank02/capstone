# def func1():
#     print("hello 1")

# def func2():
#     print("Yep!")
#     print("That did it!")

# def func3():
#     print("Oh my...")
#     print("It seems you git this down!")
#     print("Congrats!")

import datetime
import calendar

today = str(datetime.date.today())
today = today.split("-")
print(today[1])
month = calendar.month_abbr[int(today[1])]

print(month)