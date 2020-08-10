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

bextr is a bit extractor, so whatever is in the second source operand (rdx for us) is used as a way to tell how many bits to extract from the first source operand (rcx in our case) and write to the destination operand (rbx). 

stosb will store whatever is in the source operand (al) and write it to the memory in our destination operand ([rdi]) and then increment the destination by one. 

So knowing this what we can: 
- find multiple strings saved in our file that we can use to spell "flag.txt" 
- pop the address where we are going to write flag into rdi
- zero out al so that xlatb is only offset by rbx 
- use bextr to get rbx pointing to where each of our characters in memory are
- use xlat to write "f" into al
- use stosb to write al into memory
- repeat until flag.txt is in memory
- pop the address of flag.txt into rdi
- call print_file()

# What it looks like

I found all of my strings here:

```
f - 0x004003c1+3 - libfluff.so
l - 0x004003c1+0 - libfluff.so
a - 0x00400415+3 - _edata
g - 0x004003cd+1 - _gmon_start_
. - 0x004003c1+8 - libfluff.so
t - 0x00400415+4 - _edata
x - 0x004006c4+4 - nonexistent
t - 0x00400415+4 - _edata
```

And after writing a quick function to add them all to an array I was able to get my string into memory and win using the solution.py file