import sys

def func1():
    commands = len(sys.argv)
    if commands == 2:
        name = sys.argv[1]
    elif commands == 3:
        name = sys.argv[2]
    print("hello {}".format(name))

def func2():
    print("Yep!")
    print("That did it!")

def func3():
    print("Oh my...")
    print("It seems you git this down!")
    print("Congrats!")

if __name__ == '__main__':
    if sys.argv[1] == "func1":
        func1()
    if sys.argv[1] == "func2":
        func2()
    if sys.argv[1] == "func3":
        func3()



# import datetime
# import calendar

# today = str(datetime.date.today())
# today = today.split("-")
# print(today[1])
# month = calendar.month_abbr[int(today[1])]

# print(month)