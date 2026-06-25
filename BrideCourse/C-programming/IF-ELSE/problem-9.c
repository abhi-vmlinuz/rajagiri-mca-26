#include <stdio.h>

int main() {
    int age;
    printf("Enter your age: ");
    if (scanf("%d", &age) == 1) {
        if (age >= 18)
            printf("You are eligible to vote\n");
        else
            printf("You are not eligible to vote\n");
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
