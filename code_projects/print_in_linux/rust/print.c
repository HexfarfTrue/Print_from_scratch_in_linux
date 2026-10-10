#include <stdint.h>

static const char message[] = "йцукен\n";

__attribute__((naked))
static void write(uint64_t fd,const char *buffer,uint64_t length) {
        __asm__ volatile(
            "mov $1, %%rax\n"
            "syscall\n"
            "ret\n"
            :
            :
            : "rax", "rcx", "r11", "memory"
        );
}

static uint64_t string_lenght (const char *str)
{
    uint64_t lenght = 0;
    
    while (str[lenght] != '\0') {
        lenght++;
    }
    return lenght;
}

void print(void) {
    write(
      1,
      message,
      string_lenght(message)
    );
}

__attribute__((naked))
void exit_program(int32_t code) {
    __asm__ volatile(
                "mov $60, %%rax\n"
                "syscall\n"
                "hlt\n"
                :
                :
                : "rax", "rcx", "r11", "memory"
    );
}
