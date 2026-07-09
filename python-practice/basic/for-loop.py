#A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).
#The for loop does not require an indexing variable to set beforehand. 
# to generate a sequence of numbers. use range(start, stop,step-size) 
# Execute still sequence(chain of characters, numbers,etc வரிசை) ends
#break(termnate) and continue(skip) statement works with loop iteration
#Syntax: for variable_name in sequence:
# String using for loop
""" a = "python learning"
for each_char in a:
  print(each_char)
 """
# List using for loop
""" food = ["idli", "dosai", "rice", "parota", "puri"]
for each_food_item in food:
   print(each_food_item) """

# Tuple values using for loop
""" food = ("idli", "dosai", "rice", "parota", "puri")
for each_tuple_element in food:
    print(each_tuple_element) """
# To generate a sequence of numbers
""" for seq_of_num in range(1,10,1):
    print(seq_of_num)  """

# Passing a string in range()
""" a = "python learning"
for i in range(len(a)):
    print(i, a[i]) """
# Passing a List in range()
""" food = ["idli", "dosai", "rice", "parota", "puri"]
for list_using_range in range(len(food)):
    print(list_using_range, food[list_using_range]) """
#1. Print 2 table using for loop
""" table_num = int(input("Enter a number to dispaly multiplication table"))
for i in range(1,table_num+1):
    #print(i," * 2 =",i*2)
    print(f"{i} * 2 = {i*2}") """

#2. Get input for number a and b. Print the number between a and b.
""" num_a = int(input("Enter Number1: "))
num_b = int(input("Enter Number2: "))
for i in range(num_a, num_b+1):
    print(f"Numbers between {num_a} and {num_b} are: {i}") """

#3. Print Even numbers between 1 to 10 
""" for i in range(1, 11):
    if (i % 2 == 0):
        print(i) """

#4.Count the Number of odd numbers between 1 to 10
""" count = 0
for i in range(1,11):
    if (i % 2 != 0):
        count=count+1
print(count) """

#5. Count the number which are divisible by 3 and 5 between 1 to 100
""" count = 0
for i in range(1,101):
    if (i % 3 == 0) and (i % 5 ==0):
        count=count+1
print(count) """

#6. Write a program to compute the sum of the first 5 nautural numbers(positive integers beginning at 1)
""" nat_num = int(input("Naturals numbers: "))
sum = 0
for i in range(1, nat_num+1):
    sum = sum + i 
print(sum) """
#7. Write a program to read 10 numbers from the keyboard and their sum and Avg
""" empty_list = []
key_input = int(input("Enter the number of terms: "))
sum = 0
for i in range(1,key_input+1):
    num = int(input(f"Enter your number{i}: "))
    empty_list.append(num)
for j in empty_list:
    sum = sum + j
print("Sum of Entered values are ",sum)
avg = sum/key_input
print("Average of Entered values are",avg) """
#8. Write a program to display n terms of natural numbers and their sum 
# Program to display n terms of natural numbers and their sum

""" # Input: number of terms
n = int(input("Enter the number of terms: "))

# Initialize sum
total_sum = 0

print("The first", n, "natural numbers are:")

# Loop through natural numbers
for i in range(1, n + 1):
    print(i, end=" ")
    total_sum += i

# Print the sum
print("\nThe sum of the first", n, "natural numbers is:", total_sum) """

#9. Write a program to display the cube of the number up to an integer.
""" key_input = int(input("Enter numbers: "))
for i in range(1,key_input+1):
    print(f"cube of the {i} is {i**3}") """

# Write a program to display week and day with nested for loop
""" for i in range(1, 5):
    print(f"Week{i}:")
    for j in range(1,8):
        print(f"Day{j}:")
 """
#Nested for loop withg List
""" food = ["idli", "dosai", "parota", "puri"]
flour = ['rice','wheat']
for item in food:
    for made_flour in flour:
        print(item, made_flour) """
        
#10 Write a program to display right angle triangle and inverted triangles using * symbol
""" for i in range (1,5+1):
    print()
    for j in range(1,i+1):
        print("*", end=" ")
 """

#11. Write a program to display Diamond-like triangle pattern

n = 5  # height of the top half

""" # Top half (increasing)
for i in range(1, n + 1):
    for j in range(i):
        print("*", end=" ")
    print()

# Bottom half (decreasing)
for i in range(n, 0, -1):
    for j in range(i):
        print("*", end=" ")
    print()
 """

# Inverted Right-angled triangle
""" print("Inverted Right-angled triangle:")
for i in range(n, 0, -1):
    for j in range(i):
        print("*", end=" ")
    print()  # move to next line """

# Inverted Left-angled triangle
""" print("\nInverted Left-angled triangle:")
for i in range(n, 0, -1):
    # print spaces first
    for j in range(n - i):
        print(" ", end=" ")
    # then print stars
    for k in range(i):
        print("*", end=" ") 
    print()  # move to next line"""
#With the break statement we can stop the loop before it has looped through all the items:
#Exit the loop when x is "banana":
""" fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break """

#The else keyword in a for loop specifies a block of code to be executed when the loop is finished:
#Print all numbers from 0 to 5, and print a message when the loop has ended.
""" for x in range(6):
  print(x)
else:
  print("Finally finished!") """

#Note: The else block will NOT be executed if the loop is stopped by a break statement.
#Break the loop when x is 3, and see what happens with the else block:
""" for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!") """

#With the continue statement we can stop the current iteration of the loop, and continue with the next:
#Continue to the next iteration if i is 3:
""" for i in range(5):
    if i ==3:
        continue
    else:
        print(i) """
# Print Even/Odd number but use for with If and else:
""" for i in range(15):
    if (i%2==0):
        print(i)
    else:
        print("Next odd numbers", i) """
