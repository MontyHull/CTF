x = 895706419

# picoCTF{A_b1t_0f_b1t_sh1fTiNg_d79dd25ce3}


y = bin(x)
z = int(y,2)

#print(y,z)
a = y[2:]
b = a
length = len(a)
first = a[length-8:]
b = a[:length-8]
length = len(b)
second = b[length-8:]
b = b[:length-8]
length = len(b)
third = b[length-8:]
b = b[:length-8]
#print("yes")
#print("a = "+a)
#print("b = "+b)
#print("first = " + first)
#print("second = " +second)
#print("second = " +third)
#print("fourth = " +b)
#print(a)
#print(b+third+second+first)
#print("done")

one = chr(int(first,2))
two = chr(int(second,2))
three = chr(int(third,2))
four = chr(int(b,2))
print(four+three+two+one)
