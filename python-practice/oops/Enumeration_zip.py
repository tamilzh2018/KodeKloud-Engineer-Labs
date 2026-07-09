#Dispaly iterables with their index numbers
""" l1=['apple','orange','banna','cherry']
index=1
for fruits in l1:
    print(index,fruits)
    index=index+1 """

#without counter to achieve,we can use enumerate(iterables) gives output content with index: index,value
""" fruits=['apple','orange','banna','cherry','Guava']
for x,fruit in enumerate(fruits,1): #indexing starts from 0 default,we can modify starting indexing
    print(x,fruit)

#zip(iterable1,iterable2...etc) to combine the iterable uniform element give ouput as tuple object, incase uneven elements take minimum elements and combine
l1=['apple','orange','banna','Cherry']
l2=[10,20,15,24,5]
s=('Count:','Count:', 'Count:')
result=list(zip(l1,s,l2))
print(result)
print(set(zip(l1,l2)))
print(dict(zip(l1,l2)))

#zip with for loop
for x,y,z in result:
    print(x,y,z) """

#unzip and longest package use case:
#syntax:variables_name=zip(*zipped_values)
""" pairs=[(1,'a'),(2,'b'),(3,'c')]
chars,nums=zip(*pairs)
print(chars)
print(nums)
 """
#uneven elements zip operation with longest package to avoid data loss
""" from itertools import zip_longest
l1=['apple','orange','banna','Cherry']
l2=[10,20,15,24,5]
l3= range(1,7)
uneven_zip=list(zip_longest(l3,l1,l2,fillvalue='No value')) #fillvalue defualt is None, we can change
print(uneven_zip) """

#Enumerate(takes 2 parameters) with zip: incase zipped content requires indexing and ascending order
""" l1=['apple','orange','banna','Cherry']
l2=[10,20,15,24]
l3= range(1,5)
for i,(serial_num,fruit,count) in enumerate(zip(l1,l2,l3)): #i for index others for store respective values
    print(i,serial_num,fruit,count) """
#zip with sorting
""" l1=['apple','orange','banna','cherry']
l2=[10,20,15,24]
data=sorted(zip(l1,l2)) #by alphabetical
data1=sorted(zip(l2,l1)) # by numerical
print(data)
print(data1)
 """
#
buy_price=[100,200,300]
sold_price=[105,210,330]
products=range(1,4)
over_all_profit=0
for buy,sold,product in zip(buy_price,sold_price,products):
    profit=sold-buy
    over_all_profit=over_all_profit+profit
    print(f'{product} Total Profit value: {profit}')
print("Over all Profit: ",over_all_profit)