# handy-shellcode

## TODO

- [x] Create python script to complete challenge
- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

This code just takes whatever code you give it and tries to execute it, so if we give it just about any shellcode we will win

### How are we going to exploit it?

I went a little overboard with testing different shellcode methods. In my solution I have three similar but different methods to popping a shell. The first is just a copy and pasted sequence of bytes from shellstorm that we can send to the program. The next is using pwntools shellcraft library to generate shellcode for us and using that. Finally I used shellcrafts cat function to just cat the function without needing an interactive shell.

### The exploit

When we run solution.py we send it shellcode, pop a shell, and cat flag.txt. It's pretty simple.
