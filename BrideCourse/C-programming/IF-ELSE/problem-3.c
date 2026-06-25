#include <stdio.h>

int main() {
    int a, b;
    printf("Enter two numbers: ");
    if (scanf("%d %d", &a, &b) == 2) {
        if (a > b)
            printf("Max (using if-else): %d\n", a);
        else
            printf("Max (using if-else): %d\n", b);
        int max = (a > b) ? a : b;
        printf("Max (using ternary): %d\n", max);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
