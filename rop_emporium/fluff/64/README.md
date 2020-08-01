# Fluff

The concept here is identical to the write4 challenge. The only difference is we may struggle to find gadgets that will get the job done. However if we take our time to consider all our options, we'll succeed.

## What we are given

In the description it states that all we need to do is call the print_file() function with "flag.txt" as an argument. We are also told that there is a questionableGadget object and a usefulFunction in our binary. So we know that we need to find a place to write "flag.txt" into memory, find a way to write it to that memory, then call print_file() with the memory address of "flag.txt" in rdi. After some r2 magic we know that our writable memory is:

```
18  0x00000df0    0x8 0x00600df0    0x8 -rw- .init_array
19  0x00000df8    0x8 0x00600df8    0x8 -rw- .fini_array
20  0x00000e00  0x1f0 0x00600e00  0x1f0 -rw- .dynamic
21  0x00000ff0   0x10 0x00600ff0   0x10 -rw- .got
22  0x00001000   0x28 0x00601000   0x28 -rw- .got.plt
23  0x00001028   0x10 0x00601028   0x10 -rw- .data
24  0x00001038    0x0 0x00601038    0x8 -rw- .bss
```

our print_file() is called in our useful function here:

```
sym.usefulFunction ();
    0x00400617      55             push rbp
    0x00400618      4889e5         mov rbp, rsp
    0x0040061b      bfc4064000     mov edi, str.nonexistent    ; 0x4006c4 ; "nonexistent"
    0x00400620      e8ebfeffff     call sym.imp.print_file
    0x00400625      90             nop
    0x00400626      5d             pop rbp
    0x00400627      c3             ret
```

and our questionable gadgets held these:
```
0x00400628      d7             xlatb
0x00400629      c3             ret
0x0040062a      5a             pop rdx
0x0040062b      59             pop rcx
0x0040062c      4881c1f23e00.  add rcx, 0x3ef2
0x00400633      c4e2e8f7d9     bextr rbx, rcx, rdx
0x00400638      c3             ret
0x00400639      aa             stosb byte [rdi], al
0x0040063a      c3             ret
```

## How to use what we found

After looking at the questionable gadgets I realized I didn't know what any of them did, so I started googling to find out. 

xlatb is a lookup table, and will put whatever is in [rbx+al] into al.

bextr is a bit extractor, so whatever is in the second source operand (rdx for us) is used as a way to tell how many bits to extract from the first source operand and write to the destination operand. 

stosb will store whatever is in the source operand (al) and write it to the memory in our destination operand ([rdi]) and then increment the destination by one. 

So knowing this what we can: 
- write "flag.txt" into our buffer so that we can look for it in memory later 
- pop the address where we are going to write flag into rdi
- zero out al so that xlatb is only offset by rbx 
- use bextr to get rbx pointing to where flag is written at the start of our buffer
- use xlat to write "f" into al
- use stosb to write al into memory
- repeat until flag.txt is in memory
- run out of room on the stack and need to reset rsp to our initial buffer
- pop the address of flag.txt into rdi
- call print_file()

# What it looks like

It all seems to work in gdb. When I get to my call print_file() portion everything looks good:

```
 RAX  0x0
 RBX  0x7fffffffe198 ◂— 0x4141414100000000
 RCX  0x7fffffffe198 ◂— 0x4141414100000000
 RDX  0x3000
 RDI  0x601028 (data_start) ◂— 'flag.txt'
 RSI  0x7ffff7dae7e3 (_IO_2_1_stdout_+131) ◂— 0xdaf8c0000000000a /* '\n' */
 R8   0x7ffff7bef740 ◂— 0x7ffff7bef740
 R9   0x7ffff7bef740 ◂— 0x7ffff7bef740
 R10  0xfffffffffffff526
 R11  0x246
 R12  0x400520 (_start) ◂— xor    ebp, ebp
 R13  0x7ffff7dcc940 (pwnme+150) ◂— nop    
 R14  0x7478742e67616c66 ('flag.txt')
 R15  0x4141414100000000
 RBP  0x4242424242424242 ('BBBBBBBB')
*RSP  0x7fffffffe1b8 —▸ 0x4006a3 (__libc_csu_init+99) ◂— pop    rdi
*RIP  0x400620 (usefulFunction+9) ◂— call   0x400510
[ DISASM ]─────────────────────────────────────────────────────────────────────────────────────
   0x4006a4 <__libc_csu_init+100>      ret    
    ↓
   0x4006a3 <__libc_csu_init+99>       pop    rdi
   0x4006a4 <__libc_csu_init+100>      ret    
    ↓
   0x4006a3 <__libc_csu_init+99>       pop    rdi
   0x4006a4 <__libc_csu_init+100>      ret    
    ↓
 ► 0x400620 <usefulFunction+9>         call   print_file@plt <print_file@plt>
        rdi: 0x601028 (data_start) ◂— 'flag.txt'
        rsi: 0x7ffff7dae7e3 (_IO_2_1_stdout_+131) ◂— 0xdaf8c0000000000a /* '\n' */
        rdx: 0x3000
        rcx: 0x7fffffffe198 ◂— 0x4141414100000000
 
   0x400625 <usefulFunction+14>        nop    
   0x400626 <usefulFunction+15>        pop    rbp
   0x400627 <usefulFunction+16>        ret    
 
   0x400628 <questionableGadgets>      xlatb  
   0x400629 <questionableGadgets+1>    ret    

```

And as I step through the print function I even get the flag printed out:

'''
pwndbg> 
ROPE{a_placeholder_32byte_flag!}

Program received signal SIGSEGV, Segmentation fault.
0x0000000000601028 in data_start ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[ REGISTERS ]────────────────────────────────────────────────────────────────────────────────────
*RAX  0x0
 RBX  0x7fffffffe198 —▸ 0x7fffffffe100 ◂— 0xaf7f36e4f0ee5a00
*RCX  0x602010 ◂— 0x0
*RDX  0x0
*RDI  0x21
*RSI  0x1
*R8   0x21f
*R9   0x602260 ◂— 0x0
*R10  0x0
*R11  0x206
 R12  0x400520 (_start) ◂— xor    ebp, ebp
 R13  0x7ffff7dcc940 (pwnme+150) ◂— nop    
 R14  0x7478742e67616c66 ('flag.txt')
 R15  0x4141414100000000
*RBP  0x4006a3 (__libc_csu_init+99) ◂— pop    rdi
*RSP  0x7fffffffe1c8 —▸ 0x400610 (main+9) ◂— mov    eax, 0
*RIP  0x601028 (data_start) ◂— 'flag.txt'
[ DISASM ]─────────────────────────────────────────────────────────────────────────────────────
 ► 0x601028 <data_start>    insb   byte ptr [rdi], dx

[ STACK ]──────────────────────────────────────────────────────────────────────────────────────
00:0000│ rsp  0x7fffffffe1c8 —▸ 0x400610 (main+9) ◂— mov    eax, 0
01:0008│      0x7fffffffe1d0 ◂— 0x4242424242424242 ('BBBBBBBB')

'''

but when I try to run on the command line all I get is a segfault:

'''
$/rop_emporium/fluff/64$ cat payload.txt | ./fluff 
fluff by ROP Emporium
x86_64

You know changing these strings means I have to rewrite my solutions...
> Thank you!
Segmentation fault
'''


## Other attempts

After looking at my code, I realized that since I know where flag.txt is on the stack, I should just be able to call print_file() on it using that address, so I did and got the same results. It prints out fine in gdb, but just a segfault on the command line. 