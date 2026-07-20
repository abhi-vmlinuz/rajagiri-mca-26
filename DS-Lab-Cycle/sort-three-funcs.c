#include <stdio.h>

void read(int arr[], int *n) {
    printf("Enter size: ");
    if (scanf("%d", n) != 1) return;
    printf("Enter %d elements: ", *n);
    for (int i = 0; i < *n; i++) scanf("%d", &arr[i]);
}

void disp(int arr[], int n) {
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

void sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

int main() {
    int arr[100], n;
    read(arr, &n);
    printf("Original: ");
    disp(arr, n);
    sort(arr, n);
    printf("Sorted: ");
    disp(arr, n);
    return 0;
}
