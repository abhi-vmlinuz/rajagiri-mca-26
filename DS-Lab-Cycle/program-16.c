#include <stdio.h>

#define MAX_LENGTH 100

int value_stack[MAX_LENGTH];
char operator_stack[MAX_LENGTH];
int value_top = -1;
int operator_top = -1;
int error = 0;

void push_value(int value)
{
    value_top++;
    value_stack[value_top] = value;
}

int pop_value(void)
{
    int value = value_stack[value_top];

    value_top--;
    return value;
}

void push_operator(char symbol)
{
    operator_top++;
    operator_stack[operator_top] = symbol;
}

char pop_operator(void)
{
    char symbol = operator_stack[operator_top];

    operator_top--;
    return symbol;
}

char peek_operator(void)
{
    return operator_stack[operator_top];
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

int power(int base, int exponent)
{
    int result = 1;
    int i;

    for (i = 0; i < exponent; i++)
    {
        result = result * base;
    }
    return result;
}

void apply_operator(void)
{
    int left;
    int right;
    int result;
    char symbol;

    if (value_top < 1 || operator_top == -1)
    {
        error = 1;
        return;
    }

    right = pop_value();
    left = pop_value();
    symbol = pop_operator();

    if (symbol == '+')
    {
        result = left + right;
    }
    else if (symbol == '-')
    {
        result = left - right;
    }
    else if (symbol == '*')
    {
        result = left * right;
    }
    else if (symbol == '^')
    {
        if (right < 0)
        {
            error = 1;
            return;
        }
        result = power(left, right);
    }
    else if (symbol == '/')
    {
        if (right == 0)
        {
            error = 1;
            return;
        }
        result = left / right;
    }
    else
    {
        if (right == 0)
        {
            error = 1;
            return;
        }
        result = left % right;
    }

    push_value(result);
}

int main(void)
{
    char expression[MAX_LENGTH];
    int i = 0;
    int number;
    int expect_operand = 1;
    int valid = 1;
    char symbol;

    printf("Enter an infix expression: ");
    scanf(" %99[^\n]", expression);

    while (expression[i] != '\0' && valid == 1 && error == 0)
    {
        symbol = expression[i];

        if (symbol == ' ')
        {
            i++;
        }
        else if (symbol >= '0' && symbol <= '9')
        {
            if (expect_operand == 0)
            {
                valid = 0;
            }
            else
            {
                number = 0;
                while (expression[i] >= '0' && expression[i] <= '9')
                {
                    number = number * 10 + expression[i] - '0';
                    i++;
                }
                push_value(number);
                expect_operand = 0;
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
                push_operator(symbol);
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
                while (operator_top != -1 &&
                       peek_operator() != '(' && error == 0)
                {
                    apply_operator();
                }

                if (operator_top == -1)
                {
                    valid = 0;
                }
                else
                {
                    pop_operator();
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
                while (operator_top != -1 &&
                       peek_operator() != '(' &&
                       should_pop(peek_operator(), symbol) == 1 &&
                       error == 0)
                {
                    apply_operator();
                }

                push_operator(symbol);
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

    while (operator_top != -1 && valid == 1 && error == 0)
    {
        if (peek_operator() == '(')
        {
            valid = 0;
        }
        else
        {
            apply_operator();
        }
    }

    if (valid == 1 && error == 0 && value_top == 0)
    {
        printf("Result = %d\n", pop_value());
    }
    else if (error == 1)
    {
        printf("Cannot evaluate the expression. Check the operands or division by zero.\n");
    }
    else
    {
        printf("Invalid expression.\n");
    }

    return 0;
}
