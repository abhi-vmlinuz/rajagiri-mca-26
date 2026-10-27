#include <stdio.h>

#define MAX 30

char stack[MAX];
int top = -1;

void push(char value)
{
    top++;
    stack[top] = value;
}

char pop()
{
    char value = stack[top];

    top--;
    return value;
}

int main()
{
    char operations[] = "EAS*Y*QUE***ST***IO*N***";
    int i = 0;

    printf("Values returned by pop operations: ");

    while (operations[i] != '\0')
    {
        if (operations[i] == '*')
        {
            printf("%c ", pop());
        }
        else
        {
            push(operations[i]);
        }
        i++;
    }

    printf("\n");
    return 0;
}
