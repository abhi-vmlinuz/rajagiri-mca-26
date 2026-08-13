#include <stdio.h>

#define MAX 100

/* These are global variables, as required by question 2. */
int array[MAX];
int size = 0;

void display()
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

void insert_element()
{
    int value;
    int position;
    int i;

    if (size == MAX)
    {
        printf("Array is full.\n");
        return;
    }

    printf("Enter the value to insert: ");
    scanf("%d", &value);
    printf("Enter the position (1 to %d): ", size + 1);
    scanf("%d", &position);

    if (position < 1 || position > size + 1)
    {
        printf("Invalid position.\n");
        return;
    }

    for (i = size; i >= position; i--)
    {
        array[i] = array[i - 1];
    }

    array[position - 1] = value;
    size++;
    printf("Element inserted.\n");
}

void search_element()
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

void delete_element()
{
    int value;
    int position = -1;
    int i;

    if (size == 0)
    {
        printf("Array is empty.\n");
        return;
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
        return;
    }

    for (i = position; i < size - 1; i++)
    {
        array[i] = array[i + 1];
    }

    size--;
    printf("First occurrence deleted.\n");
}

void sort_elements()
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

int main()
{
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
                insert_element();
                break;
            case 2:
                display();
                break;
            case 3:
                search_element();
                break;
            case 4:
                delete_element();
                break;
            case 5:
                sort_elements();
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

