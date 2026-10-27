#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME 50

typedef struct StackNode
{
    int data;
    struct StackNode *next;
} StackNode;

typedef struct QueueNode
{
    int data;
    struct QueueNode *next;
} QueueNode;

typedef struct CircularNode
{
    int data;
    struct CircularNode *next;
} CircularNode;

typedef struct CircularQueueNode
{
    int data;
    struct CircularQueueNode *next;
} CircularQueueNode;

typedef struct DoubleNode
{
    int data;
    struct DoubleNode *prev;
    struct DoubleNode *next;
} DoubleNode;

typedef struct CircularDoubleNode
{
    char name[MAX_NAME];
    struct CircularDoubleNode *prev;
    struct CircularDoubleNode *next;
} CircularDoubleNode;

void stack_push(StackNode **top, int value)
{
    StackNode *node = malloc(sizeof(StackNode));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    node->data = value;
    node->next = *top;
    *top = node;
}

int stack_pop(StackNode **top)
{
    StackNode *temporary;
    int value;

    if (*top == NULL)
    {
        printf("Stack is empty.\n");
        return -1;
    }

    temporary = *top;
    value = temporary->data;
    *top = temporary->next;
    free(temporary);

    return value;
}

void stack_display(StackNode *top)
{
    StackNode *current = top;

    printf("Stack: ");

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
}

void stack_free(StackNode *top)
{
    StackNode *current = top;
    StackNode *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

void demo_linked_stack(void)
{
    StackNode *top = NULL;

    stack_push(&top, 10);
    stack_push(&top, 20);
    stack_push(&top, 30);

    stack_display(top);

    printf("Popped: %d\n", stack_pop(&top));
    stack_display(top);

    stack_free(top);
}

void queue_enqueue(QueueNode **front, QueueNode **rear, int value)
{
    QueueNode *node = malloc(sizeof(QueueNode));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    node->data = value;
    node->next = NULL;

    if (*rear == NULL)
    {
        *front = node;
        *rear = node;
    }
    else
    {
        (*rear)->next = node;
        *rear = node;
    }
}

int queue_dequeue(QueueNode **front, QueueNode **rear)
{
    QueueNode *temporary;
    int value;

    if (*front == NULL)
    {
        printf("Queue is empty.\n");
        return -1;
    }

    temporary = *front;
    value = temporary->data;
    *front = temporary->next;

    if (*front == NULL)
    {
        *rear = NULL;
    }

    free(temporary);

    return value;
}

void queue_display(QueueNode *front)
{
    QueueNode *current = front;

    printf("Queue: ");

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
}

void queue_free(QueueNode *front)
{
    QueueNode *current = front;
    QueueNode *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

void demo_linked_queue(void)
{
    QueueNode *front = NULL;
    QueueNode *rear = NULL;

    queue_enqueue(&front, &rear, 10);
    queue_enqueue(&front, &rear, 20);
    queue_enqueue(&front, &rear, 30);

    queue_display(front);

    printf("Dequeued: %d\n", queue_dequeue(&front, &rear));
    queue_display(front);

    queue_enqueue(&front, &rear, 40);
    queue_display(front);

    queue_free(front);
}

void circular_insert_end(CircularNode **head, int value)
{
    CircularNode *node = malloc(sizeof(CircularNode));
    CircularNode *current;

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    node->data = value;
    node->next = node;

    if (*head == NULL)
    {
        *head = node;
        return;
    }

    current = *head;

    while (current->next != *head)
    {
        current = current->next;
    }

    current->next = node;
    node->next = *head;
}

void circular_display(CircularNode *head)
{
    CircularNode *current;

    if (head == NULL)
    {
        printf("Circular list is empty.\n");
        return;
    }

    printf("Circular list: ");
    current = head;

    do
    {
        printf("%d ", current->data);
        current = current->next;
    } while (current != head);

    printf("\n");
}

void circular_delete(CircularNode **head, int value)
{
    CircularNode *current = *head;
    CircularNode *previous = NULL;

    if (*head == NULL)
    {
        printf("Circular list is empty.\n");
        return;
    }

    do
    {
        if (current->data == value)
        {
            break;
        }

        previous = current;
        current = current->next;
    } while (current != *head);

    if (current->data != value)
    {
        printf("%d not found.\n", value);
        return;
    }

    if (current->next == current)
    {
        *head = NULL;
    }
    else
    {
        if (previous == NULL)
        {
            previous = *head;

            while (previous->next != *head)
            {
                previous = previous->next;
            }

            *head = current->next;
        }

        previous->next = current->next;
    }

    free(current);
}

void circular_free(CircularNode *head)
{
    CircularNode *current;
    CircularNode *next;

    if (head == NULL)
    {
        return;
    }

    current = head;

    do
    {
        next = current->next;
        free(current);
        current = next;
    } while (current != head);
}

void demo_circular_linked_list(void)
{
    CircularNode *head = NULL;

    circular_insert_end(&head, 10);
    circular_insert_end(&head, 20);
    circular_insert_end(&head, 30);

    circular_display(head);

    circular_delete(&head, 20);
    circular_display(head);

    circular_free(head);
}

void circular_queue_enqueue(CircularQueueNode **rear, int value)
{
    CircularQueueNode *node = malloc(sizeof(CircularQueueNode));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    node->data = value;
    node->next = node;

    if (*rear == NULL)
    {
        *rear = node;
        return;
    }

    node->next = (*rear)->next;
    (*rear)->next = node;
    *rear = node;
}

int circular_queue_dequeue(CircularQueueNode **rear)
{
    CircularQueueNode *front;
    int value;

    if (*rear == NULL)
    {
        printf("Circular queue is empty.\n");
        return -1;
    }

    front = (*rear)->next;
    value = front->data;

    if (front == *rear)
    {
        *rear = NULL;
    }
    else
    {
        (*rear)->next = front->next;
    }

    free(front);

    return value;
}

void circular_queue_display(CircularQueueNode *rear)
{
    CircularQueueNode *front;
    CircularQueueNode *current;

    if (rear == NULL)
    {
        printf("Circular queue is empty.\n");
        return;
    }

    printf("Circular queue: ");
    front = rear->next;
    current = front;

    do
    {
        printf("%d ", current->data);
        current = current->next;
    } while (current != front);

    printf("\n");
}

void demo_circular_linked_queue(void)
{
    CircularQueueNode *rear = NULL;

    circular_queue_enqueue(&rear, 10);
    circular_queue_enqueue(&rear, 20);
    circular_queue_enqueue(&rear, 30);

    circular_queue_display(rear);

    printf("Dequeued: %d\n", circular_queue_dequeue(&rear));
    circular_queue_display(rear);

    circular_queue_enqueue(&rear, 40);
    circular_queue_display(rear);

    while (rear != NULL)
    {
        circular_queue_dequeue(&rear);
    }
}

void double_insert_end(DoubleNode **head, int value)
{
    DoubleNode *node = malloc(sizeof(DoubleNode));
    DoubleNode *current;

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    node->data = value;
    node->prev = NULL;
    node->next = NULL;

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
    node->prev = current;
}

void double_display_forward(DoubleNode *head)
{
    DoubleNode *current = head;

    printf("Forward: ");

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
}

void double_display_backward(DoubleNode *head)
{
    DoubleNode *current = head;

    if (current == NULL)
    {
        printf("Backward: empty\n");
        return;
    }

    while (current->next != NULL)
    {
        current = current->next;
    }

    printf("Backward: ");

    while (current != NULL)
    {
        printf("%d ", current->data);
        current = current->prev;
    }

    printf("\n");
}

void double_delete(DoubleNode **head, int value)
{
    DoubleNode *current = *head;

    while (current != NULL && current->data != value)
    {
        current = current->next;
    }

    if (current == NULL)
    {
        printf("%d not found.\n", value);
        return;
    }

    if (current->prev != NULL)
    {
        current->prev->next = current->next;
    }
    else
    {
        *head = current->next;
    }

    if (current->next != NULL)
    {
        current->next->prev = current->prev;
    }

    free(current);
}

void double_free(DoubleNode *head)
{
    DoubleNode *current = head;
    DoubleNode *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

void demo_doubly_linked_list(void)
{
    DoubleNode *head = NULL;

    double_insert_end(&head, 10);
    double_insert_end(&head, 20);
    double_insert_end(&head, 30);

    double_display_forward(head);
    double_display_backward(head);

    double_delete(&head, 20);

    double_display_forward(head);
    double_display_backward(head);

    double_free(head);
}

void circular_double_insert_end(CircularDoubleNode **head, const char *name)
{
    CircularDoubleNode *node = malloc(sizeof(CircularDoubleNode));
    CircularDoubleNode *tail;

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return;
    }

    strcpy(node->name, name);

    if (*head == NULL)
    {
        node->next = node;
        node->prev = node;
        *head = node;
        return;
    }

    tail = (*head)->prev;
    node->next = *head;
    node->prev = tail;
    tail->next = node;
    (*head)->prev = node;
}

void circular_double_display_forward(CircularDoubleNode *head)
{
    CircularDoubleNode *current;

    if (head == NULL)
    {
        printf("Circular double list is empty.\n");
        return;
    }

    printf("Forward: ");
    current = head;

    do
    {
        printf("%s ", current->name);
        current = current->next;
    } while (current != head);

    printf("\n");
}

void circular_double_display_backward(CircularDoubleNode *head)
{
    CircularDoubleNode *tail;
    CircularDoubleNode *current;

    if (head == NULL)
    {
        printf("Circular double list is empty.\n");
        return;
    }

    printf("Backward: ");
    tail = head->prev;
    current = tail;

    do
    {
        printf("%s ", current->name);
        current = current->prev;
    } while (current != tail);

    printf("\n");
}

void circular_double_delete(CircularDoubleNode **head, const char *name)
{
    CircularDoubleNode *current = *head;

    if (*head == NULL)
    {
        printf("Circular double list is empty.\n");
        return;
    }

    do
    {
        if (strcmp(current->name, name) == 0)
        {
            break;
        }

        current = current->next;
    } while (current != *head);

    if (strcmp(current->name, name) != 0)
    {
        printf("%s not found.\n", name);
        return;
    }

    if (current->next == current)
    {
        *head = NULL;
    }
    else
    {
        current->prev->next = current->next;
        current->next->prev = current->prev;

        if (current == *head)
        {
            *head = current->next;
        }
    }

    free(current);
}

void circular_double_free(CircularDoubleNode *head)
{
    CircularDoubleNode *current;
    CircularDoubleNode *next;

    if (head == NULL)
    {
        return;
    }

    current = head;

    do
    {
        next = current->next;
        free(current);
        current = next;
    } while (current != head);
}

void demo_circular_doubly_linked_list(void)
{
    CircularDoubleNode *head = NULL;

    circular_double_insert_end(&head, "Alice");
    circular_double_insert_end(&head, "Bob");
    circular_double_insert_end(&head, "Carol");

    circular_double_display_forward(head);
    circular_double_display_backward(head);

    circular_double_delete(&head, "Bob");

    circular_double_display_forward(head);
    circular_double_display_backward(head);

    circular_double_free(head);
}

int main(void)
{
    printf("Linked Stack\n");
    demo_linked_stack();

    printf("\nLinked Queue\n");
    demo_linked_queue();

    printf("\nCircular Linked List\n");
    demo_circular_linked_list();

    printf("\nCircular Linked Queue\n");
    demo_circular_linked_queue();

    printf("\nDoubly Linked List\n");
    demo_doubly_linked_list();

    printf("\nCircular Doubly Linked List\n");
    demo_circular_doubly_linked_list();

    return 0;
}
