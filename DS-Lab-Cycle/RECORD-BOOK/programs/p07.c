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

void display_in_reverse(int array[], int position)
{
    if (position < 0)
    {
        return;
    }

    printf("%d ", array[position]);
    display_in_reverse(array, position - 1);
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

    printf("Array in reverse order: ");
    display_in_reverse(array, size - 1);
    printf("\n");

    return 0;
}
