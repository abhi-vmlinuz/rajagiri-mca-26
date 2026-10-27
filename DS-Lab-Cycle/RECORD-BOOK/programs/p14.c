#include <stdio.h>

#define MAX_LENGTH 100

char stack[MAX_LENGTH];
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

char peek()
{
    return stack[top];
}

int is_operand(char symbol)
{
    if (symbol >= 'A' && symbol <= 'Z')
    {
        return 1;
    }
    if (symbol >= 'a' && symbol <= 'z')
    {
        return 1;
    }
    if (symbol >= '0' && symbol <= '9')
    {
        return 1;
    }
    return 0;
}

int is_operator(char symbol)
{
    if (symbol == '+' || symbol == '-' || symbol == '*' ||
        symbol == '/' || symbol == '%' || symbol == '^')
    {
        return 1;
    }
    return 0;
}

int precedence(char symbol)
{
    if (symbol == '+' || symbol == '-')
    {
        return 1;
    }
    if (symbol == '*' || symbol == '/' || symbol == '%')
    {
        return 2;
    }
    if (symbol == '^')
    {
        return 3;
    }
    return 0;
}

int should_pop(char stack_symbol, char current_symbol)
{
    if (precedence(stack_symbol) > precedence(current_symbol))
    {
        return 1;
    }

    if (precedence(stack_symbol) == precedence(current_symbol) &&
        current_symbol != '^')
    {
        return 1;
    }

    return 0;
}

int main()
{
    char infix[MAX_LENGTH];
    char postfix[MAX_LENGTH];
    int i = 0;
    int output_position = 0;
    int expect_operand = 1;
    int valid = 1;
    char symbol;

    printf("Enter an infix expression without spaces: ");
    scanf("%99s", infix);

    while (infix[i] != '\0' && valid == 1)
    {
        symbol = infix[i];

        if (is_operand(symbol))
        {
            if (expect_operand == 0)
            {
                valid = 0;
            }
            else if (symbol >= '0' && symbol <= '9' &&
                     infix[i + 1] >= '0' && infix[i + 1] <= '9')
            {
                valid = 0;
            }
            else
            {
                postfix[output_position] = symbol;
                output_position++;
                expect_operand = 0;
                i++;
            }
        }
        else if (symbol == '(')
        {
            if (expect_operand == 0)
            {
                valid = 0;
            }
            else
            {
                push(symbol);
                i++;
            }
        }
        else if (symbol == ')')
        {
            if (expect_operand == 1)
            {
                valid = 0;
            }
            else
            {
                while (top != -1 && peek() != '(')
                {
                    postfix[output_position] = pop();
                    output_position++;
                }

                if (top == -1)
                {
                    valid = 0;
                }
                else
                {
                    pop();
                    expect_operand = 0;
                    i++;
                }
            }
        }
        else if (is_operator(symbol))
        {
            if (expect_operand == 1)
            {
                valid = 0;
            }
            else
            {
                while (top != -1 && peek() != '(' &&
                       should_pop(peek(), symbol) == 1)
                {
                    postfix[output_position] = pop();
                    output_position++;
                }

                push(symbol);
                expect_operand = 1;
                i++;
            }
        }
        else
        {
            valid = 0;
        }
    }

    if (expect_operand == 1)
    {
        valid = 0;
    }

    while (top != -1 && valid == 1)
    {
        if (peek() == '(')
        {
            valid = 0;
        }
        else
        {
            postfix[output_position] = pop();
            output_position++;
        }
    }

    if (valid == 1)
    {
        postfix[output_position] = '\0';
        printf("Postfix expression: %s\n", postfix);
    }
    else
    {
        printf("Invalid expression. Use single-character operands.\n");
    }

    return 0;
}
