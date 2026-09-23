hindi=int(input("Hindi : "))
english=int(input("English : "))
math=int(input("Mathematics : "))
socal_science=int(input("Socal Science  : "))
science=int(input("Science  : "))
print("Hindi :",hindi)
print("English :",english)
print("Mathematics :",math)
print("Scoal Science :",socal_science)
print("Science :",science)

total_marks=(hindi+english+math+socal_science+science)
print("Total marks : ",total_marks)

aver_per=(total_marks)/5
print("Average Percentage : ",aver_per)

if(aver_per>=90):
    print("Grade : 'A+'")
elif(aver_per>=80):
    print("Grade : 'A'")

elif(aver_per>=70):
    print("Grade : 'B'")

elif(aver_per>=60):
    print("Grade : 'C'")

elif(aver_per>=50):
    print("Grade : 'D'")

elif(aver_per>=40):
    print("Grade : 'E'")
else:
    print("Grade = 'F'")
if (aver_per<=33):
    print("Result : 'Fail' ")
else: 
    print("Result : 'Passed ' ")