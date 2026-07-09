#Generator is a special kind of function (or expression) that yields values one at a time instead of returning 
# them all at once. This makes generators memory-efficient and great for working with large or infinite sequences.
#Generators are a simpler way to create iterators
def count_up(n):
    for i in range(1, n + 1):
        yield i
gen = count_up(5) #when call the method gives generator object memroy reference
print(next(gen)) # To fetch a single 
for value in gen:
    print(value)

#Key point: yield pauses the function and saves its state.Execution resumes from where it left off.