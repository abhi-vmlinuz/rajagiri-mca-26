#include <stdio.h>

#define MAX 5

int queue[MAX];
int front = 0;
int rear = -1;
int count = 0;

void enqueue(int value)
{
    if (count == MAX)
    {
        printf("Queue is full.\n");
        return;
    }

    rear = (rear + 1) % MAX;
    queue[rear] = value;
    count++;
}

int dequeue(void)
{
    int value;

    if (count == 0)
    {
        printf("Queue is empty.\n");
        return -1;
    }

    value = queue[front];
    front = (front + 1) % MAX;
    count--;

    return value;
}

void display(void)
{
    int i;

    if (count == 0)
    {
        printf("Queue is empty.\n");
        return;
    }

    printf("Queue: ");

    for (i = 0; i < count; i++)
    {
        printf("%d ", queue[(front + i) % MAX]);
    }

    printf("\n");
}

int main(void)
{
    enqueue(10);
    enqueue(20);
    enqueue(30);
    enqueue(40);

    display();

    printf("Dequeued: %d\n", dequeue());
    printf("Dequeued: %d\n", dequeue());

    enqueue(50);
    enqueue(60);

    display();

    return 0;
}
