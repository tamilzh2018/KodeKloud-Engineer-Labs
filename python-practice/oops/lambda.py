#Anynomous Function(lambda)
#syntax: result=lambda args(optional)= expression(actual operational logic)
#def =lambda
#paramters=args
""" def add(a,b):
    return a+b
normal_result=add(4,5)
print(normal_result) """

#convert normal function to lambda
""" result=lambda a,b: a+b
print(result(4,5)) #calling the lambda function
 """
#string operation
""" str1="lambda conversion"
upper=lambda args:args.upper()
result=upper(str1)
print(result)
 """
# usage of lambda function in user defined and high order function
#non pre-defined argumets operation
""" add=lambda *args: sum(args)
print(add(2,3,4,5)) """

#immediately invoke funtion expression(iife)-defined and executed immediately
""" result=(lambda a,b:a*b)(2,3)
print(result) """

#list of numbers squared value use for loop with lambda
""" list1=[5,8,7,9,10]
new_list=[]
for i in list1:
    result=lambda i:i**2
    new_list.append(result(i)) #caling the lambda
print("Squared value of list1: ",new_list) """

#user defined fuction with lambda
""" def func(x):
    return (lambda y: x*y)
result=func(5) #function cal and recieve value 
print(result(9)) #lambda caling """
#High order functio with lambda
#A function in Python with another function as argument or returns a finction as an output
""" ✔ Passing a function as an argument → higher-order function
✔ Returning a function → higher-order function
✔ Lambdas are commonly used for short functional behavior """
""" high_order=lambda x,func : x+func(x) #lambda receive 2 arguments
print(high_order(20, lambda x: x * x)) #one argument is 20 another one is another lambda x:x*x """

#Map Function(Transform each element):Use when you want to modify each element.Syntax: result=map(function_name, iterables)
""" def add(a):
    return a+a
iterable_num=[2,3,8,9,12]
result=map(add,iterable_num) #returns map object
#with lambda
result1=map(lambda a:a+a,iterable_num) #returns map object 
print(list(result))
print(list(result1)) """

#Filter Function(Select elements): Use when you want to remove unwanted elements.Syntax: result=filter(functiona_name,iterables)
#Key Rule for filter():-Function must return True(keep element) or False(discard element)
""" def even(num):
    return num%2==0 
iter_nums=[2,3,8,9,12]
even_num=filter(even,iter_nums) #returns filter object
#with lambda
even_lambda=filter(lambda num:num%2==0,iter_nums)
print(list(even_num))
print(list(even_lambda)) """
#Reduce Function(Combine elements into one):Use when you want to aggregate values.Syntax: result=reduce(functiona_name,iterables). import library: from functools import reduce
#Repeatedly applies a function to reduce iterable to a single value.
""" from functools import reduce
def reduce_fuc(a,b):
    return a*b
iter_values=[2,3,8,9,12] 
result=reduce(reduce_fuc,iter_values)
result_lamda=reduce(lambda a,b:a*b,iter_values)
print(result)
print(result_lamda) """

#operate() and accumulate()
#instead of lambda we can use operaotor() with reduce()for aruthmetic operation
from functools import reduce
import operator
list1=[2,3,8,9,12] 
list2=["Hai", " How are you "]
add_result=reduce(operator.add,list1)
mul_result=reduce(operator.mul,list1)
str_concat=reduce(operator.concat,list2)
print(add_result)
print(mul_result)
print(str_concat)

#instead of reduce(),we can use accumulate(), also we can get middle value not only aggregate value
#syntax: accumulate(iterables,function_name)
from itertools import accumulate
from functools import reduce
list3=[2,3,8,9,12]
result=accumulate(list3, lambda x,y:x+y)
result_reduce=reduce(lambda x,y:x+y, list3)
print("Accumulate Method: ",list(result))
print("Reduce Method: ",result_reduce)