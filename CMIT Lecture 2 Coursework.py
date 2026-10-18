#This file walks through turning a repeated calculation into reusable code, and finishes with a homweowk task on building a hilbert matrix

# Task 8 - from functions to classes 

#1- simple function def()
print('Task 8 – from "def" to advanced "class"')
print("First, a simple function (similar to MATLAB's function):")

def my_sum(x, n): # def tells python you are creating a function named my_sum, where x is the number you want to calculate the exponential of an n is how many terms to calculate
    """Compute sum_{k=0}^{n} x^k/k! using efficient recurrence.""" # this is a docstring, which is a comment that describes what the function does, here it calculates an approximation of e^x
    s = 1.0
    t = x
    for j in range(1, n+1): #s=s+t 
        t = x * t / (j+1) # calculate the next term in the series using the previous term, this avoids using powers and factorials form scratch
    return s # returns the final total when the loop finishes so you can use the answer outside the function 

x = 0.123 
answer = my_sum(x, 25)
print(f'my_sum({x}, 25) = {answer:.6f}, true exp = {math.exp(x):.6f}') 

# 2- introduction to classes 
# A class groups data (attributes) and functions (methods) together. This is the foundation of Object-Oriented Programming

#Class form 1 - stores both values 
print('Class form 1: Attributes set in __init__') #explains that this class stores its data inside __init__

class my_sum1: # class creates a class named my_sum1 which is the blueprint for creating objects
    def __init__(self, x=1.0, n=10): #__init__ runs automatically when you create a new object, seld refers to the particular object being created, x deafults to 1.0 if no value provided and n defaults to 10 if no value is provided
        self.x = x # stores the value of x inside the object so it can be used later, self.x and self.n belong to the object ans remember the values u gave it 
        self.n = n
    
    def comp(self): # this creates a method called comp, which performs the calculation, it only needs self because the object already stores x and n 
        s = 1.0 # stores the running total at 1.0, the first term in the exponential series 
        t = self.x # sets the current term to the object's stored value of x 
        for j in range(1, self.n + 1): # repeats the calculation using the objects stored n value
            s += t # adds the current term to the running total 
            t = self.x * t / (j + 1) # calculates the next term using the previous term 
        return s #returns the final approximation of e^x

# Usage
obj = my_sum1(x=0.789, n=15) #creates an object called obj and stores the variables inside
ans1 = obj.comp() #runs the comp() method on obj and stores it in ans1, the object already remembers x and n 
print(f'my_sum1(0.789, 15) = {ans1:.6f}, true exp = {math.exp(0.789):.6f}') #Prints the approximation to six decimal places and compares it with Python's built-in exponential calculation

x = 0.123 #stores a new value of x
ans = my_sum1(x, 25).comp() #creates a new my_sum1 object with x=0.123 ans n=25, calls .comp() to calculate the approximation and stores the result in ans
print(f'my_sum1({x}, 25) = {ans:.6f}, true exp = {math.exp(x):.6f}') # prints the approxiamtion and the true exponential value for x=0.123

#Class form 2 - stores x and provides n later 
print('Class form 2: x stored, n passed to comp()') #explains x is stored in the object but n is supplied when you run the calculation 

class my_sum2: 
    def __init__(self, x=1.0): #__init__ runs automatically when you create a new object, self refers to the object being created, x deafults to 1.0
        self.x = x 
    
    def comp(self, n=10): #this defines a method calles comp(), self identifies which object's stored x to use, n=10 means the number of terms defaults to 10, but you can choose a different value each time you call the method 
        s = 1.0 #starts the running total 
        t = self.x #sets the current term to the x value stored in the object 
        for j in range(1, n + 1): #repeats the calculation n tines 
            s += t
            t = self.x * t / (j + 1)
        return s

# Usage
obj2 = my_sum2(x=0.789) # creates an object called obj2 and stores x = 0.789 inside it and the value of n is not stored 
ans2 = obj2.comp(n=10) # runs the calculation using the stored x and newly supplied n=10, answer saved in ans2
print(f'my_sum2(0.789, 10) = {ans2:.6f}') #prints resul to 6dp

obj3 = my_sum2(x=0.123) #creates another object storing x=0.123
ans3 = obj3.comp(25) #calculates the approximation using n=25, writing 25 without "n=" is allowed becuade python matches it to the first argument after self
print(f'my_sum2(0.123, 25) = {ans3:.6f}, true exp = {math.exp(0.123):.6f}') #Prints the approximation to six decimal places and compares it with Python's built-in calculation of \(e^{0.123}\)

#Class form 3 - unlike forms 1 and 2, this class doesn't save any input values inside the object, you provide both values every time
print('Class form 3: no attributes, parameters passed to comp()')

class my_sum3:
    def __init__(self): #self on its own because no data needs to be stored 
        pass # means "do nothing", python requires an indented body after def, so pass acts as a playholder
    
    def comp(self, x=1.2, n=10): # x and n have deafult values, if you dont give them, python uses x=1.2 and n=10
        s = 1.0 
        t = x 
        for j in range(1, n + 1): # loops j thorugh 1 to n , range stops before the end number hence the + 1
            s += t # adds the current term to the total
            t = x * t / (j + 1)
        return s #hands the final total back to whoever called comp() it is not indented under the loop so runs when the loop is finished 

# Usage: note that named arguments can be swapped
ans4 = my_sum3().comp(n=10, x=0.789) #mysum_3() creates the object, then .comp(...) runs the calculation straight away
print(f'my_sum3(0.789, 10) = {ans4:.6f}') #prints answer to 6dp 

x = 0.123
ans5 = my_sum3().comp(x, 25)
print(f'my_sum3({x}, 25) = {ans5:.6f}, true exp = {math.exp(x):.6f}')

