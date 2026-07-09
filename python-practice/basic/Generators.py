#Generators are functions that can pause and resume their execution.When a generator function is called, it returns a generator object, which is an iterator(traverse to all values one by one).
#Generators allow you to iterate over data without storing the entire dataset in memory. Instead of using return, generators use the yield keyword.
#A simple generator function:
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)

#The yield keyword is what makes a function a generator. When yield is encountered, the function's state is saved, and the value is returned. The next time the generator is called, it continues from where it left off.Unlike return, which terminates the function, yield pauses it and can be called multiple times.