#Random Module used for generate random numbers(float value, integer value),strings
import random
""" f=random.random()# module_name.method_name:-Always give float value b/w 0 to 1
print(f) """

#float value other 0 to 1 range use uniform()
""" uf=random.uniform(1,5)
print(uf) """

#random integer value require with start and end value be takes place. use randint()
""" rt=random.randint(1,10)
print(rt) """
#random integer value require but except end value also want to use step value. use randrange()
""" rr=random.randrange(1,100,5)
print(rr) """

#Want to take single element randomly with list,tuple. use choice()
""" l1=[1,2,3,4,True,False,3.4,'Hi']
string="Random-StringExamples"
tuple1=(1,6,7,8,9,345,56,10)
print('List with Random: ',random.choice(l1))
print('String with Random: ',random.choice(string))
print('Tuple with Random: ',random.choice(tuple1)) """

#Want to take more than one element randomly with list,tuple. use sample()

""" l1=[1,2,3,4,True,False,3.4,'Hi']
string="Random-StringExamples"
tuple1=(1,6,7,8,9,345,56,10)
print('Randomly take 2 element from list:',random.sample(l1,2))
print('Randomly take 2 element from list:',random.sample(string,2))
print('Randomly take 2 element from list:',random.sample(tuple1,2)) """

#Shuffle first list,tuple.then randomly re-arrange order give output. use shuffle()
""" l1=[1,2,3,4,True,False,3.4,'Hi']
string="Random-StringExamples"
tuple1=(1,6,7,8,9,345,56,10)
random.shuffle(l1)
print('Re-arrange order randomly:',l1) """



