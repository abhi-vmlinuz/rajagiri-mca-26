#include <stdio.h>

#define MAX 100

int stack[MAX];
int top = -1;

void push(int value)
{
    stack[++top] = value;
}

int pop()
{
  return stack[top--];
}

int main()
{
    int n;

    printf("Enter a decimal number: ");
    scanf("%d", &n);
    while(n > 0)
    {
    	push(n % 2);
    	n = n / 2;
    }

    printf("Binary Equivalent: ");
    while(top != -1)
{
    printf("%d", pop());
}
printf("\n");

return 0;
}
