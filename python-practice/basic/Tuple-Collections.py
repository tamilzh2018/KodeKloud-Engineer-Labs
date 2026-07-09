#Ordered(created list order will be maintained), Unchangable(add new items and remove old items not allowed but we can achieve with type casting)Item Assignment not Allowed, Allows Duplicates
#Tuple accessing-Using index-tuple_name[index-number] & negative index-tuple_name[- index-number], Using slice()
#packing and Unpacking- syntax: start_element, *remaining_element, stop_elemnet
# count(), index()
#Tuples looping- in, len(), range(), enumerate()
# empty_tuple_define = (),# Single_element_tuple_define = (value,) 
# list takes more memory space but tuples takes less: check through: list_var.__sizeod__() vs tuple_var.__sizeod__()

# Basic Operation in tuple
#1. find the length
""" num = (10,20,30,(40,50),'happy') #nested tuple content takes as single element 
print(len(num)) """

#2. tuple concatenation (takes only two varaibles)
""" a = ('happy', 'learning', 'python')
b = (1, 2, 3, 4)
print(a+b) """

#3. tuple repetition(takes one variable and integer)
""" a = ('happy', 'learning', 'python')
print(a*3) """

#4. Membership operator
""" a = ('happy', 'learning', 'python')
print( 'python3' not in a)
print( 'python' in a) """

#5. Accessing tuple values
""" a = ('happy', ('learning', 'python'), 20)
print(a[1][0]) # postive indexing
print(a[-2][-1]) # negative indexing """

#6. Slicing tuple values: more than one element to fetch from tuple
""" a = ('happy', ('learning', 'python'), 10, 20, True)
print(a[1:3]) #postive slicing
print(a[-1::-1]) # negative slicing """

#7.  packing and un-packing in normal tuples(nested tuple will not works)
""" variable_pack = ('happy', 'learning', 'python', 10, 20, True)
express, book, langauge, page_start, page_end, is_it = variable_pack # assign new variables with exact values else will through error
print(express, book, langauge, page_start, page_end, is_it) """

#8. Tuple buit-in function
""" sample_tuple = (10,2,0,31,12,54,87,10,20,10,34,2,5,2)
print(sample_tuple.count(10))
print(sample_tuple.index(54)) # first ocuurence values """


