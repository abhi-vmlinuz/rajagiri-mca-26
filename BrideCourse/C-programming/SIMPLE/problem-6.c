#include <stdio.h>

int main() {
    float kmph, mph;
    const float conversion_factor = 0.621371;

    printf("Enter speed in kilometers per hour: ");
    
    if (scanf("%f", &kmph) == 1) {
        mph = kmph * conversion_factor;

        printf("%.2f km/h is equal to %.2f mph\n", kmph, mph);
    } else {
        printf("Invalid input. Please enter a numeric value.\n");
    }

    return 0;
}
