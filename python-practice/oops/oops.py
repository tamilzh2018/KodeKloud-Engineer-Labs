""" class Person:
    
    def people(self,name,age, gender):
        name=input("Enter your name: ")
        age=int(input("Enter your age: "))
        gender=input("Enter you gender: ")
        print(f"Person Name is: {name}, his age is: {age} and his gender is: {gender}")
p=Person()
p.people('name','age','gender') """

#Area of a Room
""" class Room:
    
    def cal_area_of_room(self,length,breadth):
        length=float(input("Enter the length of the room: "))
        breadth=float(input("Enter the breadth of the room: "))
        print("Area of the Room is:", length*breadth)
area=Room()
area.cal_area_of_room('length','breadth') """

# Constructor- to initialize(assign values) to the data members(ex:variables) of the class when an object of the class is created. types: Default and Parameterised
#Default: Per clas only one defualt constructor allowed, if you try to create more than one init constructor per class it overwrites
""" class Constructor_test:
    def __init__(self): #constructor
        name=input("Enter your name: ")
        age=int(input("Enter your age: "))
        print("Name is: ", name)
        print("Name is: ", age)
        print("Constructor method, No need call after object to be created, automticallay callable when object created")
default_construct_obj= Constructor_test() """

#Parameterised constructor types: postional, default(set default argument value), keyword(set argument keyword when object creation time ),variable length(don't know exact argument)
""" class Params_constructor:
    def __init__(self, name,age): #Positional parameterised constructor
    #def __init__(self, name='raj',age=40): #Default parameterised constructor
    #def __init__(self, name,*age): #variable length parameterised constructor
        name=input("Enter your name: ")
        age=int(input("Enter your age: "))
        print("Name is: ", name)
        print("Name is: ", age)
        print("Constructor method, No need call after object to be created, automticallay callable when object created")
Params_constructor_obj= Params_constructor("name","age")
#Params_constructor_obj= Params_constructor("name",40,45,20) #variable length use for loop to pass each value
#Params_constructor_obj= Params_constructor("age=40","name=raj") #What used in constructor meathod Same Keyword when object creation """

# Area of traingle using constructor
""" class Area_of_Triangle:
    def __init__(self,b,h):
        self.base=b  #self keyword using to pass this value another function incase if you are not going to pass this values another function you use without self. ex:variable_name
        self.height=h 
        self.area= self.base*self.height* 0.5
        print("Area of triangle: ", self.area)
triangle_obj=Area_of_Triangle(8,9) """

# Destructor-to deallocate the memory and cleanup hold resources when object destroyed
""" class Destructor_test:
    def __init__(self): #constructor
        name=input("Enter your name: ")
        age=int(input("Enter your age: "))
        print("Name is: ", name)
        print("Name is: ", age)
    def __del__(self): ##destructor
        print("object deleted")  
default_construct_obj=Destructor_test()
del default_construct_obj #delete the object  """

# constructor with return type: always keep return None
""" class construct_return:
    def __init__(self,a,b):
        c = a+b
        return c #__init__() should return None, not 'int' 'str' 'bool' if you give other than None throws error
obj=construct_return(10,20) """