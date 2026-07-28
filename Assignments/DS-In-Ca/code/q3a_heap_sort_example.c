/*
 * Q3a: Heap Sort Example and Explanation
 *
 * Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure.
 * It works by first building a max heap from the input array, then repeatedly extracting
 * the maximum element and rebuilding the heap until the array is sorted.
 *
 * Example walkthrough:
 *
 * Input array: [4, 10, 3, 5, 1]
 *
 * Step 1: Build Max Heap
 * - Start from the last non-leaf node (index n/2 - 1 = 1)
 * - Index 1 (value 10): left child = 5, right child = 1. 10 > 5, 10 > 1 ✓
 * - Index 0 (value 4): left child = 10, right child = 3. 4 < 10, swap 4 and 10
 *   Array becomes: [10, 4, 3, 5, 1]
 *   Now check index 1 (value 4): left child = 5, right child = 1. 4 < 5, swap 4 and 5
 *   Array becomes: [10, 5, 3, 4, 1]
 * Max heap built: [10, 5, 3, 4, 1]
 *
 * Step 2: Extract Max and Rebuild Heap
 * - Swap root (10) with last element (1): [1, 5, 3, 4, 10]
 * - Heapify root on reduced heap (size 4): [5, 4, 3, 1, 10]
 * - Swap root (5) with last element (1): [1, 4, 3, 5, 10]
 * - Heapify root on reduced heap (size 3): [4, 1, 3, 5, 10]
 * - Swap root (4) with last element (3): [3, 1, 4, 5, 10]
 * - Heapify root on reduced heap (size 2): [3, 1, 4, 5, 10]
 * - Swap root (3) with last element (1): [1, 3, 4, 5, 10]
 *
 * Final sorted array: [1, 3, 4, 5, 10]
 *
 * Time Complexity:
 * - Build heap: O(n)
 * - n-1 extractions with heapify: O(n log n)
 * - Total: O(n log n) for all cases (best, average, worst)
 *
 * Space Complexity: O(1) - in-place sorting
 *
 * Properties:
 * - Not stable (relative order of equal elements may change)
 * - In-place algorithm
 * - Guaranteed O(n log n) worst-case performance
 */

#include <stdio.h>

void heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest])
        largest = left;

    if (right < n && arr[right] > arr[largest])
        largest = right;

    if (largest != i) {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest);
    }
}

void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    for (int i = n - 1; i > 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify(arr, i, 0);
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int arr[] = {4, 10, 3, 5, 1};
    int n = 5;

    printf("Original array: ");
    printArray(arr, n);

    heapSort(arr, n);

    printf("Sorted array:   ");
    printArray(arr, n);

    return 0;
}