#Poly+morphism:- many+forms Ex: when Man/Women in office their roles is employee if they are in home there roles is father/mother or if they are in play ground their roles is player form.  
#Polymorphism in '+' operator
""" num1=10
num2=20
print("'+' operator with integer form is addition: ", num1+num2)
num3= 'hai'
num4='all'
print("'+' operator with string form is concatenation: ", num3+num4) """
#Polymorphism in '*' operator
""" num1=10
num2=20
print("'*' operator with integer form is Multiplication: ", num1*num2)
num3= 'hai'
num4=2
print("'*' operator mix of string and integer form is repeat  : ", num3*num4) """
#Polymorphism in Functions
""" print(len('string'))
print(len(['list',1,True, 0.5]))
print(len({'key':'value','dict':'form'})) """

#Polymorphism in Classes: diffrent class name but same method name
""" class A:
    def info(self):
        print("Class A method")
class B:
    def info(self):
        print("Class B method")
a_obj=A()
b_obj=B()
a_obj.info()
b_obj.info()
 """

#types:Operator overloading(arithmetic operator, comparision operator,assignment operator) 
#Operator overloading allows us to define how operators behave when used with objects instead of built-in types.
""" class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # + operator
    def __add__(obj1, obj2):
        return Point(obj1.x + obj2.x, obj1.y + obj2.y)

    # * operator
    def __mul__(obj1, obj2):
        return Point(obj1.x * obj2.x, obj1.y * obj2.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p1 = Point(3, 4)
p2 = Point(1, 2)

print(p1 + p2)  # Point(4, 6)
print(p1 * p2)  # Point(3, 8) """
#Method Overloading means having multiple methods with the same name but different:number of parameters,type of parameters,order of parameters
# Method overloading(Python does not support true overloading because:A class can have ONLY ONE method of a given name,The last defined method overrides the previous one
#But we can simulate method overloading using:
# Default parameters
# Variable-length arguments (*args, **kwargs)
# Type-checking inside a method
# by default not support but we can achive by if condn and for loop or multipledispatch modules),
# ✔ Method Overloading using Default Arguments
""" 
class MathOps:
    def add(self, a=None, b=None, c=None):
        if a is not None and b is not None and c is not None:
            return a + b + c
        elif a is not None and b is not None:
            return a + b
        else:
            return a

obj = MathOps()
print(obj.add(10, 20))
print(obj.add(1, 2, 3))

# ✔ Method Overloading using `*args`

class MathOps:
    def add(self, *args):
        return sum(args)

obj = MathOps()
print(obj.add(10, 20))       # 30
print(obj.add(1, 2, 3))      # 6
print(obj.add(5))            # 5

# ✔ Method Overloading using Type Checking

class Display:
    def show(self, a):
        if isinstance(a, int):
            print("Integer:", a)
        elif isinstance(a, str):
            print("String:", a)

obj = Display()
obj.show(10)
obj.show("Hello") """

# Method overriding:A child class defines a method with the same name, same parameters, and same return type as a method in the parent class.
#The child class replaces or modifies the behavior of the parent method
#real usecase: software updation 
""" class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):  # Overriding parent method
        print("Dog barks")

d = Dog() #object creating for class
d.sound()
a=Animal() ##object creating for class
a.sound() """
#Method  Overriding Using super()
""" class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):
        super().sound()  # Call parent version
        print("Dog barks")

d = Dog()
d.sound() """
# Polymorphism using Inheritance and Method Overriding 
""" class Vehicle:
    def __init__(self, name, color, price):  #common values
        self.name=name
        self.color=color
        self.price=price
    def show(self):
        print("Vehicle Details: ", self.name,self.color,self.price)
    def speed(self):
        print("Max speed limit is 100")
    def gear(self):
        print("No Gear")
class Car(Vehicle):
    def speed(self):
        print("Max Speed limit is 240")
    def gear(self):
        print("Car has gear")

car= Car('Honda', 'Black', '5Lacs')
car.show()
car.speed()
car.gear()
print()
scooty=Vehicle('Tvs 50', 'Green', '1Lac')
scooty.show()
scooty.speed()
scooty.gear() """

#Polymorphism with classes methods and objects
""" class Birds:
    def sounds(self):
        return "parrot speak"
class Animals(Birds):
    def sounds(self):
        return "dogs barks"
class Fishes(Animals):
    def sounds(self):
        return "Doesn't make noise"
obj=[Birds(),Animals(),Fishes()] #list of class assigned to single object
for i in obj: #same method name to iterate
    print(i.sounds()) """


