#include <stdio.h>

int main() {
    float kmph, mph;
    printf("Enter speed in kilometers per hour: ");
    if (scanf("%f", &kmph) == 1) {
        mph = kmph * 0.621371;
        printf("%.2f km/h is equal to %.2f mph\n", kmph, mph);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
