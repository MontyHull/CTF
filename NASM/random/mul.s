[BITS 64]
global _start

_start:
    ; set status code to 0
    ; rdi: first argument
    mov rdi, 0

    ; set syscall number to 0x3c => SYS_exit
    mov rax, 0x3c

    ; syscall time!
    syscall
