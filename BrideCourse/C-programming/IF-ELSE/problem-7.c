#include <stdio.h>

int main() {
    float m1, m2, m3, m4, m5, total, percentage;
    printf("Enter marks of 5 subjects: ");
    if (scanf("%f %f %f %f %f", &m1, &m2, &m3, &m4, &m5) == 5) {
        total = m1 + m2 + m3 + m4 + m5;
        percentage = total / 5;
        printf("Total = %.2f\n", total);
        printf("Percentage = %.2f%%\n", percentage);
        if (percentage >= 60)
            printf("Division: First\n");
        else if (percentage >= 50)
            printf("Division: Second\n");
        else if (percentage >= 40)
            printf("Division: Third\n");
        else
            printf("Division: Fail\n");
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
