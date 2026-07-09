#comprehension:-new list and append operation ease can do
""" # syntax: expression for item in iterables
letters=[char for char in 'python']
print(letters)
new_list=[num for num in range(1,11)]
print(new_list)
# syntax: expression for item in iterables if condn
even_num=[even for even in range(1,51) if even%2==0]
print(even_num)
#logic gate and/or operator
gate_operation=[big for big in range(1,51) if big%2==0 if big%3==0]
print(gate_operation) """
# syntax: expression if condition else statement for item in iterables
""" even_odd=[even if even%2==0 else 'odd_numbers' for even in range(1,11)]
print(even_odd) """
#list comprehension with fucntion
""" def square(x):
    return x*x
list4=[2,3,4,5,6]
square_value=[square(x) for x in list4]
print(square_value) """
#Nested list with comprehension:
# Read nested list comprehensions from left to right as nested for loops.[x for row in matrix for x in row]
#syntax: [expression for item1 in iterable1 for item2 in iterable2 ... if condition]
""" [expression
 for item1 in iterable1
 for item2 in iterable2
 ...
 if condition]

This is equivalent to:
result = []
for item1 in iterable1:
    for item2 in iterable2:
        if condition:
            result.append(expression) """

""" nest_list=[[1,2,3,4],[5,6,7,8]]
indexing_value=[x[1] for x in nest_list]
print(indexing_value)

#Simple example (2D combinations).Order matters: the leftmost for is the outer loop.
pairs = [(x, y) for x in [1, 2, 3] for y in [4, 5]]
print(pairs) #[(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)]
#Nested list comprehension for matrices (flattening)
matrix = [[1, 2, 3], [4, 5, 6]]

flat = [num for row in matrix for num in row]
print(flat)#[1, 2, 3, 4, 5, 6] """

#Multiple conditions
""" results = [
    (x, y)
    for x in range(5) #0,1,2,3,4
    for y in range(5) #0,1,2,3,4
    if x != y and (x + y) % 2 == 0
]
print(results) #[(0, 2), (0, 4), (1, 3), (2, 0), (2, 4), (3, 1), (4, 0), (4, 2)] """
#built-in function operation with comprehension
str1="alpha1234"
str2="hai"
alphabet=[x for x in str1 if x.isalpha()]
numbers=[num for num in str1 if num.isdigit()]
case_change=[char.upper() for char in str2 ]
print(alphabet)
print(numbers)
print(case_change)