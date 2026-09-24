import random
import os 
a=random.randint(0,100)
count=0
while True:
    try:
        n = int(input("Enter the number: "))
    except ValueError:
        print("Please enter a valid number.")
        continue
    count+=1
    
    
    if(n==a):
        print("Wow! you are gussing the number.  ")
        print("count : ",count)
        break
    elif(n>a):
        print("number is too high.")
    else:
        print("number is too low")
        
    