#String:- Surrounded by either single quotation marks, or double quotation marks.
#Multiline Strings-assign a multiline string to a variable by using three quotes either double os single quotes:
#Python does not have a character data type
#To access elements of the string-Square brackets ex:a[index-value]
#To get the length of a string, use the len() function.
#Modify a string:- upper() method returns the string in upper case, lower() method returns the string in lower case,strip() method removes any whitespace from the beginning or the end, To concatenate, or combine, two strings you can use the + operator.
#Note: All string methods return new values. They do not change the original string.
""" 
capitalize()	Converts the first character to upper case # syntax: string.capitalize()
casefold()	Converts string into lower case # syntax: string.casefold()
center()	will center align the string, using a specified character (space is default) as the fill character # syntax: string.center(length, character)
count()	Returns the number of times a specified value occurs in a string
encode()	Returns an encoded version of the string
endswith()	Returns true if the string ends with the specified value
expandtabs()	Sets the tab size of the string
find()	Searches the string for a specified value and returns the position of where it was found #returns -1 if the value is not found.
format()	Formats specified values in a string
format_map()	Formats specified values in a string
index()	Searches the string for a specified value and returns the position of where it was found #raises an exception error if the value is not found
isalnum()	Returns True if all characters in the string are alphanumeric
isalpha()	Returns True if all characters in the string are in the alphabet
isascii()	Returns True if all characters in the string are ascii characters
isdecimal()	Returns True if all characters in the string are decimals
isdigit()	Returns True if all characters in the string are digits
isidentifier()	Returns True if the string is an identifier
islower()	Returns True if all characters in the string are lower case
isnumeric()	Returns True if all characters in the string are numeric
isprintable()	Returns True if all characters in the string are printable
isspace()	Returns True if all characters in the string are whitespaces
istitle()	Returns True if the string follows the rules of a title
isupper()	Returns True if all characters in the string are upper case
join()	Joins the elements of an iterable to the end of the string
ljust()	Returns a left justified version of the string
lower()	Converts a string into lower case
lstrip()	Returns a left trim version of the string
maketrans()	Returns a translation table to be used in translations(Ascii code)
partition()	Returns a tuple where the string is parted into three parts
replace()	Returns a string where a specified value is replaced with a specified value
rfind()	Searches the string for a specified value and returns the last position of where it was found
rindex()	Searches the string for a specified value and returns the last position of where it was found
rjust()	Returns a right justified version of the string
rpartition()	Returns a tuple where the string is parted into three parts
rsplit()	Splits the string at the specified separator, and returns a list
rstrip()	Returns a right trim version of the string
split()	Splits the string at the specified separator, and returns a list #syntax: string.split(separator, maxsplit)
splitlines()	Splits the string at line breaks and returns a list #syntax: string.splitlines(keeplinebreaks)
startswith()	Returns true if the string starts with the specified value # syntax: string.startswith(value, start-position, end-position)
strip()	Returns a trimmed version of the string #removes any leading(beginning of the string), and trailing(at the end of string) whitespaces. #syntax: string.strip(characters)
swapcase()	Swaps cases, lower case becomes upper case and vice versa
title()	Converts the first character of each word to upper case
translate()	Returns a translated string(Ascii code)
upper()	Converts a string into upper case
zfill()	Fills the string with a specified number of 0 values at the beginning # syntax: string.zfill(len) .adds zeros (0) at the beginning of the string, until it reaches the specified length.If the value of the len parameter is less than the length of the string, no filling is done.

"""
#Note: we cannot combine strings and numbers like "My name is John, I am " + 18

#1.Upper case the first letter in follwoing sentence
""" txt = "hello, and welcome to my world."
x = txt.capitalize()
print(x) """
#2.Join all items in a tuple into a string, using any character as separator:
""" myTuple = ("John", "Peter", "Vicky")
y = '$'.join(myTuple)
print(y)
 """
#3. Remove spaces to the left of the string:
""" txt ="  removed_left_space"
z = txt.lstrip()
print(z) """

#4. Split a string into a list 
""" txt = "welcome to the jungle"

a = txt.split()
print(a) """

#4. Split the string, but keep the line breaks:
""" txt = "Thank you for the music\nWelcome to the jungle"

x = txt.splitlines(True)

print(x) """

#5.Check if the string starts with either "Hello" or "Hi":
""" txt = "Hi, welcome to my world."

x = txt.startswith(("Hello", "Hi"))

print(x) """

#6. Check if position 7 to 20 starts with the characters "wel":
""" txt = "Hello, welcome to my world."

x = txt.startswith("wel", 7, 20)

print(x) """

#6.Fill the string with zeros until it is 10 characters long:
""" 
a = "hello"
b = "welcome to the jungle"
c = "10.000"

print(a.zfill(10))
print(b.zfill(10)) #no fill bacause string length exceeds
print(c.zfill(10)) """

#7. Replace the word S to J":
""" txt = "I like bananas"

x = txt.replace("s", "j")
print(x)
 """



#8. String Concatenation means bring into single string
a = "Hello"
b = "welcome to the jungle"
c = a+ " "+ b
print(c) 
print(a+ "", b)

#9. String Repetition
""" a = "Hello"
b = a*3
print(b) """

#10. String Postive Indexing(0,1, etc)/Negative(-1,-2, etc), to access each charactor from the string
""" a = "Hello world"
print(a[4]) 
print(a[-5])
"""

#11. String slicing, starts from specific character end with from string to access ex: [start, end, step]
a = "Hello world"
print(a[::2])
print(a[::-2]) #start from backside
print(a[-5:-8:-2]) # negative index slicing