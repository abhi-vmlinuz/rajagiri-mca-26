#include <stdio.h>

int main() {
    int num;
    printf("Enter a number: ");
    if (scanf("%d", &num) == 1) {
        if (num % 2 == 0)
            printf("%d is even\n", num);
        else
            printf("%d is odd\n", num);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
