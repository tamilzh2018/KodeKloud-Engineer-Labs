#1. Get input for variable name, age and address.Print it.
""" name = input("Enter your name: ")
age = int(input("Enter your age: "))
address = input("Enter your address: ")
print(f"Name: {name}, Age: {age}, Address: {address}") """

#2. Get two numbers from user and print their sum, difference, product and division.
""" num1 = int(input("Enter Number1: "))
num2 = int(input("Enter Number2: "))
def add(num1, num2):
    reterms num1 + num2

def sub(num1, num2):
    reterms num1 - num2

def mul(num1, num2):
    reterms num1 * num2

def div(num1, num2):
    reterms num1 / num2

def mod(num1, num2):
    reterms num1 % num2

def flor(num1, num2):
    reterms num1 // num2

add = add(num1, num2)
sub = sub(num1, num2)
mul = mul(num1, num2)
div = div(num1, num2)
mod = mod(num1, num2)
flor = flor(num1, num2)

print(f"Addition value: {add}, Subtraction value: {sub}, Mulitiplication vlaue: {mul}, Division value: {div}, Modulus value: {mod}, floor division value: {flor}") """

# Get Input for Variable name, score, department
# Get score for 100
# Divide 100/10
""" name = input("Enter your Name: ")
score = int(input("Enter your score: "))
department = input("Which Department from: ")

def div():
    reterms score/10
div = div()
print(f"Name: {name}, Score: {div}/10, Department: {department}")   """

#1. How to find a number is postive or not
""" num = int(input("Enter a number: "))
if num>0:
    print('Entered Number is Positve Number: ', num)
else:
    print("Entered Number is Negative Number: ", num) """

#2. Find Odd or Even Numbers in Range of Numbers
""" start=int(input("Enter the starting number: "))
stop=int(input("Enter the Ending Number: "))
for i in range(start, stop+1):
    if (i%2==0):
        print("Entered Number is Even: ",i)
    else:
        print("Entered Number is Odd: ",i) """
#3. Identifying Vowels
""" vowels='aeiouAEIOU'
identify = input("Enter an alphabet: ")

if not identify.isalpha():
    print("Numbers not allowed")      
elif len(identify) != 1:
    print("Please enter a single alphabet character.")
else:
    if identify in vowels:
        print("vowel character")
    else:
        print("consonant character")
 """

""" ch = input("Enter a char:")
if ch=='a' or ch=='e' or ch=='i' or ch=='o' or ch=='u' or ch=='A' or ch=='E' or ch=='I' or ch=='O' or ch=='U':
    print(ch, 'is vowels')
else:
    print(ch, 'is not vowels') """

# finding given character is alphabet or not
""" identify = input("Enter an alphabet: ")

if identify.isalpha():
    print(identify, "is an alphabet")
elif identify.isdigit():
    print("Numbers not allowed. Enter only alphabet.")
else:
    print("Symbols not allowed. Enter only alphabet.") """

#Finding Average of N Numbers
""" num = int(input('Enter the numbers to find avg: '))
list1 = []

for i in range(1, num + 1):
    list1.append(int(input(f"Enter your {i} number: ")))

avg = sum(list1) / num
print("Average:", avg) """

#print all numbers in a range that are divisible by given number
""" start = int(input("Enter the starting Number: "))
stop = int(input("Enter the ending Number: "))
division_num = int(input("Enter the Number to be Divided: "))
for i in range(start, stop+1):
    if (i%division_num)==0:
        print("Divisible numbers is: ", i) """
# Finding a Grade of a Student
""" subjects=int(input("Enter number of Subjects: "))
sub_list=[]

for sub in range(subjects):
    sub_list.append(int(input(f"Enter the subject {sub} marks: ")))

grade=sum(sub_list)/subjects
if grade<60:
    print("Grade 4 student")
elif grade>=60 and grade<70:
    print("Grade 3 student")
elif grade>=70 and grade<80:
    print("Grade 2 student")
else:
    print("grade 1 Student") """

#Swapping of Two numbers with and without temporary variable
""" num1 = int(input("Enter number x: "))
num2 = int(input("Enter number y: "))
#swap = num1
#num1 = num2
#num2 = swap
#print("With Swapping variable: ", num1, num2) 
num2,num1= num1, num2
print("Without swpapping variable: ", num1, num2) """

# Multiplication  Table
""" mul_tab=int(input("Enter Number: "))
for i in range(1,20+1):
    print(f"{i} * {mul_tab} =", i*mul_tab) """

# Conversions km to miles vicwe versa 1km = 0.6217 miles
""" kms=int(input("Enter your walked distance today in kilo-metres: "))
miles=kms*0.6217
#kms=miles/0.6217
print("Today you walked miles is: ", miles) """
# Celsius to Fahrenheit Conversion 1 faren=(cel*1.8)+32
""" faren = int(input("Enter farenheit value: "))
celsius=(faren-32)/1.8
print(celsius) """
# How to find Area of Triangle semi-perimeter=a+b+c/2 area=s(s-a)*(s-b)*(s-c)**0.5
""" a= int(input("Enter side a: "))
b= int(input("Enter side b: "))
c= int(input("Enter side c: "))
s= (a+b+c)/2
print("Semi-Perimeter value is: ", s)
area=s*(s-a)*(s-b)*(s-c)**0.5
print("Area of triangle is: ",area) """
# How to find Largest among three inputs
""" a= int(input("Enter first number: "))
b= int(input("Enter second number: "))
c= int(input("Enter third number: "))

if a>=b and a>=c:
    print("Largest number is:",a)
elif b>=a and b>=c:
    print("Largest number is:",b)
else: 
    print("Largest number is:",c)

#altermethod: max()
d= max(a,b,c)
print("largets number is:", d) """
# Find sum of Natural numbers means if number  > 0 natural
""" num_terms=int(input("Enter numbers terms: "))
sum = 0
if num_terms>0:
    for sum_natural in range(1,num_terms+1):
        sum = sum+sum_natural
        #sum += sum_natural
print(f"Sum of this natural: {sum}") """

#Find Factorial of a Number Ex: 5! = 5*4*3*2*1 =120 logic here Start with the given number, multiply it by each whole number in descending order down to 1, and take the final product as the result.
""" fact_num=int(input("Enter numbers to find factorial: "))
factorial=1
for i in range(fact_num,0,-1):
    factorial=factorial*i
print(f"Factorial of {fact_num} is: {factorial}")
#while loop
while fact_num>0:
    factorial=factorial*fact_num 
    fact_num=fact_num-1
    
print(f"Factorial value is: {factorial}") """
    
#How to generate Fibonacci Series: sequence of numbers where each number after the first two is the sum of the two preceding ones. Ex:F(0) = 0, F(1) = 1 ,then F(2) = F(1) + F(0) = 1 + 0 = 1
""" fib_num = int(input("Enter number to find Fibnacci: "))
f0,f1 = 0,1
if fib_num<=0:
    print("Enter the postive numbers")
elif fib_num==1:
    print(f"Fibonacci Series of {fib_num} is :{f0}")
else:
    for i in range(fib_num):
        print(f0, end=",")
        f0,f1 = f1,f0+f1

# while
    counter=0
    while counter<fib_num:
        print(f0, end=",")
        f0,f1 = f1,f0+f1
        counter+=1 """
#How to find whether a year is leap year or not:Divisible by 400 but not by 100 and divisible by 4 is leap year
""" get_year=int(input("Enter a year: "))
if (get_year%4==0) and (get_year % 400 == 0) or (get_year % 100 != 0):
    print("Leap year")
else:
    print("Not a leap year") """

#How to find whether a string is palindrome or not A palindrome is a number/string that reads the same forward and backward. Ex:121, madam
""" palindrome = input("Enter a string to find palindrome: ")

# Make it case-insensitive
palindrome_clean = palindrome.lower()

rev = palindrome_clean[::-1]

if palindrome_clean == rev:
    print("Entered string is Palindrome")
else:
    print("Not Palindrome string") """


#How to print certain range of Armstrong Numbers:number that is equal to the sum of its own digits each raised to the power of the number of digits.
# Ex:123=1^3+2^3+3^3=36 36 is not equal 123 so not armstrong
""" num = input("Enter a number to check armstrong: ")
length = len(num)
total = 0

for each_digit in num:
    power_value = int(each_digit) ** length
    total = total + power_value

if total == int(num):
    print("Armstrong Number")
else:
    print("Not Armstrong") """

#How to Print Calendar 
""" import calendar
print(calendar.month(2026,1)) #module name(calendar) and method name(month)
print(calendar.calendar(2026,2,2,3,4)) #year,width,length,space b/w, column with screen
print(calendar.weekday(2026,1,14)) #year,month,date(which week the date falls)
print(calendar.isleap(2024))
print(calendar.leapdays(2000,2024)) #leap year b/w=starting year, ending year """
#Sorting Operations (ascending/descending or alphabetical)
""" names=['rajmohan','vinodha','aazhini','viyan']
age=[40,32,2020,2022]
names.sort()
age.sort()
print(names)
print(age) 
names.reverse()
print(names)
print()
print("Alphabet wise name sorting: ",list(reversed(sorted(names))))
print("Ascending Number wise sorting: ",sorted(age)) """

#How to Remove Punctuations: symbols that we use to separate written sentences and parts ex: commas, full stop, question mark, or exclamation mark.
""" punct = "It uses symbols like periods, commas, question marks, and exclamation points to guide readers on how to interpret text, indicating pauses, stops, and emphasis"
punctuation = ".,!?:;'-\"()[]{}"
clean_word=""
for char in punct:
    if char not in punctuation:
        clean_word=clean_word+char

#import re
#clean_word=re.sub(r'[^\w\s]', '', punct)
print(clean_word) """
#How to Count Number of Digits in a Number
""" digits=int(input("Enter a number to check digits: "))
total_digits=0
while (digits!=0):
    digits=digits//10
    total_digits+=1
print(total_digits) 
#len()
print("Total digits: ", len(str(digits))) """

# How to count Number of occurrence of Character in a String
""" string1 = "It uses symbols like periods, commas, question marks, and exclamation points to guide readers on how to interpret text, indicating pauses, stops, and emphasis"
letter_find = "i"
total=0
for char in string1:
    if char == letter_find:
        total = total+1
print(total)
# built-in function
num_terms=string1.count(letter_find)
print(num_terms) """

# How to count Number of occurrence of each character in a String
""" string1 = "It uses symbols like periods, commas, question marks, and exclamation points to guide readers on how to interpret text, indicating pauses, stops, and emphasis"
frequency= {}

for char in string1:
    if char == frequency:
        frequency[char] = frequency[char]+1
    else:
        frequency[char] = 1
print(frequency)
# collection module
from collections import Counter
freq = Counter(string1)
print(freq) """

