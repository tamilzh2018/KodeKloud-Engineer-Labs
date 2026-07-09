#The 'match' statement is used to perform different actions based on different conditions.
#Instead of writing many if..else statements, you can use the match statement.
#The match expression is evaluated once.
#The value of the expression is compared with the values of each case.
#If there is a match, the associated block of code is executed.
#syntax:
""" 
match expression:
  case x:
    code block
  case y:
    code block
  case z:
    code block 
    """
#Example
day = 4
match day:
  case 1:
    print("Monday")
  case 2:
    print("Tuesday")
  case 3:
    print("Wednesday")
  case 4:
    print("Thursday")
  case 5:
    print("Friday")
  case 6:
    print("Saturday")
  case 7:
    print("Sunday")