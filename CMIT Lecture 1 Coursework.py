
#This file walks through python fundamentals and concludes with building and analysing a Hilbert Matrix 

# Task 1 - standard arithmetic operations and print statements

print('Task 1 --- Basic commands for scalar numbers / print')
a=30000
b=7.3
c=a*13
d=30000%9   # gives the remainder of a division
e=11.34 // 5 # floor division, divides then rounds down to the nearest whole number
print('a=', a, ', b =', b, ', c=a/5=', c,', d=30000%9 =', d, ', e = 11.34 // 5 =', e, '\n')

# Task 2 - string operations

print('Task 2 --- Basic commands for processing/extracting texts')
F = 'CMIT Lecture 1 Coursework.py' #stores the text in variable F
a = F[0:3] #start at position 0 and stop before position 3 (poition 0,1,2)
b = F[1:4] #postions 1,2,3
c = F[-1:] #last character
what_is = F[-2] #second last character
print('\tStrings in F =', F) 
print('a = F[0:3] =', a, ', b=F[1:4]=', F[1:4], '  F[-2]=',
      what_is, ' F[-2:] =', F[-2:], 'c=F[-1:]=', c)

# split() breaks the string into pieces wherever it finds a chosen character and gives you the peices in a list
a = F.split('.')[0]   # 'CMIT Lecture 1 Coursework'
b = F.split('.')[1]   # 'ipynb'
print('String SPLIT 1 for F =', F, ': to', a, ' and ', b, ' or', F.split('.')[-1])

# string concatenation means joining strings together, end to end, which is done with +
C = F + '.zip'
print('Consider C =', C)

# Task 3 - math functions & user-defined functions 

print('\nTask 3 --- calling a built-in math function or defining own')
import math # built in toolbox 

a = math.exp(1.0)   # e^1
b = math.pi # the dot means "from the math toolbox, take this one"
print('math.exp(1)=', a, ', math.pi=', b, ', math.sinh(1)=', math.sinh(1.0))

# Custom implementation of hyperbolic sine
def my_sinh(x): # def means define a function, x is the input variable
    y = math.exp(x) 
    ym = math.exp(-x)
    return (y - ym) / 2.0 # return is the output of the function, which is the value of sinh(x)

print('my_sinh(1.0)=', my_sinh(1.0), '(compare with the built-in function)') # this runs the function my_sinh() with input 1.0 and prints the output

# Task 4 - conditional statements 

print('\nTask 4 --- Programming basics: (i) "if" conditional') 
import numpy as np #NumPy is a toolbox for working with numbers, arrays and matrices
from numpy.random import rand as rd #numpy.random.rand() generates a random number in [0,1), we rename it to rd for convenience

x = rd() - 0.5   # rd() is the shortcut from the import, the brackets allow the code to run, subtracting 0.5 shifts the range to [-0.5, 0.5)
y = np.random.rand() - 0.5 # both lines of code do the same thins, this just doesn't use the shortcut rd()

print('x=', x, ' y=', y) 

# Standard if-else
if x >= 0.0:
    print('non-negative x')
else: # means otherwise
    print('\tnegative x')

if y >= 0.1:
    print('positive y and y>=0.1')
else:
    print('\tless than 0.1')
print('|')

# pattern: value_if_true  if  condition  else  value_if_false
x1 = 'non-negative x' if x >= 0.0 else '\tnegative x' 
y1 = 'positive y and y>=0.1' if y >= 0.1 else '\tless than 0.1'
print(x1, ' | ', y1)

# Task 5 - formatted printing & image loading 

print('\nTask 5 --- Formatted print and Image loading')

a = r"C:\cmit2025\week1\File2.py"   # "r" raw string, backslashes are not treated as escape characters
b = 789
c = math.pi

# Old-style formatting using %

print(a, '\t| b=', b, '\t | c=', c) # this is the simplest way to print, but it is not very flexible
print(a.split('\\')[-1], '\t\t\t| b=%04d' % b, '\t | c= %.4f' % c) # the % slots a value into a placeholder in the text, %04d means a whole number, 4 characters wide, padded with zeros, so 789 becomes 0789, %.4f means a decimal with 4 digits after the point, so π becomes 3.1416

# New-style f-string (Python 3.6+)
name = a.split("\\")[-1] 
print(f"{name} \t\t\t| b={b:04d} \t | c={c:.4f}") # puttging an f before the string allows anything inside {} to be swapped for its value, after the colon you add the same formatting codes but it is just easier to read

# Image reading and display (requires the image files to exist)
import os, cv2, matplotlib.pyplot as plt # this loads 3 toolboxes in one line separated by commas, "os" is for working with files and oflders on your computer, "cv2" is OpenCV for reading and processing images, "matplotlib.pyplot" 

my_image = 'Liver.jpg' # these are just text, storing 2 filenames in variables
my_imag2 = 'Glasgow.jpg'

# Safety check to avoid FileNotFoundError
if os.path.exists(my_image) and os.path.exists(my_imag2): # is there a file with this name in the current folder, answers True or False
    A  = cv2.imread(my_image, 1)          # loads the image in colour, this is stored as a grid of numbers, with 3 values per pixel ( Color, BGR format as OpenCV uses BGR instead of RGB )
    A0 = cv2.imread(my_image, 0)          # loads the image in grayscale, with just one valiue per pixel
    A = cv2.cvtColor(A, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for matplotlib

    B  = cv2.imread(my_imag2, 1) # this just does the same but for the second image
    B0 = cv2.imread(my_imag2, 0)
    B = cv2.cvtColor(B, cv2.COLOR_BGR2RGB)

    fig = plt.figure(figsize=(12, 12)) # creates an empty figure, the figsize is in inches, so 12x12 is a square figure
    ax1 = fig.add_subplot(2, 2, 1) # adds one panel to the canvas, these numbers mean a grid of 2 rows, abd 2 colums and this is panel number 1)
    ax1.imshow(A); ax1.set_title('Colour Image') # imshow displays the image, set_title adds a title to the panel
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.imshow(A0, cmap='gray') # tells matplotlib to draw it in shades of gray, without it matplotlib can apply odd default colours to a greyscale image
    ax2.set_title('Gray Image'); ax2.axis('off') # hides the numbered axis around the image
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.imshow(B); ax3.set_title('Colour Image')
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.imshow(B0, cmap='gray')
    ax4.set_title('Gray Image'); ax4.axis('off') # the ; allows you to put 2 commands on the same line, so you don't have to write ax4.set_title('Gray Image') and ax4.axis('off') on 2 lines

    print('Images plotted - close the plot window to continue (if running as .py)')
    plt.show() # this is what actually draws the figure on the screen, without it you won't see anything, as a plain .py file will just run the code and exit without showing the figure
else:
    print('Image files not found. Skipping image demonstration. You can download any .jpg images and name them Liver.jpg and Glasgow.jpg to test this feature.') # this runs if either image is missing, prints a message instead of an error

    # Task 6 - for loops, Taylor series for exp(x)
   
print('\nTask 6 --- Programming basics: (ii) "for" loop') # n is a blank line

# approach 1 - recomputes x**i and factorial(i) each time, which is inefficient but simple to understand

print('\tfor -- example 1: Direct call to math.factorial') # t is a tab 
n = 8  # how many terms to include in the Taylor series
s1 = 1.0  # is the running total, starts at 1.0 because the first term of the Taylor series is 1
x = 0.123 # is the number we are computing e to the power of 
for i in range(1, n+1): # the for loop repeats the intended lines again with i changing each time, the range here gives 1,2,3,...,n 
    s1 += x**i / math.factorial(i)   # Alternatively: s1 = s1 + ...
print('s1 =', s1, ' (n=', n, ')  True exp(x)=', math.exp(x)) # sh

# approach 2 - reccurance 
print('\n\tfor -- example 2: Efficient recurrence (using the previous term)')
s2 = 1.0
x = 0.123
t = x          # First term t_1 = x, this holds the current term in the Taylor series, which is updated each time through the loop
n = 25
for j in range(1, n+1):
    if j % 5 == 0 or j == 1:   # Print every 5 steps to reduce clutter
        print('j=', j, ' term t_j=', t)
    s2 += t # Add the current term to the running total
    t = x * t / (j+1) # turns t into the next term, ready for the next loop
print('When x=', x, ',  s2 = %.8f' % s2, 'NB exp(x) = %.8f' % math.exp(x),
      ' error = {:.2e}'.format(s2 - math.exp(x))) 

# Task 7 - NumPy Arrays & PyTorch Tensors
print('\nTask 7 --- Programming basics: (iii) arrays, matrices, tensors')
import numpy as np

print('\n\t vectors a b c')
a = np.arange(4) # this is like range(), but it gives you a NumPy array instead of a list, and it can be used for vectorised operations [0,1,2,3]
b = np.arange(2, 7)  # [2,3,4,5,6]
print('a=', a, 'b=', b)

h = 0.125 # step size for the next array
c = np.arange(3.0, 4.0+h, h)   # arrange always exclues the stop value
print('c =', c)
print('Length: a b c =', len(a), len(b), len(c), ' and shape a =', a.shape) # len() counts the items:4,5,9 and .shape gives the dimensions as a tuple, for a it is (4,) which is a 1D array with 4 elements

# Random matrix
ar = np.random.rand(3, 5) # creates a 3x5 matrix/grid of random numbers in [0,1)
print('ar =\n', ar) # this puts the matrix on a new line and is displayed neatly
print('HERE ar shape =', ar.shape, ' after conversion a`s shape =',
      a[:, np.newaxis].shape, 'or to row =', a[np.newaxis, :].shape) # a[:, np.newaxis] turns it into a column (4 rows, 1 column), a[np.newaxis, :] turns it into a row (1 row, 4 columns) 

# Slicing arrays
a1 = ar[0:2, 0:2] # rows 0 and 1, columns 0 and 1 
a2 = ar[-2:, -2:] # last 2 rows and last 2 columns, the ":" means "all of" in that dimension
print('ar`s submatrices =\n', a1, ' and\n', a2)

# 3D Tensor
at = np.random.rand(3, 5, 2) # a tensor is just an array with 3 or more dimensions, it is 3 grids stacked up, each with 5 rows and 3 columns
print('HERE at (tensor) shape =', at.shape, ' after conversion at`s shape =',
      at[np.newaxis, :].shape) # this adds a new dimension at the front so the shape becomes (1, 3, 5, 2). A common use later is adding a "batch" dimension for neural networks.

# PyTorch Tensors

print('pytorch has its own set of commands similar to numpy')
import torch #PyTorch package

t1 = torch.rand(()) #torch.rand is the pytorch version of np.random.rand, it gives random decimals between 0 and 1, the difference is that PyTorch wants the shape as one tuple, so there are extra brackets for a scalar
ta = torch.rand((3, 5))      # 3x5 tensor
print(t1, '\n', ta) # The \n puts a line break between the two 
print('Minor point: np.random.seed(42) and torch.manual_seed(42) cannot agree on rd') # computers dont make truly random numbers, they follow a formula and a seed is the starting value for it. if you set the same seed you get the same random numbers every run whuch is useful for repeatable experiments
print('Usually we use: torch.from_numpy or  ta.numpy()') # torch.from_numpy turns a numpy array into a tensor and ta.numpy() turns a tensor into a numpy array, so you can switch between the two easily

import datetime # built in module for working with dates and times
time0 = datetime.datetime.now().strftime("%Y %m %d @ %H:%M:%S") # datetime.datetime.now() gets the current date and time from your computer, .strftime(...) means "string format time". It turns the time into text, laid out however you describe in the quotes
print('\t time =', time0)

# Homework 1 - Hilbert Matrix, fix the code below to generate the Hilbert matrix H with H_{ij}=1/(i*j - 1) for i,j = 1,...,n. Then compute its condition number cond(H) for n=4 and n=8 using numpy.linalg.cond. Show your answers (print them) in the next lecture.

# TASK: Write a code to generate the Hilbert matrix H with H_{ij}=1/(i*j - 1)
# for i,j = 1,...,n. Then compute its condition number cond(H) for n=4 and n=8
# using numpy.linalg.cond.
# Show your answers (print them) in the next lecture.

import numpy as np

def hilbert(n):
    # Implement the Hilbert matrix
    # Hint: use nested loops or vectorized operations
    H = np.zeros((n, n))
    for i in range(1, n+1):
        for j in range(1, n+1):
            H[i-1, j-1] = 1.0 / (i+j - 1) # Hilbert matrix uses addition not multiplication
    return H

# Compute for n=4 and n=8
for n in [4, 8]:
    H = hilbert(n)
    cond = np.linalg.cond(H)
    print(f"Condition number for n={n}: {cond:.3e}")

# Bonus (vectorized version):
# i = np.arange(1, n+1).reshape(-1,1)
# j = np.arange(1, n+1).reshape(1,-1)
# H = 1.0 / (i*j - 1)
# print(np.linalg.cond(H))