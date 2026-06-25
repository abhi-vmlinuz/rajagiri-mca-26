#include <stdio.h>

int main() {
    float fahrenheit, celsius;
    printf("Enter temperature in Fahrenheit: ");
    if (scanf("%f", &fahrenheit) == 1) {
        celsius = (fahrenheit - 32) * 5.0 / 9.0;
        printf("%.2f Fahrenheit is equal to %.2f Celsius\n", fahrenheit, celsius);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
