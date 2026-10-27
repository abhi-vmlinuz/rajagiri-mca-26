#include <stdio.h>

#define MAX 100

typedef struct
{
    int value;
    int priority;
} Item;

Item queue[MAX];
int count = 0;

void insert(int value, int priority)
{
    if (count == MAX)
    {
        printf("Priority queue is full.\n");
        return;
    }

    queue[count].value = value;
    queue[count].priority = priority;
    count++;
}

int delete_highest(void)
{
    int i;
    int highest = 0;
    int value;

    if (count == 0)
    {
        printf("Priority queue is empty.\n");
        return -1;
    }

    for (i = 1; i < count; i++)
    {
        if (queue[i].priority > queue[highest].priority)
        {
            highest = i;
        }
    }

    value = queue[highest].value;

    for (i = highest; i < count - 1; i++)
    {
        queue[i] = queue[i + 1];
    }

    count--;

    return value;
}

void display(void)
{
    int i;

    printf("%-8s %-8s\n", "Value", "Priority");

    for (i = 0; i < count; i++)
    {
        printf("%-8d %-8d\n", queue[i].value, queue[i].priority);
    }
}

int main(void)
{
    insert(10, 2);
    insert(20, 5);
    insert(30, 1);
    insert(40, 4);

    printf("Priority queue:\n");
    display();

    printf("Deleted: %d\n", delete_highest());
    display();

    printf("Deleted: %d\n", delete_highest());
    display();

    return 0;
}
