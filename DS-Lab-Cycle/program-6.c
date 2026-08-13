#include <stdio.h>

#define MAX 100

void read_array(int array[], int size)
{
    int i;

    for (i = 0; i < size; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &array[i]);
    }
}

void display_in_same_order(int array[], int size, int position)
{
    if (position == size)
    {
        return;
    }

    printf("%d ", array[position]);
    display_in_same_order(array, size, position + 1);
}

int main()
{
    int array[MAX];
    int size;

    printf("Enter the size of the array (maximum %d): ", MAX);
    scanf("%d", &size);

    if (size < 1 || size > MAX)
    {
        printf("Invalid size.\n");
        return 0;
    }

    read_array(array, size);

    printf("Array in the same order: ");
    display_in_same_order(array, size, 0);
    printf("\n");

    return 0;
}
