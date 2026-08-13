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

void display_occurrences(int array[], int size, int value)
{
    int i;
    int found = 0;

    printf("Positions of %d: ", value);
    for (i = 0; i < size; i++)
    {
        if (array[i] == value)
        {
            printf("%d ", i + 1);
            found = 1;
        }
    }

    if (found == 0)
    {
        printf("Element not found");
    }
    printf("\n");
}

int main(void)
{
    int array[MAX];
    int size;
    int value;

    printf("Enter the size of the array (maximum %d): ", MAX);
    scanf("%d", &size);

    if (size < 1 || size > MAX)
    {
        printf("Invalid size.\n");
        return 0;
    }

    read_array(array, size);
    printf("Enter the element to search: ");
    scanf("%d", &value);
    display_occurrences(array, size, value);

    return 0;
}
