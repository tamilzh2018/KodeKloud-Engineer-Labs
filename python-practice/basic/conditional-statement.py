#Conditions can be used in several ways, most commonly in "if statements" and loops.If Condition met do this else do that
#The if statement evaluates a condition (an expression that results in True or False). If the condition is true, the code block inside the if statement is executed. If the condition is false, the code block is skipped.
#Python can evaluate many types of values as True or False in an if statement.
#Zero (0), empty strings (""), None, and empty collections are treated as False. Everything else is treated as True.
#This includes positive numbers (5), negative numbers (-3), and any non-empty string (even "False" is treated as True because it's a non-empty string).
#Short Hand If:If you have only one statement to execute, you can put it on the same line as the if statement.
# Example
"""
  = 5 
b = 2
if a > b: print("a is greater than b") """

#pass Statement
# if statements cannot be empty, but if you for some reason have an if statement with no content, put in the pass statement to avoid getting an error. if b > a:   pass
""" 
Python supports the usual logical conditions from mathematics:

Equals: a == b
Not Equals: a != b
Less than: a < b
Less than or equal to: a <= b
Greater than: a > b
Greater than or equal to: a >= b """


#1. Get user input for Variable mark, if mark> 35 then print Pass  else print Fail
""" mark = int(input("Enter your mark: "))

if (mark > 35):
    print("Pass")
else:
    print("Fail") """

#2. Get input for a number and check whether it is divisible by both 3 and 5 or not. If yes then print,
# the number is divisible by 3 and 5 else print the number is not divisible by 3 and 5.
""" number = int(input("Enter a Number: "))

if (number % 3 == 0 and number % 5 == 0):
    print("Given Number is Divisble by 3 and 5")
else:
    print("Given Number is not Divisible by 3 and 5") """

#3. Get input for a number and find it is even or odd
""" number = int(input("Enter a number: "))

if (number % 2 == 0):
    print("Even Number")
else: 
    print("Odd Number") """
#4. Get input for score out of 100, if score is <= 35 "Poor Student", if score > 35 but < 70 "Average Stundent"
# if score is > 70 "Good Student".
""" score = int(input("Enter your mark: "))

if (score <= 35):
    print("Poor Student")
elif (score > 35 and score <= 70):
    print("Average Student")
else:
    print("Good Student") """

#5. Get input for salary and age. if salary >= 20000 or age <= 25 then get input for required loan amount. if not print You are not eligible to get a loan.
# if required loan amount is <= 50000 then print we will process your loan amount. if it is > 50000 then print we cannot process above 50000 loan.
""" salary = int(input("Enter your salary: "))
age = int(input("Enter your age: "))

if (salary >= 20000) and (age <= 25):
    loan_amount = int(input("Enter your required loan amount: "))
    if (loan_amount <= 50000):
        print("We will process your loan amount")
    else:
        print("We cannot process not more than 50000 laon amount")

else:
    print("You are not eligible to get a loan") """

#6. Get input for 5 subjects marks. Add all of it, and find average.if avg mark is < 35 . Additional Class is required. else print "you are good to go "
# Program to calculate average marks of 5 subjects
# and decide if additional class is required

""" num_sub = int(input("Enter number of Subjects: "))
total = 0
for i in range(1, num_sub+1):
    mark = int(input(f"Enter your mark of subject{i}: "))
    total = total + mark
# Calculate average
average = total / num_sub

# Decision based on average
if average < 35:
    print("Additional class is required")
else:
    print("You are good to go")
 """
#7.Given an integer, n, perform the following conditionals actions: if 'n' is odd, print Weird, if 'n' is even and in the inclusive range 2 to 5, print not Weird, if range above 6 to 20, Print Weird,  if range > 20 print Not Weird.
num = int(input("Enter a number: "))

if num % 2 != 0:
    print("Odd Number Weird")
elif num in range(2, 6):   # 2, 3, 4, 5
    print("Even Number Not Weird")
elif num in range(6, 21):  # 6 through 20
    print("Even Number Weird.")
else:  # num > 20
    print("Even Number Not Weird.Above 20 ")




