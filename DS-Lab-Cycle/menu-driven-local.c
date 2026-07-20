#include <stdio.h>
#include <stdlib.h>

void display(int arr[], int n) {
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

void insert(int arr[], int *n) {
    int val, pos;
    printf("Enter element & position (0 to %d): ", *n);
    if (scanf("%d %d", &val, &pos) != 2 || pos < 0 || pos > *n || *n >= 100) {
        printf("Invalid\n");
        return;
    }
    for (int i = *n; i > pos; i--) arr[i] = arr[i-1];
    arr[pos] = val;
    (*n)++;
}

void search(int arr[], int n) {
    int val;
    printf("Enter element to search: ");
    if (scanf("%d", &val) != 1) return;
    for (int i = 0; i < n; i++) {
        if (arr[i] == val) {
            printf("Found at index %d\n", i);
            return;
        }
    }
    printf("Not found\n");
}

void delete_element(int arr[], int *n) {
    int pos;
    printf("Enter position (0 to %d): ", *n - 1);
    if (scanf("%d", &pos) != 1 || pos < 0 || pos >= *n) {
        printf("Invalid\n");
        return;
    }
    for (int i = pos; i < *n - 1; i++) arr[i] = arr[i+1];
    (*n)--;
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
    int arr[100];
    int n = 0;
    int choice;
    while (1) {
        printf("1.Insert 2.Search 3.Delete 4.Sort 5.Display 6.Exit\nChoice: ");
        if (scanf("%d", &choice) != 1) break;
        if (choice == 1) insert(arr, &n);
        else if (choice == 2) search(arr, n);
        else if (choice == 3) delete_element(arr, &n);
        else if (choice == 4) { sort(arr, n); display(arr, n); }
        else if (choice == 5) display(arr, n);
        else if (choice == 6) break;
        else printf("Invalid choice\n");
    }
    return 0;
}
