#include <stdio.h>

int main() {
    float a, b, c;
    printf("Enter three sides of a triangle: ");
    if (scanf("%f %f %f", &a, &b, &c) == 3) {
        if (a + b > c && a + c > b && b + c > a) {
            if (a == b && b == c)
                printf("Equilateral triangle\n");
            else if (a == b || b == c || a == c)
                printf("Isosceles triangle\n");
            else
                printf("Scalene triangle\n");
        } else {
            printf("Not a valid triangle\n");
        }
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
