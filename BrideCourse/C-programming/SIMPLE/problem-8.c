#include <stdio.h>

int main() {
    float angle1, angle2, angle3;
    printf("Enter two angles of a triangle: ");
    if (scanf("%f %f", &angle1, &angle2) == 2) {
        angle3 = 180 - (angle1 + angle2);
        printf("The third angle is %.2f\n", angle3);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
