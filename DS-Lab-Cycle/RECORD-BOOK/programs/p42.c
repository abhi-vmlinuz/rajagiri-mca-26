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

void insert_beginning(Node **head, int value)
{
    Node *node = create_node(value);

    if (node == NULL)
    {
        return;
    }

    node->next = *head;
    *head = node;
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

void insert_after(Node *head, int target, int value)
{
    Node *current = head;
    Node *node;

    while (current != NULL && current->data != target)
    {
        current = current->next;
    }

    if (current == NULL)
    {
        printf("Element %d not found.\n", target);
        return;
    }

    node = create_node(value);

    if (node == NULL)
    {
        return;
    }

    node->next = current->next;
    current->next = node;
}

void display(Node *head)
{
    Node *current = head;

    printf("Linked list: ");

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
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
    Node *head = NULL;

    insert_end(&head, 20);
    insert_end(&head, 30);
    insert_beginning(&head, 10);
    insert_after(head, 20, 25);
    insert_after(head, 30, 35);

    display(head);

    free_list(head);

    return 0;
}
