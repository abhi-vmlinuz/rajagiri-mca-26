#include <stdio.h>

int main() {
    int a, b, c;
    printf("Enter three numbers: ");
    if (scanf("%d %d %d", &a, &b, &c) == 3) {
        int max;
        if (a >= b && a >= c)
            max = a;
        else if (b >= a && b >= c)
            max = b;
        else
            max = c;
        printf("Max (using if-else): %d\n", max);
        max = (a > b) ? ((a > c) ? a : c) : ((b > c) ? b : c);
        printf("Max (using ternary): %d\n", max);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
