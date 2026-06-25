#include <stdio.h>

int main() {
    int num, reverse = 0, temp;
    printf("Enter a number: ");
    if (scanf("%d", &num) == 1) {
        temp = num;
        while (temp != 0) {
            reverse = reverse * 10 + temp % 10;
            temp /= 10;
        }
        printf("Reverse of %d is %d\n", num, reverse);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
