# collections of unique and unordered items, Entire is set mutable(we can add new values inside set) but inside set element are immutable(we can't change existing values of set becuase no indexing follows)
#UnOrdered, Un Changable, Item Assignment not Allowed, No index logic so slicing not allowed , Duplicates Not Allowed(If ducplicates there, auto removed), 
# Add new items: add(), update(iterables),
# Remove old Items: remove(removes specific value incase the value dosen't exist will throw error),pop(removes randomly and also print those value),clear(),del keyword,discard(gracefully removes specific value incase the value dosen't exist will not throw error)
#empty_set define = set()
#Set Accesing: No index logic to acees set use 'in' and 'not in'
#set follos venn diagrams like union, right join, left join: difference(),difference_update(don't create seperate set update the difference on same set),intersection(common_values),intersection_update(),
# symmeteric_difference(without common values of both set),symmeteric_difference_update(), issubset(), issuperset(),isdisjoint(between the both set have comman values or not), union(join both set)
#Looping in Set - in , len(), range(no index based), enumerate(index with values)

""" 
add()	 	Adds an element to the set
clear()	 	Removes all the elements from the set
copy()	 	Returns a copy of the set
difference()	-	Returns a set containing the difference between two or more sets
difference_update()	-=	Removes the items in this set that are also included in another, specified set
discard()	 	Remove the specified item
intersection()	&	Returns a set, that is the intersection of two other sets
intersection_update()	&=	Removes the items in this set that are not present in other, specified set(s)
isdisjoint()	 	Returns whether two sets have a intersection or not
issubset()	<=	Returns True if all items of this set is present in another set
 	<	Returns True if all items of this set is present in another, larger set
issuperset()	>=	Returns True if all items of another set is present in this set
 	>	Returns True if all items of another, smaller set is present in this set
pop()	 	Removes an element from the set
remove()	 	Removes the specified element
symmetric_difference()	^	Returns a set with the symmetric differences of two sets
symmetric_difference_update()	^=	Inserts the symmetric differences from this set and another
union()	|	Return a set containing the union of sets
update()	|=	Update the set with the union of this set and others 

"""
#1. creating a set
""" a = {1, 2, 'we', True, 3.2}
print(a) """
#2. creating a empty set
""" var_a = set()
print(var_a) """
#3. Basic Operations like len(), min(),max(),sum() etc
""" a = {1, 2, 'we', True, 3.2}
print(len(a))
b = {12, 54, 87, 3.2}
print(min(b)) # all elements should be in integers or float
print(max(b)) # all elements should be in integers or float
print(sum(b)) # all elements should be in integers or float """

#4. Adding an element to set - add()
""" a = {1, 2, 'we', True, 3.2}
a.add('new_element')
print(a) """
#5. Adding mulitiple element to set - update()
""" a = {1, 2, 'we', True, 3.2}
b = {12, 54, 87, 3.2}
c = ['list-update', 'inside-set']
a.update(b,c)
print(a) """
#6. Accessing element from set - use for loop because no indexing
""" new_set = {1, 'we', 2, 3.2, 12, 'inside-set', 54, 87, 'list-update'}
for each_element in new_set:
    print(each_element) """
    
#7. Removing element from set - remove(),discard(),pop(), del() etc
""" new_set = {11, 'we', 2, 3.2, 12, 'inside-set', 54, 87, 'list-update'}
new_set.remove('we') # removes only existing value incase if you non existing value it will throws key-error
print(new_set) 
new_set.discard('non-exist') # if we give non-existing value it will not throws error
print(new_set)
new_set.pop() # removes randomly
print(new_set)
 """
#8 . Built-in function follows venn diagram
""" colors_vibgyor = {'Violet', 'Indigo', 'Blue', 'Green', 'Yellow', 'Orange', 'Red'}
colors_rgb = {'Blue', 'Green', 'Red','White', 'Pink'}
more_colors = {'Brown','Black','Grey','Green'}
u = colors_vibgyor.union(colors_rgb,more_colors) # All unique elements from all sets.
d = colors_vibgyor.difference(colors_rgb,more_colors) # Elements in colors_vibgyor that are NOT in the other sets.
i = colors_vibgyor.intersection(colors_rgb,more_colors) # Elements common to all sets.
sd = colors_vibgyor.symmetric_difference(colors_rgb) # removes common values between the sets but will create new set to display 
#colors_vibgyor.difference_update(colors_rgb,more_colors) # removes common elements b/w the sets, output overwrites existing set colors_vibgyor new-o/p:{'Orange', 'Violet', 'Yellow', 'Indigo'}
#colors_vibgyor.intersection_update(colors_rgb) # keeps only common values,output overwrites existing set colors_vibgyor new o/p: {'Red', 'Green', 'Blue'}
colors_vibgyor.symmetric_difference_update(colors_rgb) # removes common values between the sets but will not create new set to display it overwrites first set
print(u)
print(d)
print(i)
print(sd)
print(colors_vibgyor) """

#issubset() and issuperset() isdisjoint()
colors_rgb = {'Blue', 'Green', 'Red','White', 'Pink'}
more_colors = {'Brown','Black','Grey','Green'}
print(colors_rgb.issubset(more_colors)) # Returns True if all elements of set1 are contained in set2.subset means set1 ⊆ set2 (set2 may have extra elements)
print(colors_rgb.issuperset(more_colors)) #Returns True if set1 contains all elements of set2. not allowed to have extra elements
print(colors_rgb.isdisjoint(more_colors)) # Returns True if the two sets have no elements in common.
