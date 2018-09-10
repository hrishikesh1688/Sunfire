import datetime
min=610
hrs=min//60
rem=min%60

print(hrs,rem)

p=(4,5)
x,y=p
print(x)

data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
for l in range(0,len(data)+1):
    print(data[l])
phn_nos=[]
data=('Jeevan','jee@gmail.com','9271442321','9252535154')
name,email,*phn_nos=data
print(phn_nos,name,email)