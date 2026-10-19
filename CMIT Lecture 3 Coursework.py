# This file builds and trains neural networks in PyTorch to classify inages, starting with MNIST digits and then CIFAR10 photos
import torch
import torchvision

print(torch.__version__)
print(torchvision.__version__)

from torchvision import datasets 
from torchvision.transforms import ToTensor # ToTensor is a tool that converts images to PyTorch tensors 

train_data = datasets.MNIST( # creates the training dataset from mnist and stores it in train_data, the bracket stays open so the arrguments can go on separate lines
    root = 'data', # folder where data gets saved
    train = True,      # this says "give me the training set", false gives the test set instead                    
    transform = ToTensor(), # applies ToTensor() to every image as it's loaded, this turns each image into a tensor & scales pixel values from 0-225 down to 0-1
    download = True) # downloads the data if you laready dont have the data, if its already there it skips 
test_data = datasets.MNIST( 
    root = 'data', 
    train = False, # train = false makes this the test set, no download = true needed as it has already been downloaded as this line has ran 
    transform = ToTensor()
)

# Visualisation 

 #Plot one train data 
print(train_data) # just prints a summary of the training data set 
print(test_data)
print(train_data.data.size()) # .data holds raw images .size() gives their shape 
print(train_data.targets.size()) # .targets holds the labels 

import matplotlib.pyplot as plt #plt is nickname
i=40000 #picks which image to look at, this is the 40001st image in the dataset 
plt.imshow(train_data.data[i], cmap='gray') # grabs image number i, a 28 * 28 grid of pixel values, plt.imshow() draws the grid as a picture, cmap='gray' shows it in grayscale, without this matplotlib colours the pixels with deafult yellow / green scheme
plt.title('%i' % train_data.targets[i]) # train_data.targets[i] is the true digit (0-9),'%i' % ... is an older way of formatting that turns the number into text, so the title is just e.g. 7.,  
plt.show() # this displays the figure

#Plot multiple
figure = plt.figure(figsize=(10, 8)) # creates an empty canvas that will hold all the images, this makes it 10 inches wide and 8 inches tall
cols, rows = 5, 5 # this sets 5 columns and 5 rows on separate lines 
for i in range(1, cols * rows + 1): # this is a loop that runs 25 times, starting from 1 (matplotlib)
    sample_idx = torch.randint(len(train_data), size=(1,)).item() #this is all indented which means it is inside the loop and runs once per image, torch.randint(len(train_data)=60000, size=(1,)) makes a random whole number between 0 and 59999, as a one-item tensor, item() turns that one item tensor into a plain Python number 
    img, label = train_data[sample_idx] # this grabs that image from the dataset, each item is a pair 
    figure.add_subplot(rows, cols, i) # this says to python put the next picture in slot number i of a grid with rows rows and cols columns, slot 1 is top left and fills across each row 
    plt.title(label) 
    plt.axis("off") # hides axis numbers and tick markjs so you can see clean images 
    plt.imshow(img.squeeze(), cmap="gray") # img has shape (1,28,28) where 1 is the colour channel, .squeeze() removes the extra dimension, which is what imshow wants fro greyscale, cmap="gray" shows it in greyscale
plt.show()  

# Preparing data for training with DataLoaders

from torch.utils.data import DataLoader
loaders = { # this creates a dictionary called loaders, which stores things under names
    'train' : torch.utils.data.DataLoader(train_data, # 'train' maps to a dataloader built from train_data
                                          batch_size=100, # each batch has 100 images, the network looks at 100 images at once then it updates its wreights. this gives 600 batches per epoch
                                          shuffle=True, # mixes up the order of the images 
                                          num_workers=1), # this is the number of background processes loading data, it's only about speed
    
    'test'  : torch.utils.data.DataLoader(test_data, 
                                          batch_size=100, 
                                          shuffle=True, 
                                          num_workers=1),
}
loaders

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Define Network 

class Net(nn.Module): # defines network as a class. nn.Module is PyTorch base class for all networks, so your Net inherits the machinery for tracking weights, gradients etc. 
    def __init__(self): # the constructor which runs once you create the network, this is where you declare the layers
        super(Net, self).__init__() # this runs the setup code of the parent class (nn.Module), you must include it or PyTorch will not register layers

        self.hidden1 = nn.Linear(28*28,512) # these are the layers declared in __init__, this is a fully connected layer with 784 inputs (28*28 pixels) 512 neurons, so a 512*784 weight matrix and a bias vector length 512
        self.relu = nn.ReLU() # The ReLU activation, max(0, x).
        self.hidden2 = nn.Linear(512,10) # second fully connected layer: 512 -> 10 outputs, one per digit 
        self.softmax = nn.Softmax() # turns the 10 outputs into probabilities that add to 1
        
# [batch_size, 28, 28]
    def forward(self, x): #defines what happens when the data goes through the network, x is a batch of images 
        x = x.view(x.size(0), -1)  # flattens each image, x.size(0) is the batch size and -1 means work out the rest, [100,28,28] becomes [100,784]. A plain limear layer needs a flat vector
        x = self.hidden1(x) # size: [batch_size,512]
        x = self.relu(x)
        x = self.hidden2(x) # size [ batch_size, 10]
        x = self.softmax(x) # probabilities of size [batch_size,10]
        return x # Pass through layer 1, then ReLU, then layer 2, then softmax, and hand back the result.

model = Net()
print(model) # Builds an actual network from the blueprint and prints its layer structure.

learning_rate = 0.01

optimizer = optim.Adam(model.parameters(), lr = learning_rate)   #optim.Adam is the type of optimizer. Adam is a smarter version of gradient descent that adapts the step size for each weight, so it usually trains faster and needs less tuning, model.parameters() hands it every weight and bias in your network (all the θ), so it knows what to update,lr = learning_rate sets the step size to 0.01.  
optimizer

loss_func = nn.NLLLoss()   #Negative Log-Likelihood Loss, which is used for classification. It looks at the probability the network gave to the correct class and turns it into a penalty:If the network gave the right answer a high probability, the loss is small and vice versa
loss_func

# Training Loop 

from torch.autograd import Variable
num_epochs = 10 # one epoch is one full pass through all 60000 training images

def train(num_epochs, model, loaders): # wraps the training code in a function, this takes the number of epochs, my model and the loaders dictionary
    
    model.train() # puts model in training mode
        
    # Train the model
    total_step = len(loaders['train']) # the number of batches in one epoch: 60000/100 = 600
        
    for epoch in range(num_epochs): # runs each epoch 10 times
        for i, (images, labels) in enumerate(loaders['train']): # loaders['train'] hands out batches of 100 images and their 100 labels, enumerate also gives a counter i (0, 1, 2 ... 599) so you know which batch you’re on, images has shape [100, 1, 28, 28] and labels has shape [100]
            # images is of size [batch_size, 28, 28]
            
            
            # gives batch data, normalize x when iterate train_loader
            b_x = Variable(images)   # batch x
            b_y = Variable(labels)   # batch y
            output = model(b_x)#[0]    
            
            #print(b_x.shape)
            #print(output.shape)
            #print(b_y.shape)
            loss = loss_func(output, b_y) # this measures the error, cimpares predictions to the true labels and produces one loss number for the batch
            
            # clear gradients for this training step   
            optimizer.zero_grad() # this clears old gradients as PyTorch accumulates gradients by default          
            
            # backpropagation, compute gradients 
            loss.backward()  # back propagation: this computes the gradient of the loss with respect to every weight             
            optimizer.step() # this updates the weigths using those gradients               
            
            if (i+1) % 100 == 0: # % gives the remainder, true every 100th batch
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))  # prints a progress line              
        
    
    
train(num_epochs, model, loaders) #everything above this line of code defines the function, this line runs it 

def test(): # defines the function, this takes no inputs because it uses the global model and loaders
    model.eval() # this puts the model in evaluation mode, which switches off training only behaviour
    test_loss = 0 
    correct = 0 # these are the 2 running totals, both starting at 0
    with torch.no_grad(): # this tells PyTorch not to rack gradients inside this block
        for data, target in loaders['test']: # goes through the test set one batch at a time, data is the images and target is the true labels
            output = model(data) # this runs the batch through the network to get predictions, shape [100,10]
            test_loss += F.nll_loss(output, target, size_average=False).item() # calculates the loss for the batch ans adds it to the runnig toal, F.nll_loss is the functional version of NLLLoss, size_average=False means the sum losses over the batch instead of averaging them, item() converst the result to a plain number
            pred = output.data.max(1, keepdim=True)[1] # works out the predicted digit for each image, .max(1,...) finds the largest value across the outputs, max returns their values and positions, keepdim=True keeps the shape as [100,1] rather than [100]
            correct += pred.eq(target.data.view_as(pred)).sum() # counts how many predictions were right: target.data.view_as(pred) reshapes the true labels to match pred’s shape, pred.eq(...) compares them, giving True where they match, .sum() counts the Trues, and it’s added to correct
        test_loss /= len(loaders['test'].dataset) #divides the toal loss by the number of test images to get the average loss per image 
        print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
          test_loss, correct, len(loaders['test'].dataset),
          100. * correct / len(loaders['test'].dataset)))
test() # runs the function

#Plot multiple
figure = plt.figure(figsize=(15, 12)) # bigger canvas 
cols, rows = 5, 5 # 5 * 5 grid
for i in range(1, cols * rows + 1): # runs 25 x
    sample_idx = torch.randint(len(test_data), size=(1,)).item() # picks a random test image
    img, label = test_data[sample_idx] # gets the image & its true label
    output = model(img) # feeds the image to the trained model to get its 10 output scores
    pred_y = torch.max(output,1) #returns the highest values and their positions
    pred_label = pred_y[1].numpy() # this takes the position of the highest score, which is the predicted digit ans converts it to a NumPy array so it can be put in a string
    figure.add_subplot(rows, cols, i) # puts the image in slot i
    plt.title('gt = ' + str(label) + ', pred = ' + str(pred_label))
    plt.axis("off") # hides axis
    plt.imshow(img.squeeze(), cmap="gray") # greyscale
plt.show()

# CNN class 

class CNN(nn.Module): # same blueprint pattern as Net: inherit from nn.Module, run the parent's setup
    def __init__(self): 
        super(CNN, self).__init__() 
# Input to conv1 will be image of shape [batch_size,1,28,28] (height and width are 28 for this example)
        self.conv1 = nn.Sequential(    #nn.Sequential builds several layers into one block that runs them in order
            nn.Conv2d(in_channels=1,out_channels=10,kernel_size=(3,3),padding=1), # nn.Conv2d is the main building block of a CNN, in_channels is how many channels come in, out_channels is how many filters it learns (how many fature maps come out), kernel_size(3,3) means each filter is a 3*3 windoe that slides over the image, padding=1 adds a border of zeros so the image keeps its height and width, the output of this conv is of shape [BS,10,28,28]
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size=(2,2)) #output of this is [BS,10,14,14]
        )
        self.conv2 = nn.Sequential( 
            nn.Conv2d(in_channels=10,out_channels=20,kernel_size=(3,3),padding=1), #output of this is [BS,20,14,14]
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2,2)) # output of this is [BS,20,7,7]
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=20,out_channels=30,kernel_size=(3,3),padding=1), #Output of this [BS,30,7,7]
            nn.ReLU(),
            nn.Conv2d(in_channels=30,out_channels=30,kernel_size=(3,3),padding=1),
            nn.ReLU()
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=30,out_channels=20,kernel_size=(3,3),padding=1), # [BS,20,7,7]
            nn.ReLU(),
            nn.Upsample(scale_factor=2)) # [BS, 20, 14, 14]
        
        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=20,out_channels=10,kernel_size=(3,3),padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=2)) #[BS,10,28,28]
        
        
        self.conv6 = nn.Sequential(
            nn.Conv2d(in_channels=10,out_channels=1,kernel_size=(1,1)), # uses a 1*1 kernel which mixes the 10 chennels down to 1 without looking at neighboring pixels
            
        )
        
        self.HiddenFinal = nn.Linear(1*28*28,10) 
        self.softmax = nn.Softmax() #this is a fully connected layer taking the flattened 784 values to 10 outputs then softmax for probabilities
        
            

    def forward(self, x,plot=False):

        x1 = self.conv1(x)
        x2 = self.conv2(x1)
        x3 = self.conv3(x2)
        x4 = self.conv4(x3)
        x5 = self.conv5(x4)
        x6 = self.conv6(x5) # this passes the data through each block in turn, keeping each result in its own variable
        
        x6b = x6.view(x6.size(0), -1) 
        x7 = self.HiddenFinal(x6b)
        x8 = self.softmax(x7) # flattens [BS, 1, 28, 28] to [BS, 784], applies the final linear layer, then softmax
        
        if plot:
            print('Input shape', x.shape)
            print('After layer 1', x1.shape)
            print('After layer 2', x2.shape)
            print('After layer 3', x3.shape)
            print('After layer 4', x4.shape)
            print('After layer 5', x5.shape)
            print('After layer 6', x6.shape)
            print('After layer 7', x7.shape)
            print('After layer 8', x8.shape)

        return x8 #if you call model(x, plot=true) it prints the shape after every stage so you can check your size tracking, otherwise it stays quiet then it returns the output

model = CNN()
print(model) # builds the network and prints its structure

#Look at layers
im,label = train_data[0] #[1,28,28] 
im = im.unsqueeze(1) # -> [1,1,28,28]
print(im.shape)

output = model(im,plot=True) # takes one image, adds a batch dimension and runs it thorugh with plot=True to print every layer's shape

learning_rate = 0.01

optimizer = optim.Adam(model.parameters(), lr = learning_rate)   

loss_func = nn.NLLLoss()    # these are recreates because the optimiser must be built form the new models parameters. I f you reused the old optimiser it would update the old network
loss_func

# Train:
num_epochs = 10

def train(num_epochs, model, loaders):
    
    model.train()
        
    # Train the model
    total_step = len(loaders['train'])
        
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(loaders['train']):
            # images is of size [batch_size, 28, 28]
            
            
            # gives batch data, normalize x when iterate train_loader
            b_x = Variable(images)   # batch x
            b_y = Variable(labels)   # batch y

            output = model(b_x)#[0]   
            

            loss = loss_func(output, b_y)
            
            # clear gradients for this training step   
            optimizer.zero_grad()           
            
            # backpropagation, compute gradients 
            loss.backward()                # apply gradients             
            optimizer.step()                
            
            if (i+1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))               
        
    
    
train(num_epochs, model, loaders)

# Homework 
from torchvision import datasets
from torchvision.transforms import ToTensor

train_data = datasets.CIFAR10(root='data', 
                            train=True,
                            transform=ToTensor(),
                             download=True)
test_data = datasets.CIFAR10(
    root = 'data', 
    train = False, 
    transform = ToTensor(),
    download=True
)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

import torch
from torch.utils.data import DataLoader
loaders = {
    'train' : torch.utils.data.DataLoader(train_data, 
                                          batch_size=100, 
                                          shuffle=True, 
                                          num_workers=0), # needs to be changed to 0, to avoid multiprocessing errors
    
    'test'  : torch.utils.data.DataLoader(test_data, 
                                          batch_size=100, 
                                          shuffle=True, 
                                          num_workers=0), # needs to be changed to 0
}
loaders

import numpy as np
import matplotlib.pyplot as plt
# Plot an image with the class

i=500# change index
im, label = train_data[i]
print('image shape:' , im.shape) 
im = np.transpose(im, [1,2,0])
print('image shape:' , im.shape) 
print('label is', label, '->', classes[label])
plt.imshow(im)
plt.title(classes[label])
