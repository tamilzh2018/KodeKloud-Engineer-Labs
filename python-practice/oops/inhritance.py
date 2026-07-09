#inheritance(parent-child relation):- parent class variables and functions can accessible by child
#without distubing parent class add some more values in new child class 
#types: single,multi, multi-level,hybrid,hirearchial
#single
""" class person:
    def details(self,name,age,gender):
        name=input("Enter your name: ")
        age=int(input("Enter you age: "))
        gender=input("Enter your gender: ")
        print(f"Employee name is:  {name}, his age is: {age} and his gender is: {gender}")

class update(person):
    def update_details(self,city):
        city=input("Enter your city: ")
        print(f"Employee city is: {city}")
child_obj=update()
child_obj.details('name','age','gender')
child_obj.update_details('city') """

#multi-level:- more than 2 class inherits
""" class Person:
    def personal(self,name,age,gender):
        self.name=input("Enter your name:")
        age= int(input("Enter your age: "))
        gender=input("Enter your gender: ")
        print(f"Person name is: {name}, his age: {age}, and his gender is: {gender}")
class Company(Person):
    def company_details(self,comp_name,comp_location):
        comp_name=input("Working Company name is: ")
        comp_location=input("Work location is: ")
        print(f"{self.name}'s Company name is: {comp_name}, and his work location is: {comp_location}")
class others(Company):
    def other_details(self,salary,designation):
        salary=int(input("Enter your Salary: "))
        designation=input("Enter your Designation: ")
        print(f"{self.name}'s getting salary is: {salary}, and his designation is: {designation}")

multi_level_obj=others()
multi_level_obj.personal('name','age','gender')
multi_level_obj.company_details('comp_name','comp_location')
multi_level_obj.other_details('salary','designation') """

#multiple inheritance:- 2 parents and child
""" class Person:
    def personal(self,name,age,gender):
        self.name=input("Enter your name:")
        self.age= int(input("Enter your age: "))
        self.gender=input("Enter your gender: ")
        print(f"Person name is: {name}, his age: {age}, and his gender is: {gender}")
class Company:
    def company_details(self,comp_name,comp_location):
        self.comp_name=input("Working Company name is: ")
        self.comp_location=input("Work location is: ")
        print(f"{self.name}'s Company name is: {self.comp_name}, and his work location is: {self.comp_location}")
class Others:
    def other_details(self,salary,designation):
        self.salary=int(input("Enter your Salary: "))
        self.designation=input("Enter your Designation: ")
        print(f"{self.name}'s getting salary is: {self.salary}, and his designation is: {self.designation}")
class Employee(Person,Company,Others):
    def combined_details(self):
        print("Employee Name: ", self.name)
        print("Employee Age: ", self.age)
        print("Employee Gender: ", self.gender)
        print("Employer Name : ", self.comp_name)
        print("Work Location : ", self.comp_location)
        print("Employee Salary: ", self.salary)
        print("Employee Designation: ", self.designation)
multiple_obj=Employee()
multiple_obj.personal('name','age','gender')
multiple_obj.company_details('comp_name','comp_location')
multiple_obj.other_details('salary','designation')
multiple_obj.combined_details()
 """

#Hirearchial:- opposite to multiple inheritance single parent but more than childs
""" class Family:
    def parent(self,fname,mname):
        self.fname=input("Enter your father name:")
        self.mname= input("Enter your mother name: ")
        print(f"Father is: {self.fname}, Mother is: {self.mname}")
class Son(Family):
    def son(self,sname):
        self.sname=input("Enter son name: ")
        print(f"{self.sname}'s, Father is: {self.fname}, Mother is: {self.mname}")
class Daughter(Family):
    def daughter(self,dname):
        self.dname=input("Enter daughter name: ")
        print(f"{self.dname}'s, Father is: {self.fname}, Mother is: {self.mname}")
son_obj=Son()
daugther_obj=Daughter()
son_obj.parent('fname','mname')
son_obj.son('sname')
daugther_obj.parent('fname','mname')
daugther_obj.daughter('dname') """

#Hybrid inheritance: combination any 2 inheritance type
""" class Wild_Animals:
    def horse(self):
        print(f"Wild Horse ")
    def elephant(self):
        print(f"Wild elephant ")

class Domestic_Animals():
    def cat(self):
        print(f"domestic cat ")
    def dog(self):
        print(f"domestic dog ")
class Tiger(Wild_Animals):
    def tiger(self):
        print("Tiger comes wild")
class Animals(Domestic_Animals,Tiger):
    def animals(self):
        print("Wild and Domestic Animals ")
animals_obj=Animals()
animals_obj.elephant()
animals_obj.tiger()
animals_obj.cat()
animals_obj.animals() """
#Same method name in inheritance follows mro(method resolution order) concept always takes left most params
""" class Wild_Animals:
    def cat(self):
        print(f"Wild Horse ")
class Domestic_Animals(Wild_Animals):
    def cat(self):
        print(f"domestic cat ")
cat_obj=Domestic_Animals()
cat_obj.cat() """

#Constructor in inheritance
""" class Teacher:
    def __init__(self,subject):
        self.subject=input("Enter your favourie subject: ")
        print("Teacher class constructor")
class student(Teacher):
    def student_fuc(self):
        print(f"Student clas without constructor ")
        print(" Student Favoutite subject is: ", self.subject)
student.obj=student('sub')
student.obj.student_fuc() """

#super()-incase multiple constructor is there on inheritance or base class methods want to access by derived class use super()
#constructor with super()
""" class A:
    def __init__(self):
        print("Base constructor of Class A")
class B:
    def __init__(self):
        print("Base Constructor of Class B")
class C(B,A):
    def __init__(self):
        super().__init__()
        print("Class C Constructor by default comes based on MRO concept")
sup_obj=C() """
#Single inherit with super()
""" class A:
    def func_a(self):
        print("Class A method")

class B(A):
    def func_b(self):
        super().func_a() #points base class of B,without mention actual class name you can access all methods from base class.
        print("Class B method")
single_obj=B()
single_obj.func_b() """

#Multiple Inheritance with super() and without super()
""" class Person:
    def personal(self):
        self.p_name='raj'
        print("Person Name is: ", self.p_name)
class Company:
    def company(self):
        self.c_name='hcl'
        print("Person Name is: ", self.c_name)
class Others:
    def others(self):
        self.salary="25LPA"
        self.designation="Devops"
        print(f"Person Name is: {self.p_name}, salary {self.salary},and his {self.designation}")
class Mul_Inherit(Person,Company,Others):
        print(f"Person Details are:", end="\n\n")
class with_super(Person,Company,Others):
     def with_super(self):
          print("Display Employee Detials: ", end="\n\n")
          super().personal()
          super().company()
          super().others()
with_super_obj=with_super()
with_super_obj.with_super()
without_sup_obj=Mul_Inherit()
without_sup_obj.personal()
without_sup_obj.company()
without_sup_obj.others() """

#multilevel Inheritance with super()
""" class A:
     def func1(self):
          print("Class A")

class B(A):
     def func2(self):
        print("Class B")
        super().func1()

class C(B):
     def func3(self):
        print("Class C")
        super().func2()

multi_level_obj=C()
multi_level_obj.func3()
 """
#Constructor with multi-level inheritance with super()
""" class A:
     def __init__(self):
         print("Constructor from Class A")
     def func(self):
          print("Class A Method")

class B(A):
     def __init__(self):
         print("Constructor from Class B")
         super().__init__()
     def func(self):
        print("Class B Method")
        super().func()

class C(B):
     def __init__(self):
         print("Constructor from Class C")
         super().__init__()
     def func(self):
        print("Class C Method")
        super().func()


obj1=C()
obj1.func() """

#keep common process in base class then other operation in derivate class to access common process use super()
class shape:
    def __init__(self,length,breadth):
        self.length=length
        self.breadth=breadth
        self.result=self.length * self.breadth
class rectangle(shape):
    def __init__(self, length, breadth):
        super().__init__(length, breadth)
        print("Area of Rectangle value is: ",self.result)
class cube(shape):
    def __init__(self, length, breadth,height):
        super().__init__(length, breadth)
        self.height=height
        print("VOlume of Cube value is: ", self.result * self.height)
class square(shape):
    def __init__(self, length):
        super().__init__(length, length)
        print("Area of Square value is: ", self.result)
s=square(2)
cu=cube(4,4,4)
rect=rectangle(2,4)
