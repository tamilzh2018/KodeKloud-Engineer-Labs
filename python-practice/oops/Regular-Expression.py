#Regular expression:To find certain pattern is avail inside the string or not
import re
#findall checks certain pattern if avail it dispalys inside list else returns empty list
""" string1="Hi How are you"
result=re.findall('n',string1) #findall(pattern,string)
print(result) """
#search() used to which postion the pattern avail and returns matchobject to fromtaht use start() or span() or string()
""" s1="Hi How are you"
ans=re.search('ow',s1) 
print("start method:", ans.start()) #the pattern starting position if not avail error:'NoneType' 
print("span method:",ans.span()) #the pattern between range position if not avail error:'NoneType' 
print("string method:",ans.string)#complte string value retuns if not avail error:'NoneType' """

#split() used to bifuricate the string
""" split1="Hi How are you" 
ans=re.split('H',split1)#split(pattern and variable) removes the char fill with empty
#want to split each char
ans1=re.split("",split1)
print(ans)
print(ans1) """
#don't split more than 2 times
""" new='complte string value retuns if not avail'
print("Splits 2 times then rest keeps:",re.split(" ",new,2)) """

#sub() used to replace a charcter
""" replac="Hi How are you all is well" 
ans2=re.sub('H','h',replac)
print("replace 2 occurrence remaing keep: ",re.sub('l','#',replac,2)) 
print(ans2)
 """
#Meta chracters [string],^start,end$,let..(ex:2 chars comes from this string 'let' no remember fetch that value)
#Special Characters And Sets
string1="91lets us see what meta characteers.com 456"
""" print("How many times occured this string or char:", re.findall('[a]',string1))
print("The string or char starts from:", re.findall('^91',string1))
print("The string or char ends with:", re.findall('.com$',string1))
print("Partially known character or string:", re.findall('rin.',string1)) 
print("Character Occured once or more than once:", re.findall("ee*",string1)) # Character occured once or more than display that rest enter enter empty value
print("Patern Occured once or more than once:", re.findall("ee+",string1))
print("Patern Occured times:", re.findall("e{2}",string1))
print("Display only space:", re.findall("\s",string1))
print("Dispaly other than space:", re.findall("\S",string1))
print("Dispaly only digts:", re.findall("\d",string1))
print("Dispaly other than digits even space:", re.findall("\D",string1))
print("Dispaly only word characters:", re.findall("\w",string1))
print("Dispaly other than words:", re.findall("\W",string1)) """

#sets
""" print("Single digit range:", re.findall("[0-9]",string1))
print("Two digit range:", re.findall("[0-9][0-9]",string1))
print("Three digit range:", re.findall("[0-9][0-9][0-9]",string1))
print("albhabets range:", re.findall("[a-c]",string1)) """
#india phone number validation pattern="^[789]\d{9}$"
#Email Validation pattern=r"[a-zA-Z0-9._]+@[a-z]{8}\.[a-z]{2,4}$"
""" import re

# Phone number validation
def phone_validation(number):
    pattern = r"^[789]\d{9}$"
    if re.match(pattern, number):
        return "Valid Indian Mobile Number"
    else:
        return "Invalid Indian Mobile Number"

number = input("Enter Your Mobile Number: ")
print(phone_validation(number))


# Email validation
def email_validation(mail):
    pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z]+\.[a-z]{2,4}$"
    return bool(re.match(pattern, mail))

mail = input("Enter Email Address: ")
if email_validation(mail):
    print("Email Address valid")
else:
    print("Invalid address") """
