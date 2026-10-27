#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 50

typedef struct Node
{
    char name[MAX_NAME];
    struct Node *next;
} Node;

Node *create_node(const char *name)
{
    Node *node = malloc(sizeof(Node));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    strcpy(node->name, name);
    node->next = NULL;

    return node;
}

void insert_end(Node **head, const char *name)
{
    Node *node = create_node(name);
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

void delete_name(Node **head, const char *name)
{
    Node *current = *head;
    Node *previous = NULL;

    while (current != NULL && strcmp(current->name, name) != 0)
    {
        previous = current;
        current = current->next;
    }

    if (current == NULL)
    {
        printf("%s not found.\n", name);
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

    printf("List: ");

    while (current != NULL)
    {
        printf("%s ", current->name);
        current = current->next;
    }

    printf("\n");
}

void sort(Node *head)
{
    Node *current;
    Node *next;
    char temporary[MAX_NAME];
    int swapped;

    do
    {
        swapped = 0;
        current = head;

        while (current != NULL && current->next != NULL)
        {
            next = current->next;

            if (strcmp(current->name, next->name) > 0)
            {
                strcpy(temporary, current->name);
                strcpy(current->name, next->name);
                strcpy(next->name, temporary);
                swapped = 1;
            }

            current = current->next;
        }
    } while (swapped == 1);
}

void reverse(Node **head)
{
    Node *previous = NULL;
    Node *current = *head;
    Node *next;

    while (current != NULL)
    {
        next = current->next;
        current->next = previous;
        previous = current;
        current = next;
    }

    *head = previous;
}

int count_nodes(Node *head)
{
    int count = 0;
    Node *current = head;

    while (current != NULL)
    {
        count++;
        current = current->next;
    }

    return count;
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

    insert_end(&head, "Alice");
    insert_end(&head, "Bob");
    insert_end(&head, "Carol");
    insert_end(&head, "Dave");

    display(head);
    printf("Count: %d\n", count_nodes(head));

    delete_name(&head, "Bob");
    display(head);

    sort(head);
    printf("After sorting: ");
    display(head);

    reverse(&head);
    printf("After reversing: ");
    display(head);

    free_list(head);

    return 0;
}
