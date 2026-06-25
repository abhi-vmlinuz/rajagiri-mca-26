#include <stdio.h>

int main() {
    int minutes, hours, remaining;
    printf("Enter minutes: ");
    if (scanf("%d", &minutes) == 1) {
        hours = minutes / 60;
        remaining = minutes % 60;
        printf("%d minutes = %d hours and %d minutes\n", minutes, hours, remaining);
    } else {
        printf("Invalid input.\n");
    }
    return 0;
}
