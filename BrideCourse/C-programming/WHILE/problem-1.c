#include <stdio.h>

int main() {
    int num, sum = 0, temp;
    printf("Enter a number: ");
    if (scanf("%d", &num) == 1) {
        temp = num;
        if (temp < 0)
            temp = -temp;
        while (temp > 0) {
            sum += temp % 10;
            temp /= 10;
        }
        printf("Sum of digits of %d is %d\n", num, sum);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
