import sys
def displaysalary(salary):
    if salary < 0:
        raise ValueError("薪水為正")
    print("薪水"+str(salary))

try:
    Salary=eval(input('請輸入薪水'))
    displaysalary((Salary))
except OSError as err:
    print("OSError",format(err))
except ValueError:
    print("請輸入薪水為正")
except :
    print("Unexpected error:",sys.exc_info())
