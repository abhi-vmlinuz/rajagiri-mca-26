#include <stdio.h>

int main() {
    int n, i, p = 1;
    printf("Enter number: ");
    if (scanf("%d", &n) == 1 && n > 1) {
        for (i = 2; i * i <= n; i++) 
            if (n % i == 0) p = 0;
    } else p = 0;

    printf("%d is %sprime.\n", n, p ? "" : "not ");
    return 0;
}
