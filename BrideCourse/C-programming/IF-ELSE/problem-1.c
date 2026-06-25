#include <stdio.h>

int main() {
    int a, b;
    printf("Enter two integers: ");
    if (scanf("%d %d", &a, &b) == 2) {
        if (a == b)
            printf("%d and %d are equal\n", a, b);
        else
            printf("%d and %d are not equal\n", a, b);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
