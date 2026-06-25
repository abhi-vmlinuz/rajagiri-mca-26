#include <stdio.h>

int main() {
    float principal, rate, time, si;
    printf("Enter Principal, Rate, and Time: ");
    if (scanf("%f %f %f", &principal, &rate, &time) == 3) {
        si = (principal * rate * time) / 100;
        printf("Simple Interest = %.2f\n", si);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
