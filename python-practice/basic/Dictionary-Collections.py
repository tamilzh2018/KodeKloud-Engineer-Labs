# We cannot set our own index value for list and tuple elements, but we can set our own index value for each element in a dictionary. That's "Key".
# Ordered, Changable(values can change), Duplicates not Allowed because accessing by keys if duplicated keys there it will overwrite the exisitng value.
# Dictionary are key:value pair,Accessing dict is Using keys, values, like .key(), .values(), .items(provide keys:value pair tuple), .get(key)-to access specific value without throw error
# Add new items: use dictname[key]=value, .update(update/add specified key:value), 
# Remove old Items: pop(removes specific key), popitem(removes last insreted pairs),del keyword,pop(), clear()
# empty_dict_define = {}
# count(), copy(), reverse(), sort()
# Dictionary looping: keys(), values(), items()
# Nested Dcit: ex:json file

"""
clear()	Removes all the elements from the dictionary
copy()	Returns a copy of the dictionary
fromkeys()	Returns a dictionary with the specified keys and value
get()	Returns the value of the specified key
items()	Returns a list containing a tuple for each key value pair
keys()	Returns a list containing the dictionary's keys
pop()	Removes the element with the specified key
popitem()	Removes the last inserted key-value pair
setdefault()	Returns the value of the specified key. If the key does not exist: insert the key, with the specified value
update()	Updates the dictionary with the specified key-value pairs
values()	Returns a list of all the values in the dictionary 

"""
# List as dictionary
""" food = ["idli", "dosai", "rice", "parota", "puri"]
numbers = [1,2,3,4,5,3,6,7,8,9,0] #even if u have extra values then "keys" dict will not assign keys for that values simply it ommits the values
print(dict(zip(food, numbers)))  """
# Tuple as dictionary
""" a = ('happy', 'learning', 'python')
b = (1, 2, 3, 4)
print(dict(zip(a, b))) """
# dict function
""" a = dict([('express', 'happy'), ('learning','book'), ('python','langauge')])  #convert list and tuple as dict
print(a) """
# Basic Operation in Dictionary
# 1.Find the length
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
print(len(a)) """
# 2.Concatenation (takes only two varaibles) : dict+dict not allowed
# 3.Repetition(takes one variable and integer)dict*int not allowed
# 4.Membership operator
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
print( 'express' in a) # Check with key
print( 'express' not in a) # Check with key """
# 5. Accessing dictionary elements
""" a = {'express': 'happy', 'learning': 'book', 'python': 'langauge','python': 'snake'} # Duplicates not Allowed because accessing by keys if duplicated keys there it will overwrite the exisitng value.
print(a ['express'])
print(a['python']) #output snake becuase value overwritten
 """
#6 Nested Dictionary Accessing or Json Accessing
""" nest_data = {'name': 'sivam', 'class': 10,
              'interest':['playing hockey', 'playing basketball'],
              'location': {'trichy': 'ponmalai', 'kavai':'high school'}
             
             }
print(nest_data["location"]['kavai']) # dict inside list so use key with subkey to access value
print(nest_data["interest"][1]) #dict inside list so use key with index to access value
data = {
    "menu": {
        "header": "SVG Viewer",
        "items": [
            {"id": "Open"},
            {"id": "OpenNew", "label": "Open New"},
            None,
            {"id": "ZoomIn", "label": "Zoom In"},
            {"id": "ZoomOut", "label": "Zoom Out"},
            {"id": "OriginalView", "label": "Original View"},
            None,
            {"id": "Quality"},
            {"id": "Pause"},
            {"id": "Mute"},
            None,
            {"id": "Find", "label": "Find..."},
            {"id": "FindAgain", "label": "Find Again"},
            {"id": "Copy"},
            {"id": "CopyAgain", "label": "Copy Again"},
            {"id": "CopySVG", "label": "Copy SVG"},
            {"id": "ViewSVG", "label": "View SVG"},
            {"id": "ViewSource", "label": "View Source"},
            {"id": "SaveAs", "label": "Save As"},
            None,
            {"id": "Help"},
            {"id": "About", "label": "About Adobe CVG Viewer..."}
        ]
    }
}

print(data["menu"]["items"][13]["id"]) #dict inside list inside dict so use combination of key,key,index,key since you know the position of list
print(data["menu"]["items"][17]["label"]) ##dict inside list inside dict so use combination of key,key,index,key since you know the position of list """

#7. modifying dictionary elements value
""" nest_data = {'name': 'sivam', 'class': 10,
              'interest':['playing hockey', 'playing basketball'],
              'location': {'trichy': 'ponmalai', 'kavai':'high school'}
             
             }
nest_data["location"]["kavai"]="Higher Secondary School" #existing value modified
nest_data['dist']='ariyalur' # whether the key and value is exist in the dictinary if yes overwrites new value else create new key value pair
print(nest_data) """

#8.Deleting dict elemetns and entire dictionary
""" 
a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
del a['python'] #key name
print(a)
del a # dictionary variable name
print(a) #error: 'a' is not defined """

#9. Built-in Functions
#a. items()- whatever we are giving key:values inside dictionaries called item.it will give ouput as tuple
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
print(a.items())
#b. keys()- provide available keys inside dict only
print(a.keys())
#c. values()-provide available valuess inside dict only
print(a.values()) """

#d. Accessing Dict by get()
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
print(a.get('learning')) 
print(a.get('nothing')) # there is no such a key avail inside dict but get will not throw error, but we can set some display if the keys not avail inside dictionary
print(a.get('nothing', 'expected key not available')) #get() check matchable keys avail or not if there gives else default message give as output if we set """

#e. adding dict with dict or dict witn new element
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
a.update(write='any') #new item adding on existing dict iems
print(a)
b= {'location': 'trichy', 'kavai':'high school'}
a.update(b) # dict addtion
print(a) """
#f. copy()-duplicate existing dict but diffrent store in diff memory location
""" a= {'express': 'happy', 'learning': 'book', 'python': 'langauge'}
b = a.copy()
print(b) """
#g.Different keys but common values 
""" name=("aazhini","raj","viyan","vinodha")
com_value=(20)
empty_dict={}
print(empty_dict.fromkeys(name,com_value)) """

#h. if keys not exist then add items in the dictionary else don't set default value or new value
""" name={"aazhini":5,"raj":40,"viyan":2,"vinodha":32}
print(name.setdefault('total',4))
print(name) """

#I. To remove specified key from a dictionary and dispaly the removed value
""" name={"aazhini":5,"raj":40,"viyan":2,"vinodha":32,'total_member':4,'planning':'onemore'}
print(name.pop('total_member')) """

#j. To remove last key from a dictionary and dispaly the removed value
""" name={"aazhini":5,"raj":40,"viyan":2,"vinodha":32,'total_member':4,'planning':'onemore'}
print(name.popitem()) """

#k. To remove entire itesm but don't delete dict variable
name={"aazhini":5,"raj":40,"viyan":2,"vinodha":32,'total_member':4,'planning':'onemore'}
name.clear()
print(name) #output empty dictionary
