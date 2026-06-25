#include <stdio.h>

int main() {
    float celsius, fahrenheit;

    printf("Enter temperature in Centigrade: ");
    
    if (scanf("%f", &celsius) == 1) {
        fahrenheit = (celsius * 9 / 5) + 32;

        printf("%.2f Celsius is equal to %.2f Fahrenheit\n", celsius, fahrenheit);
    } else {
        printf("Invalid input. Please enter a numeric value.\n");
    }

    return 0;
}
