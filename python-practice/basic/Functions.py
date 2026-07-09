# A function is a block of code which only runs when it is called.A function can return data as a result.A function helps avoiding code repetition. 
# A function name must start with a letter or underscore
# A function name can only contain letters, numbers, and underscores
# Function names are case-sensitive (myFunction and myfunction are different)

#Example:
def my_function():
  print("Hello from a function")

my_function() #To call a function, write its name followed by parentheses:You can call the same function multiple times:

#Functions can send data back to the code that called them using the 'return' statement.If a function doesn't have a return statement, it returns None by default.
#A function that returns a value:
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#Parameters vs Arguments
""" 
The terms parameter and argument can be used for the same thing: information that are passed into a function.
From a function's perspective: Are we sending an actual value(Argument) or a variable(parameter) into a function ?உண்மையான மதிப்பை அல்லது மாறியை அனுப்புகிறோமா
By default, a function must be called with the correct number of arguments.If you try to call the function with the wrong number of arguments, you will get an error:However, sometimes you may not know how many arguments that will be passed into your function.
*args and **kwargs[keyword arguments] allow functions to accept a unknown number of arguments.
You can assign default values to parameters. If the function is called without an argument, it uses the default value: def my_function(name = "friend"):
You can send arguments with the key = value syntax. def my_function(animal, name): my_function(animal = "dog", name = "Buddy")

"""
#Unpacking Arguments: The * and ** operators can also be used when calling functions to unpack (expand) a list or dictionary into separate arguments.
#Using * to unpack a list into arguments:
def my_function(a, b, c):
  return a + b + c

numbers = [1, 2, 3]
result = my_function(*numbers) # Same as: my_function(1, 2, 3)
print(result)
