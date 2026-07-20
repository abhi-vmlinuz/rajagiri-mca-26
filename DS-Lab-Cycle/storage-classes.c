#include <stdio.h>

int global_var = 10;

void demo() {
    auto int local_var = 5;
    static int static_var = 20;
    register int reg_var = 30;
    
    printf("Local: %d, Static: %d, Register: %d, Global: %d\n", local_var, static_var, reg_var, global_var);
    local_var++;
    static_var++;
    global_var++;
}

int main() {
    demo();
    demo();
    return 0;
}
