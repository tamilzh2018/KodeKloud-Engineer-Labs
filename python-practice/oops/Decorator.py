#A Python decorator is a function that wraps another function to extend or modify its behavior without changing the original function’s code.
#A function is passed to another function, modified, and returned as a new function.
#Nested Funtion
""" def outer_fun():
    msg1="Hi "
    def inner_fun():
        msg2="How are you"
        msg=msg1+msg2
        return msg 
    return inner_fun #return's memory address
var=outer_fun() #calling outer function
print(var) #display memory value
print(var()) #calling inner function """
#pass a fcuntion as ref
""" def add(x,y):
    return x+y
def dispaly(func,x,y):#receiving parameters
    return func(x,y) #calling memory address
result=dispaly(add, 4,6) #calling display function and passing 3 parameters like memory address of add, 4,6
print(result) """

#return function as value
""" def greeting(name):
    def hai():
        return "Hello, " + name
    return hai
call=greeting('Raj')
print(call()) """

#Nested function,Return a function to another function,Pass a function as Referrence
#manual decorator pattern in Python
#A function is passed to another function, modified, and returned as a new function.
""" Key Concepts Demonstrated
✔ Functions are first-class objects (can be passed as arguments)
✔ Nested functions
✔ Closures (inner function remembers ref)
✔ Manual implementation of a decorator """
""" def decorate_fuc(ref): #receive another function 
    def process():  # nested function
        mem_store = ref()   # call the original function
        return mem_store.upper()  # modify its result, converts it to uppercase
    return process  # return the new function not calling

def original_fuc():
    return 'Orginal statement'

output = decorate_fuc(original_fuc)  # Pass function as argument
print(output())  # Call the returned function(process) """

#Why this is called a Decorator Because It adds extra behavior (uppercase).Without changing original_fuc code
#Closure is a nested function that allows to access variables of the outer function.Even after the outer function closed

#Decorator Types: function decorator, Class decorator, method decorator(inside class )
#single function decorator
""" def decorate_fuc(ref): #receive another function 
    def process():  # nested function
        mem_store = ref()   # call the original function
        return mem_store.upper()  # modify its result, converts it to uppercase
    return process  # return the new function not calling
@ decorate_fuc
def original_fuc():
    return 'Orginal statement'
print(original_fuc()) """
#Multiple decorator
""" def decorate_fuc(ref): #receive another function 
    def process():  # nested function
        mem_store = ref()   # call the original function
        return mem_store.upper()  # modify its result, converts it to uppercase
    return process  # return the new function not calling
def multi_decorate_fuc(ref):
    def process2():
        mem_store= ref()
        return mem_store.split()
    return process2
@multi_decorate_fuc
@ decorate_fuc
def original_fuc():
    return 'Orginal statement'

# output = multi_decorate_fuc(decorate_fuc(original_fuc))  # Pass function as argument
# print(output())  # Call the returned function(process)
print(original_fuc()) """
#Accept a parameter inside decorator
""" def pass_param(val):
    def decorate_fuc(ref): #receive another function 
        def process():  # nested function
            mem_store = ref()   # call the original function
            return mem_store.upper() + val # modify its result, converts it to uppercase
        return process  # return the new function not calling
    return decorate_fuc
var = input("Enter your name: ")
@ pass_param(var)

def original_fuc():
    return 'Orginal statement '
print(original_fuc()) """
#Use a decorator for specified task Ex:Handle zero divsion error via decorator
""" def div_decor(ref):
    def cal(x,y): #defined parameters 2
        if y==0:
            return 'Enter other than zero'
        return ref(x,y)
    return cal
@ div_decor
def original_div(a,b):
    return a/b
print(original_div(8,7)) """
#Use single decorator for multiple function
""" def div_decor(ref):
    def cal(*args): #num of parameters undefined
        if 0 in args[1:]: #slicing concept
            return 'Enter other than zero'
        return ref(*args)
    return cal
@ div_decor
def original_div(a,b):
    return a/b
print(original_div(8,9))

@ div_decor
def original_div(a,b,c):
    return a/b/c
print(original_div(8,7,0)) """
#Call method in python
""" class Cal:
    def __init__(self):
        
        print('constructor init method')
    def __call__(self, *args, **kwds):
        print('call Method')
        
obj=Cal() #when object creates then init starts work
obj() #instead of using obj.class name to call any method, we can use obj()  """

#Class decorator
""" class Decor_class:
    def __init__(self,function):
        self.function=function
        print('constructor init method')
    def __call__(self):
        self.function()
        print('call Method')
@Decor_class
def function():
    print("manual class decorator")
        
# obj=Decor_class(function) #when object creates then init starts work
# obj()
function() """
#Class Decorator with return value
""" class demo:
    def __init__(self,func):
        self.func=func
        
    def __call__(self, a,b):
        val=self.func(a,b)
        return val + 6
@demo
def mul_fuc(a,b):
    return a*b
print(mul_fuc(4,5)) """

#Method decorator(inside class)
