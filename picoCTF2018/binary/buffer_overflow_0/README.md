# buffer overflow 0

## TODO

- [x] What is the exploitable piece of code?  
- [x] How are we going to exploit it?
- [x] The exploit
- [ ] Is there any similar challenges I can link to?

### Exploitable piece of code

In the first Binary Exploitation (BE) problem of picoCTF 2018 we are given the source code and the compiled binary for the challenge.

The first thing I would recommend for BE challenges is to try running the binary that you are given few times. On our first few runs of this problem we get:
```
./vuln
This program takes 1 argument
./vuln AAAAA
Thanks! Received: AAAAA
```
So it looks like this program takes our argument and prints it back to us. Now, if we open the source code for this problem we see that we have two functions besides main: vuln and segsegv_handler. The vuln function takes in a character pointer, which is pointed to our first argurment. The sigsegv_handler is a little more interesting. If you don't know about signals I would suggest you do some quick googling on them, and if you really want to understand them then I would recommend you reading the book "Advanced Programming in the UNIX Environment" by W. Richard Stevens and Stephen A. Rago. Once we know about signals we can see that in main we tell the handler function to handle all SEGSEGV signals, and this is going to be the key to our problem.

### How are we going to exploit it?

Once we see that sigsegv_handler handles all SIGSEGV signals, and that this function is what is going to print our flag, we need to find a way to create a SIGSEGV (also known as a segfault which is caused by a memory access violation). The most common way to do this is to find an array that we can write to much data to. We can see this in the vuln function.

### The exploit

Since we see that vuln takes our command line argument, and that it is being copied into a buffer that can only hold 16 bytes, we need to put enough characters into the buffer to access a piece of memory that we shouldn't be in. So our command should be
```
./vuln AAAAAAAAAAAAAAAAAAAAAAAAAAAA
picoCTF{example_flag}
```
