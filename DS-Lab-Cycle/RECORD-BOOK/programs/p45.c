#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int data;
    struct Node *next;
} Node;

Node *create_node(int value)
{
    Node *node = malloc(sizeof(Node));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    node->data = value;
    node->next = NULL;

    return node;
}

void insert_end(Node **head, int value)
{
    Node *node = create_node(value);
    Node *current;

    if (node == NULL)
    {
        return;
    }

    if (*head == NULL)
    {
        *head = node;
        return;
    }

    current = *head;

    while (current->next != NULL)
    {
        current = current->next;
    }

    current->next = node;
}

void display(Node *head)
{
    Node *current = head;

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
}

void sort_by_value(Node *head)
{
    Node *current;
    Node *next;
    int temporary;
    int swapped;

    do
    {
        swapped = 0;
        current = head;

        while (current != NULL && current->next != NULL)
        {
            next = current->next;

            if (current->data > next->data)
            {
                temporary = current->data;
                current->data = next->data;
                next->data = temporary;
                swapped = 1;
            }

            current = current->next;
        }
    } while (swapped == 1);
}

void sort_by_address(Node **head)
{
    Node **current;
    Node *first;
    Node *second;
    int swapped;

    do
    {
        swapped = 0;
        current = head;

        while (*current != NULL && (*current)->next != NULL)
        {
            first = *current;
            second = first->next;

            if (first->data > second->data)
            {
                first->next = second->next;
                second->next = first;
                *current = second;
                swapped = 1;
            }

            current = &(*current)->next;
        }
    } while (swapped == 1);
}

void free_list(Node *head)
{
    Node *current = head;
    Node *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

int main(void)
{
    Node *first = NULL;
    Node *second = NULL;

    insert_end(&first, 30);
    insert_end(&first, 10);
    insert_end(&first, 40);
    insert_end(&first, 20);

    printf("Before sorting: ");
    display(first);

    sort_by_value(first);

    printf("Sorted by changing values: ");
    display(first);

    insert_end(&second, 30);
    insert_end(&second, 10);
    insert_end(&second, 40);
    insert_end(&second, 20);

    sort_by_address(&second);

    printf("Sorted by changing addresses: ");
    display(second);

    free_list(first);
    free_list(second);

    return 0;
}
