#Error-Unable to interprete by pthon- Errors are 3 types: 1.Compile Error 2.Logical Error 3.Runtime Error
#1.Compile error-SyntaxError
#2.Logical Error-No Syntax issue but expected will not come ex: odd/numbers finding logic is any number % 2==0, instead of 2 if you give any other number expected output will not come
#3.Runtime Error- No syntax and Logic issue but if a user provides invalid input Ex: instead int user enteres str
# To handle the runtime error we use exception handling.incase in my program have error don't throw error but dispaly given message by pass to next line

#Ex:1 Any error comes print following message
""" try:
    a=int(input("Enter first number: "))
    b=int(input("Enter second number: "))
    print("The value is: ",a/b)
except:
    print("Number cannot be divided by zero, provide valid number") """

#Handline multiple except blocks with specific error message
""" try:
    a=int(input("Enter first number: "))
    b=int(input("Enter second number: "))
    print("The value is: ",a/b)
except ZeroDivisionError:
    print("Number cannot be divided by zero, Provide valid numbers")
except ValueError:
    print("Albhabets not allowed, Enter valid numbers")
except:
    print("Check your code syntax") """
#Except blcok priority or orders of except block
# any error ocurred in try block any line python come out from that try block line and 
# check is there any except error handling message if 'yes' display that then move to next line else
# come out from try blcok throws error message
#Error Handling Flows Priority:
""" 
1. BaseException
2. Exception
3. StandardError
3a. ArithmeticError--> ZeroDivisionError
3b. EnvironmentError--< IOError, OSError
3c. RuntimeError
3d. LookupError--< IndexError, KeyError
3e. SyntaxError--> IndentationError """

#Error Handling with class and object:
""" try:
    a=int(input("Enter first number: "))
    b=int(input("Enter second number: "))
    print("The value is: ",a/b)
#except ZeroDivisionError as e:
    #print(e) # python pre-defined error message takes from class and object
except (ZeroDivisionError,ValueError) as e: 
    print(e)  """
#Error handling Using system library  no need to write mutilple error handling message
""" import sys
try:
    a=int(input("Enter first number: "))
    b=int(input("Enter second number: "))
    print("The value is: ",a/b)
#except ZeroDivisionError as e:
    #print(e) # python pre-defined error message takes from class and object
except:
    print(sys.exc_info()[0]) # pre-defined error class name as output """

#Standard try exception format: Critical logic only keep in try block remaining write outside of try block
""" a=int(input("Enter first number: "))
b=int(input("Enter second number: "))
try:
    result= a/b
except (ZeroDivisionError,ValueError) as e: 
    print(e)  # python pre-defined error message takes from class and object
else:
    print("The value of: ", result) # any error occured else will not run
 """
# file opration with try exception with else and finally block(even though if inside try logic failed don't go out from program, must be run finally block code)
""" filename=input("Entera filename: ")
try:
    fileobj=open(filename)
    read_content=fileobj.read() 
except (FileNotFoundError)as e:
    print(e)

else:
    print(read_content)
    fileobj.close()
finally:
    print("Even though any error occured/not in try block or error handling is there, must run this code") """

#Generate a error manually use "Raise" keyword
#Syntax: raise Error_name("customizable message")
num = int(input("Enter a number: "))
if (num<0):
    raise ValueError("Enter the number greater than one")
print(num)