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

void delete_beginning(Node **head)
{
    Node *temporary;

    if (*head == NULL)
    {
        printf("List is empty.\n");
        return;
    }

    temporary = *head;
    *head = (*head)->next;
    free(temporary);
}

void delete_end(Node **head)
{
    Node *current;
    Node *previous;

    if (*head == NULL)
    {
        printf("List is empty.\n");
        return;
    }

    if ((*head)->next == NULL)
    {
        free(*head);
        *head = NULL;
        return;
    }

    current = *head;
    previous = NULL;

    while (current->next != NULL)
    {
        previous = current;
        current = current->next;
    }

    previous->next = NULL;
    free(current);
}

void delete_value(Node **head, int value)
{
    Node *current = *head;
    Node *previous = NULL;

    while (current != NULL && current->data != value)
    {
        previous = current;
        current = current->next;
    }

    if (current == NULL)
    {
        printf("Element %d not found.\n", value);
        return;
    }

    if (previous == NULL)
    {
        *head = current->next;
    }
    else
    {
        previous->next = current->next;
    }

    free(current);
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

    insert_end(&head, 10);
    insert_end(&head, 20);
    insert_end(&head, 30);
    insert_end(&head, 40);

    delete_beginning(&head);
    delete_end(&head);
    delete_value(&head, 20);

    display(head);

    free_list(head);

    return 0;
}
