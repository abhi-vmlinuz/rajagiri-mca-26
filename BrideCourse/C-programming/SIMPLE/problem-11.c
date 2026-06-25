#include <stdio.h>

int main() {
    float length, breadth, perimeter;
    printf("Enter length and breadth: ");
    if (scanf("%f %f", &length, &breadth) == 2) {
        perimeter = 2 * (length + breadth);
        printf("Perimeter = %.2f\n", perimeter);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
