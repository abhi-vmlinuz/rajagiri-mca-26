#include <stdio.h>

#define MAX 100

void swap(int *first, int *second)
{
    int temporary = *first;
    *first = *second;
    *second = temporary;
}

void heapify(int array[], int size, int root)
{
    int largest = root;
    int left = 2 * root + 1;
    int right = 2 * root + 2;

    if (left < size && array[left] > array[largest])
    {
        largest = left;
    }

    if (right < size && array[right] > array[largest])
    {
        largest = right;
    }

    if (largest != root)
    {
        swap(&array[root], &array[largest]);
        heapify(array, size, largest);
    }
}

void heap_sort(int array[], int size)
{
    int i;

    for (i = size / 2 - 1; i >= 0; i--)
    {
        heapify(array, size, i);
    }

    for (i = size - 1; i > 0; i--)
    {
        swap(&array[0], &array[i]);
        heapify(array, i, 0);
    }
}

void display(int array[], int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("%d ", array[i]);
    }

    printf("\n");
}

int main(void)
{
    int array[MAX];
    int size;
    int i;

    printf("Enter the size of the array: ");
    scanf("%d", &size);

    if (size < 1 || size > MAX)
    {
        printf("Invalid size.\n");
        return 0;
    }

    for (i = 0; i < size; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &array[i]);
    }

    printf("Before sorting: ");
    display(array, size);

    heap_sort(array, size);

    printf("After sorting: ");
    display(array, size);

    return 0;
}
