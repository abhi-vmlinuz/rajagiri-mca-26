#include <stdio.h>

#define MAX 100

int array[MAX];
int size = 0;

void read_element(void)
{
    printf("Enter element %d: ", size + 1);
    scanf("%d", &array[size]);
    size++;
}

void display_array(void)
{
    int i;

    printf("Array: ");

    for (i = 0; i < size; i++)
    {
        printf("%d ", array[i]);
    }

    printf("\n");
}

void sort_array(void)
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

int main(void)
{
    read_element();
    read_element();
    read_element();
    read_element();

    printf("Before sorting:\n");
    display_array();

    sort_array();

    printf("After sorting:\n");
    display_array();

    return 0;
}
