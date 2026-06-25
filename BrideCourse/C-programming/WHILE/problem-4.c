#include <stdio.h>

int main() {
    int a, b, diff;
    printf("Enter two numbers: ");
    if (scanf("%d %d", &a, &b) == 2) {
        diff = a - b;
        if (diff < 0)
            diff = -diff;
        printf("Difference of %d and %d is %d\n", a, b, diff);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
