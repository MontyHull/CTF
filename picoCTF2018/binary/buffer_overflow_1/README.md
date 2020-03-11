# buffer overflow 1

## TODO

- [x] Create python script to complete challenge
- [ ] What is the exploitable piece of code?  
- [ ] How are we going to exploit it?
- [ ] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

### How are we going to exploit it?

We are going to try to overwrite the address that vuln will return to once we hit the end of that function. Since our input is not limited with gets, and our buffer can only hold 32 bytes, we know that we can write to the stack and write instructions where we want them.

### The exploit

Since we know we can write to the stack, we first have to know how to get there. We see that our buffer can only hold 32 Bytes so we must first write 32 bytes to fill it. Then we must write 12 more bytes to skip over the other values that
