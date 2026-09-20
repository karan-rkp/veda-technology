#  variable 
a="name"                    # string
b=12                        # integer
c=12.23                     # float 
is_student=True             # boolean 

#  check type 
print(type(a))
print(type(b))
print(type(c))
print(type(is_student))

name=input("Enter your Name  : ")               # input as string
age =int(input("Enter your age : "))            # input as integer
height=float(input("Enter your height: "))      # input as float 



# type conversion  
b=str(b)                # integer to string 
c=int(c)                # float to integer 

#  check type 

print(type(b))
print(type(c))

#  formatting  

print(f"\nStudent Information")
print(f"Name   : {name}")
print(f"Age    : {age}")
print(f"Height  : {height:.2f}")

# example 1
product = input("Enter product name: ")
price = float(input("Enter price: "))
discount = float(input("Enter discount percentage: "))

discount_amount = price * discount / 100
final_price = price - discount_amount

print(f"\nProduct: {product}")
print(f"Original Price: ₹{price:.2f}")
print(f"Discount: {discount:.2f}%")
print(f"Discount Amount: ₹{discount_amount:.2f}")
print(f"Final Price: ₹{final_price:.2f}")
