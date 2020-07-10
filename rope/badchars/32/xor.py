x = "/bin/cat flag.txt"
y = "/bin//sh"
for letter in y:
    print(letter+"="+hex(ord(letter)^0xf6),end=" ")
print()
    #print(hex(ord(letter)^0xf6))
