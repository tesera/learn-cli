'''
'''
myList = [1,2,3,4,5,6,7,8,9,10]
#":" refers to list[ :num]
split = lambda num, lst: [lst[:num]] + split(num, lst[num:]) if len(lst) > num else [lst]
batches = 5
sets = split(batches,myList)
sets
myList.append(21)
sets = split(batches,myList)
sets
def square(x):
	return x*x
map(square, myList)
myList2 = map(square, myList)
zip(myList,myList2)
#functional programming ... lamda, map,  zip
#import multiprocessing
#Example
from multiprocessing import Pool

def f(x):
    return x*x

#http://docs.python.org/2/library/multiprocessing.html
#This allows mp.py to be called from the interpreter after importing
if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.apply_async(f, [10])    # evaluate "f(10)" asynchronously
    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"

#http://docs.python.org/2/library/functions.html
#The reduce function
#reduce(function, iterable[, initializer])

#Apply function of two arguments cumulatively to the items of iterable,
#from left to right, so as to reduce the iterable to a single value.
#For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
#calculates ((((1+2)+3)+4)+5). The left argument, x, is the
#accumulated value and the right argument, y, is the update value
#from the iterable. If the optional initializer is present,
#it is placed before the items of the iterable in the calculation,
#and serves as a default when the iterable is empty. If initializer
#is not given and iterable contains only one item, the first item is returned.
#Roughly equivalent to:

def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
    return accum_value

#S mapreduce
