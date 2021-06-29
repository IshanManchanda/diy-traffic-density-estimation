import numpy as np
import matplotlib.pyplot as plt

file1=open("count_+.txt","r")
file2=open("count.txt","r")

count_add=file1.readlines()
count_sub=file2.readlines()
#print(count_add)
x=[]
y=[]

for l in range(len(count_add)):
 
    x.append(l)
    y.append(int(count_add[l])+int(count_sub[l]))

plt.plot(x, y) 
    
# naming the x axis 
plt.xlabel('x - axis-time_frame') 
# naming the y axis 
plt.ylabel('y - axis_number_of_cars') 
    
# giving a title to my graph 
plt.title('cars_Density') 
    
# function to show the plot 
plt.show()

