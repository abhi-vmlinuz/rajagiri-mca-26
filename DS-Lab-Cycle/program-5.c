#include <stdio.h>

#define MAX 100

int read_array(int array[])
{
    int size;
    int i;

    printf("Enter the size of the array (maximum %d): ", MAX);
    scanf("%d", &size);

    if (size < 1 || size > MAX)
    {
        return 0;
    }

    for (i = 0; i < size; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &array[i]);
    }

    return size;
}

void display_array(int array[], int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void sort_array(int array[], int size)
{
    int i;
    int j;
    int temporary;

    for (i = 0; i < size - 1; i++)
    {
        for (j = 0; j < size - i - 1; j++)
        {
            if (array[j] > array[j + 1])
            {
                temporary = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temporary;
            }
        }
    }
}

int main()
{
    int array[MAX];
    int size;

    size = read_array(array);
    if (size == 0)
    {
        printf("Invalid size.\n");
        return 0;
    }

    printf("Array before sorting: ");
    display_array(array, size);

    sort_array(array, size);

    printf("Array after sorting: ");
    display_array(array, size);

    return 0;
}
