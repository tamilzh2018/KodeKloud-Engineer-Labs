#Abstraction in Python is about exposing what an object can do while hiding how it does it.Python supports abstraction mainly through Abstract Base Classes (ABCs) and interfaces-by-convention.
""" from abc import ABC, abstractmethod
#convert normal to abstract class and method
class Conv_Abs(ABC): # inheritthe abstract base class from the moduel to convert a class as abstract class
    @abstractmethod
    def conv_abs_method(self): # convert a method to abstract method  we use decorator and pass keyword
        pass # we can't create object for obstract class and can't define definition, just you can declare
class Use_Abstract_class(Conv_Abs):
    def conv_abs_method(self):
        print("Accesing the abcstrat method") #actual process defined at derived class's abstract method here.

obj= Use_Abstract_class()
obj.conv_abs_method() """

#Incase if you defined multiple abstract method with in abstract class but creates definition for specfic method skiping others on derived class not allowed,
#Error:Can't instantiate abstract class Derived_Class without an implementation for abstract method 'method2'
""" from abc import ABC, abstractmethod
class A(ABC):
    @abstractmethod
    def method1(self):
        pass
    @abstractmethod
    def method2(self):
        pass
class Derived_Class(A):
    def method1(self):
        print("Method1 from abstract class")
obj=Derived_Class()
obj.method1()
 """
#Sometimes in Abstract method declared and partially definition created other should be hide
from abc import ABC, abstractmethod
class Partial_Abs(ABC):
    @abstractmethod
    def partial_defined(self):
        print("Partial Exection from abstrat class method")
        pass # remining from derived class

class partial_derived(Partial_Abs):
    def partial_defined(self):
        super().partial_defined()
        print("Remianing Execution from Derived Class")
obj=partial_derived()
obj.partial_defined()