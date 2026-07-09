#Variable types: instance variable(within class and inside method variable assigned), class varible(within class but outside method)
#Method types: Instance(self parameter comes),Class(class decorator and cls parameter comes),Static
""" class demo:
    var='class variable defined'
    def instance_method(self,a,b):
        print('addition value: ',a+b)
    @classmethod
    def cls_method(cls):
        print('Class Method and Class variable', cls.var)
    @staticmethod
    def stat_method():
        print('Static Method Not passing parameter')
obj=demo()
obj.instance_method(4,5) #calling instance method
obj.cls_method() #caling class method
obj.stat_method() """

#Iterator:lets you traverse through a sequence one element at a time
#iterators-access next element one by one, we can achive this with for loop and with iter() & next()
# Without looping we can access one element at a time
list1=['hai',4,True,8.5]
#convert to iterable
var=iter(list1)
#fetch the element from iterable
print(next(var))
print(var.__next__())
