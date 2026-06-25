#include <stdio.h>

int main() {
    float length, width, area, perimeter;
    printf("Enter length and width of the rectangle: ");
    if (scanf("%f %f", &length, &width) == 2) {
        area = length * width;
        perimeter = 2 * (length + width);

        printf("Area: %.2f\n", area);
        printf("Perimeter: %.2f\n", perimeter);
    } else {
        printf("Invalid input. Please enter numeric values.\n");
    }

    return 0;
}
