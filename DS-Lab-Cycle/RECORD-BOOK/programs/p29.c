#include <stdio.h>

#define MAX 5

int queue[MAX];
int front = 0;
int rear = -1;

void enqueue(int value)
{
    if (rear == MAX - 1)
    {
        printf("Queue is full.\n");
        return;
    }

    rear++;
    queue[rear] = value;
}

int dequeue(void)
{
    int value;

    if (front > rear)
    {
        printf("Queue is empty.\n");
        return -1;
    }

    value = queue[front];
    front++;

    return value;
}

void display(void)
{
    int i;

    if (front > rear)
    {
        printf("Queue is empty.\n");
        return;
    }

    printf("Queue: ");

    for (i = front; i <= rear; i++)
    {
        printf("%d ", queue[i]);
    }

    printf("\n");
}

int main(void)
{
    enqueue(10);
    enqueue(20);
    enqueue(30);

    display();

    printf("Dequeued: %d\n", dequeue());
    display();

    enqueue(40);
    display();

    return 0;
}
