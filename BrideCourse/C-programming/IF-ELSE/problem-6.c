#include <stdio.h>

int main() {
    int num;
    printf("Enter a number: ");
    if (scanf("%d", &num) == 1) {
        if (num > 0)
            printf("%d is positive\n", num);
        else if (num < 0)
            printf("%d is negative\n", num);
        else
            printf("The number is zero\n");
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
