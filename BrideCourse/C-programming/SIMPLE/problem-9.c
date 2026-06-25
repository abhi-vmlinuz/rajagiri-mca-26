#include <stdio.h>

int main() {
    float celsius, fahrenheit;
    printf("Enter temperature in Celsius: ");
    if (scanf("%f", &celsius) == 1) {
        fahrenheit = (celsius * 9.0 / 5.0) + 32;
        printf("%.2f Celsius is equal to %.2f Fahrenheit\n", celsius, fahrenheit);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
