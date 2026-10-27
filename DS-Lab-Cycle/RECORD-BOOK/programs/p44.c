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

void display_reverse(Node *head)
{
    if (head == NULL)
    {
        return;
    }

    display_reverse(head->next);
    printf("%d ", head->data);
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
    int count;
    int value;
    int i;

    printf("Enter the number of nodes: ");
    scanf("%d", &count);

    if (count < 1)
    {
        printf("Invalid number of nodes.\n");
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        printf("Enter value %d: ", i + 1);
        scanf("%d", &value);
        insert_end(&head, value);
    }

    printf("List in original order: ");
    display(head);

    printf("List in reverse order: ");
    display_reverse(head);
    printf("\n");

    free_list(head);

    return 0;
}
