
#include <stdio.h>

void maxHeap(int arr[], int n, int i)
{
    int large = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[large])
    {
        large = left;
    }

    if (right < n && arr[right] > arr[large])
    {
        large = right;
    }

    if (large != i)
    {
        int t = arr[i];
        arr[i] = arr[large];
        arr[large] = t;

        maxHeap(arr, n, large);
    }
}

int main()
{
    int n, arr[10], i;

    printf("Enter the size of the array: ");
    scanf("%d", &n);

    if (n < 1 || n > 10)
    {
        printf("Invalid array size. Enter a size between 1 and 10.\n");
        return 1;
    }

    printf("Enter the elements:\n");

    for (i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
    }

    int start = n / 2 - 1;

    for (i = start; i >= 0; i--)
    {
        maxHeap(arr, n, i);
    }

    printf("Max Heap array: ");

    for (i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }

    printf("\n");

    return 0;
}

