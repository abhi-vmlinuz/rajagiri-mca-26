#include <stdio.h>

int main() {
    int age, roll, encoded, decoded;
    printf("Enter your age: ");
    if (scanf("%d", &age) != 1) {
        printf("Invalid input.\n");
        return 1;
    }
    printf("Enter your roll number: ");
    if (scanf("%d", &roll) != 1) {
        printf("Invalid input.\n");
        return 1;
    }
    encoded = age ^ roll;
    printf("Encoded value: %d\n", encoded);
    decoded = encoded ^ roll;
    printf("Decoded age: %d\n", decoded);
    return 0;
}
