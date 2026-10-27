#include <stdio.h>

#define MAX_LENGTH 100

char stack[MAX_LENGTH];
int top = -1;

void push(char value)
{
    top++;
    stack[top] = value;
}

char pop(void)
{
    char value = stack[top];

    top--;
    return value;
}

int main(void)
{
    char text[MAX_LENGTH];
    int i = 0;

    printf("Enter a string: ");
    scanf(" %99[^\n]", text);

    while (text[i] != '\0')
    {
        push(text[i]);
        i++;
    }

    printf("String in reverse order: ");
    while (top != -1)
    {
        printf("%c", pop());
    }
    printf("\n");

    return 0;
}
