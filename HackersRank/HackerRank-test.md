**Task 1:**
Given a positive integer n, perform the following conditional actions:

If n is odd, print "Weird"

If n is even and in the inclusive range 2 to 5, print "Not Weird"

If n is even and in the inclusive range 6 to 20, print "Weird"

If n is even and greater than 20, print "Not Weird"
Input Format:

A single line containing a positive integer, .

Constraints: 1 ≤ n ≤ 100

Output Format:

Print Weird if the number is weird. Otherwise, print Not Weird.
Ans:
# Get an integre value from user
n = int(input())

if n % 2 == 1:
    print("Weird")
elif 2 <= n <= 5:
    print("Not Weird")
elif 6 <= n <= 20:
    print("Weird")
else:
    print("Not Weird")

**Task 2:**

The provided code stub reads two integers from STDIN,  and . Add code to print three lines where:

The first line contains the sum of the two numbers.
The second line contains the difference of the two numbers (first - second).
The third line contains the product of the two numbers.
Ans:
a = int(input())
b = int(input())

print("Sum of two numbers: ", a+b)
print("Difference of two numbers: ", a-b)
print("Product of two numbers: ", a*b)

**Task 3:**
The provided code stub reads two integers,  and , from STDIN.

Add logic to print two lines. The first line should contain the result of integer division,  // . The second line should contain the result of float division,  / .

No rounding or formatting is necessary.

Ans:
a = int(input())
b = int(input())

print("Integer division of two numbers: ", a // b)
print("Float division of two numbers: ", a / b)

**Task 4:**
The provided code stub reads an integer, , from STDIN. For all non-negative integers i<n, print i**i.

Example n = 3

The list of non-negative integers that are less than  n = 3 is [0,1,,2]. Print the square of each number on a separate line.
Ans:
n = int(input())
if n >=0:
    for i in range(n):
        print(i*i)

**Task 5 :**
An extra day is added to the calendar almost every four years as February 29, and the day is called a leap day. It corrects the calendar for the fact that our planet takes approximately 365.25 days to orbit the sun. A leap year contains a leap day.

In the Gregorian calendar, three conditions are used to identify leap years:

The year can be evenly divided by 4, is a leap year, unless:
The year can be evenly divided by 100, it is NOT a leap year, unless:
The year is also evenly divisible by 400. Then it is a leap year.
This means that in the Gregorian calendar, the years 2000 and 2400 are leap years, while 1800, 1900, 2100, 2200, 2300 and 2500 are NOT leap years. Source


Given a year, determine whether it is a leap year. If it is a leap year, return the Boolean True, otherwise return False.

Note that the code stub provided reads from STDIN and passes arguments to the is_leap function. It is only necessary to complete the is_leap function.

Input Format

Read year, the year to test.

Constraints
1900<=year<=10 power 5 or print(10**5)

Output Format

The function must return a Boolean value (True/False). Output is handled by the provided code stub.

Sample Input 0

1990
Sample Output 0

False
Explanation 0

1990 is not a multiple of 4 hence it's not a leap year.

Ans:
def is_leap(year):
    leap = False
    
    # Write your logic here
    if year % 4 == 0 :
        if year % 400 == 0 or year % 100 !=0 :
            leap = True
        
    
    return leap

year = int(input())
print(is_leap(year))

**Task 6**
The included code stub will read an integer, , from STDIN.

Without using any string methods, try to print the following: 123...n

Note that "..." represents the consecutive values in between.

Example n = 5

Print the string 12345.

Input Format

The first line contains an integer n.

Constraints
1 <= n <=150

Output Format

Print the list of integers 1 from  through n as a string, without spaces.

Sample Input : 3 output: 123

Ans:
n = int(input())
if 1 <= n <= 150:
    for i in range(1, n+1):
        print(i, end="")  #To print each number on a same line

**Task 7**
If we want to add a single element to an existing set, we can use the .add() operation.
It adds the element to the set and returns 'None'.

Example

>>> s = set('HackerRank')
>>> s.add('H')
>>> print s
set(['a', 'c', 'e', 'H', 'k', 'n', 'r', 'R'])
>>> print s.add('HackerRank')
None
>>> print s
set(['a', 'c', 'e', 'HackerRank', 'H', 'k', 'n', 'r', 'R'])

Ques:

Apply your knowledge of the .add() operation to help your friend Rupal.

Rupal has a huge collection of country stamps. She decided to count the total number of distinct country stamps in her collection. She asked for your help. You pick the stamps one by one from a stack of  N country stamps.

Find the total number of distinct country stamps.

Input Format

The first line contains an integer N , the total number of country stamps.
The next N lines contains the name of the country where the stamp is from.

Constraints

0 < N < 1000
Output Format

Output the total number of distinct country stamps on a single line.

Sample Input

7
UK
China
USA
France
New Zealand
UK
France 

Sample Output

5
Explanation

UK and France repeat twice. Hence, the total number of distinct country stamps is 5 (five).

Ans:
n = int(input()) # total number of country stamps
s = set()
for i in range(n):
    country = input() #read n country names from input and add them to the set:
    s.add(country)
print (len(s))

**Task 8**
.remove(x)

This operation removes element "x" from the set.
If element "x" does not exist, it raises a KeyError.
The .remove(x) operation returns None.

Example

>>> s = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> s.remove(5)
>>> print s
set([1, 2, 3, 4, 6, 7, 8, 9])
>>> print s.remove(4)
None
>>> print s
set([1, 2, 3, 6, 7, 8, 9])
>>> s.remove(0)
KeyError: 0
.discard(x)

This operation also removes element "x" from the set.
If element "x" does not exist, it does not raise a KeyError.
The .discard(x) operation returns None.

Example

>>> s = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> s.discard(5)
>>> print s
set([1, 2, 3, 4, 6, 7, 8, 9])
>>> print s.discard(4)
None
>>> print s
set([1, 2, 3, 6, 7, 8, 9])
>>> s.discard(0)
>>> print s
set([1, 2, 3, 6, 7, 8, 9])
.pop()

This operation removes and return an arbitrary element from the set.
If there are no elements to remove, it raises a KeyError.

Example

>>> s = set([1])
>>> print s.pop()
1
>>> print s
set([])
>>> print s.pop()
KeyError: pop from an empty set

Quest:

You have a non-empty set "s", and you have to execute N commands given in N  lines.

The commands will be pop, remove and discard.

Input Format

The first line contains integer "n", the number of elements in the set "s" .
The second line contains "n" space separated elements of set "s". All of the elements are non-negative integers, less than or equal to 9.
The third line contains integer N , the number of commands.
The next N lines contains either pop, remove and/or discard commands followed by their associated value.

Constraints
0 < n < 20
0 < N < 20

Output Format

Print the sum of the elements of set "s" on a single line.

Sample Input: 
line1: 9
line2: 1 2 3 4 5 6 7 8 9
line3: 10
pop
remove 9
discard 9
discard 8
remove 7
pop 
discard 6
remove 5
pop 
discard 5

Sample Output: 4
Explanation

After completing these 10 operations on the set, we get set([4]). Hence, the sum is 4.

Note: Convert the elements of set s to integers while you are assigning them. To ensure the proper input of the set, we have added the first two lines of code to the editor.

Ans:
## Read the number of elements in the set
n = int(input())
# Read the initial set of elements and convert them to integers
s = set(map(int, input().split()))
# Read number of operations
N = int(input())

for _ in range(N):
# Taking a line of input (like "remove 3") and splitting it into a list of words:ex: command = ["remove", "3"] command[0] refers to the first word, which is the command type — like "remove", "discard", or "pop". command[1] refers to the second word, which is the value associated with the command — like 3 in "remove 3"
    command = input().split() 

    if command[0] == "pop":
        s.remove(min(s))  # deterministic pop
    elif command[0] == "remove":
        val = int(command[1])
        if val in s:
            s.remove(val)
    elif command[0] == "discard":
        s.discard(int(command[1]))

print(sum(s))

