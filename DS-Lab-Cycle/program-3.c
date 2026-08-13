#include <stdio.h>

#define MAX 100

void display(int array[], int size)
{
    int i;

    if (size == 0)
    {
        printf("Array is empty.\n");
        return;
    }

    printf("Array: ");
    for (i = 0; i < size; i++)
    {
        printf("%d ", array[i]);
    }
    printf("\n");
}

int insert_element(int array[], int size)
{
    int value;
    int position;
    int i;

    if (size == MAX)
    {
        printf("Array is full.\n");
        return size;
    }

    printf("Enter the value to insert: ");
    scanf("%d", &value);
    printf("Enter the position (1 to %d): ", size + 1);
    scanf("%d", &position);

    if (position < 1 || position > size + 1)
    {
        printf("Invalid position.\n");
        return size;
    }

    for (i = size; i >= position; i--)
    {
        array[i] = array[i - 1];
    }

    array[position - 1] = value;
    printf("Element inserted.\n");
    return size + 1;
}

void search_element(int array[], int size)
{
    int value;
    int i;

    printf("Enter the value to search: ");
    scanf("%d", &value);

    for (i = 0; i < size; i++)
    {
        if (array[i] == value)
        {
            printf("Element found at position %d.\n", i + 1);
            return;
        }
    }

    printf("Element not found.\n");
}

int delete_element(int array[], int size)
{
    int value;
    int position = -1;
    int i;

    if (size == 0)
    {
        printf("Array is empty.\n");
        return size;
    }

    printf("Enter the value to delete: ");
    scanf("%d", &value);

    for (i = 0; i < size; i++)
    {
        if (array[i] == value)
        {
            position = i;
            break;
        }
    }

    if (position == -1)
    {
        printf("Element not found.\n");
        return size;
    }

    for (i = position; i < size - 1; i++)
    {
        array[i] = array[i + 1];
    }

    printf("First occurrence deleted.\n");
    return size - 1;
}

void sort_elements(int array[], int size)
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

    printf("Array sorted in ascending order.\n");
}

int main(void)
{
    int array[MAX];
    int size = 0;
    int choice;

    do
    {
        printf("\n1. Insert\n");
        printf("2. Display\n");
        printf("3. Search\n");
        printf("4. Delete\n");
        printf("5. Sort\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
            case 1:
                size = insert_element(array, size);
                break;
            case 2:
                display(array, size);
                break;
            case 3:
                search_element(array, size);
                break;
            case 4:
                size = delete_element(array, size);
                break;
            case 5:
                sort_elements(array, size);
                break;
            case 6:
                printf("Program ended.\n");
                break;
            default:
                printf("Invalid choice.\n");
        }
    } while (choice != 6);

    return 0;
}
