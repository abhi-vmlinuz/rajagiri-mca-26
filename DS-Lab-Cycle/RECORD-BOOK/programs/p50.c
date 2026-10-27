#include <stdio.h>

#define MAX 100

int binary_search(int array[], int size, int value)
{
    int low = 0;
    int high = size - 1;
    int middle;

    while (low <= high)
    {
        middle = (low + high) / 2;

        if (array[middle] == value)
        {
            return middle;
        }

        if (array[middle] < value)
        {
            low = middle + 1;
        }
        else
        {
            high = middle - 1;
        }
    }

    return -1;
}

int main(void)
{
    int array[MAX];
    int size;
    int value;
    int position;
    int i;

    printf("Enter the size of the sorted array: ");
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

    printf("Enter the element to search: ");
    scanf("%d", &value);

    position = binary_search(array, size, value);

    if (position == -1)
    {
        printf("Element %d not found.\n", value);
    }
    else
    {
        printf("Element %d found at position %d.\n", value, position + 1);
    }

    return 0;
}
