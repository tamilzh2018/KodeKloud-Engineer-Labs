#Encapsulation:- Wrapping of data and method ex:capsule. used to protect and hide
#Encapsulation is the process of wrapping data (variables) and methods (functions) into a single unit, like a capsule. It is mainly used to protect data and hide internal details from the outside world.
#Key Points: Data and methods are bundled together in a class.Internal data can be hidden using access modifiers (like private, protected, public).Provides security, control, and data integrity.

## 🔓 **Public**

# * Variables or methods declared as **public** can be accessed:
#   ✔ Within the class
#   ✔ Within class methods
#   ✔ Outside the class (from objects)
# * **No access restrictions.**

### Example (Python)
# class Demo:      
#     def name(self):
#         self.name = "Public Variable"   # public
#         print("With in Class method,Name:", self.name) # with in class methods

# pub_obj=Demo()
# pub_obj.name()
# print("Outside class Name:", pub_obj.name) # outside the class and methods


## 🔒 **Private**

# * Variables or methods declared as **private** **cannot be accessed directly from outside the class**.
# * To access private data, you need **public getter/setter methods**.
# * In Python, private members start with `__` (double underscore).

### Example (Python)

""" class Student:
    def __init__(self, name=""):
        self.__name = name  # private variable

    def get_name(self):
        return self.__name  # public method to access private data

    def set_name(self, name):
        self.__name = name  # public method to modify private data
priv_obj=Student()
priv_obj.set_name('raj') #setting value
print(priv_obj.get_name()) #retrive value """
## 🛡️ **Protected**

# * Variables or methods declared as **protected** can be accessed:
#   ✔ Within the class
#   ✔ In child classes (inheritance)
# * By convention in Python, protected members start with `_` (single underscore).
# * Usually accessed through methods in the subclass.

### Example (Python)
""" class Parent:
    def __init__(self):
        self._value = "Protected Variable"

class Child(Parent):
    def show_value(self):
        return self._value   # allowed through inheritance """

## ✔ Summary Table

# | Access Type   | Within Class | Outside Class | Inherited Class                     |
# | ------------- | ------------ | ------------- | ----------------------------------- |
# | **Public**    | ✔ Yes        | ✔ Yes         | ✔ Yes                               |
# | **Private**   | ✔ Yes        | ✖ No          | ✖ No (unless using getters/setters) |
# | **Protected** | ✔ Yes        | ✖ No          | ✔ Yes                               |

#setter and getter works with property() Decorator-used to change the method behavior
#methos and Attribute(variable) name must be same while using Setter and Getter
class Prop_Decorator:
    def __init__(self):  #constructor
        self.__age=0
    @property
    def age(self):
        print("Getter Method called")
        return self.__age
    @age.setter
    def age(self,a):
        if (a<18):
            print("Under 18")
        print("Setter Method Called")
        self.__age=a 
obj=Prop_Decorator() #create an object
obj.age=10 #set the age value This calls the setter method.
print(obj.age) #get the age value,This calls the getter method
