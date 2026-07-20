#include <stdio.h>

int main() {
    int n, key, found = 0;
    printf("Enter number of elements: ");
    if (scanf("%d", &n) != 1 || n <= 0) return 1;
    int arr[n];
    printf("Enter %d elements: ", n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);
    printf("Enter element to search: ");
    if (scanf("%d", &key) != 1) return 1;
    printf("Occurrences of %d at indices: ", key);
    for (int i = 0; i < n; i++) {
        if (arr[i] == key) {
            printf("%d ", i);
            found = 1;
        }
    }
    if (!found) printf("None");
    printf("\n");
    return 0;
}
