#include <stdio.h>

int main() {
    float m1, m2, m3, total, average;
    printf("Enter marks of 3 subjects: ");
    if (scanf("%f %f %f", &m1, &m2, &m3) == 3) {
        total = m1 + m2 + m3;
        average = total / 3;
        printf("Total = %.2f\n", total);
        printf("Average = %.2f\n", average);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
