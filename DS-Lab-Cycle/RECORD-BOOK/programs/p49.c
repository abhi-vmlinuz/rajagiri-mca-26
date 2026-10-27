#include <stdio.h>

#define MAX 100

int linear_search(int array[], int size, int value)
{
    int i;

    for (i = 0; i < size; i++)
    {
        if (array[i] == value)
        {
            return i;
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

    printf("Enter the element to search: ");
    scanf("%d", &value);

    position = linear_search(array, size, value);

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
