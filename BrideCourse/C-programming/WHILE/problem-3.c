#include <stdio.h>

int main() {
    int num, original, reverse = 0, temp;
    printf("Enter a number: ");
    if (scanf("%d", &num) == 1) {
        original = num;
        temp = num;
        while (temp != 0) {
            reverse = reverse * 10 + temp % 10;
            temp /= 10;
        }
        if (original == reverse)
            printf("%d is a palindrome\n", num);
        else
            printf("%d is not a palindrome\n", num);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
