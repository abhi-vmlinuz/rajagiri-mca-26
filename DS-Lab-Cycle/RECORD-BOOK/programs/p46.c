#include <stdio.h>
#include <stdlib.h>

typedef struct Term
{
    int coefficient;
    int exponent;
    struct Term *next;
} Term;

Term *create_term(int coefficient, int exponent)
{
    Term *term = malloc(sizeof(Term));

    if (term == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    term->coefficient = coefficient;
    term->exponent = exponent;
    term->next = NULL;

    return term;
}

void insert_term(Term **head, int coefficient, int exponent)
{
    Term **current = head;
    Term *term;

    while (*current != NULL && (*current)->exponent > exponent)
    {
        current = &(*current)->next;
    }

    if (*current != NULL && (*current)->exponent == exponent)
    {
        (*current)->coefficient += coefficient;

        if ((*current)->coefficient == 0)
        {
            term = *current;
            *current = (*current)->next;
            free(term);
        }

        return;
    }

    term = create_term(coefficient, exponent);

    if (term == NULL)
    {
        return;
    }

    term->next = *current;
    *current = term;
}

Term *read_polynomial(void)
{
    Term *head = NULL;
    int count;
    int coefficient;
    int exponent;
    int i;

    printf("Enter the number of terms: ");
    scanf("%d", &count);

    for (i = 0; i < count; i++)
    {
        printf("Term %d coefficient: ", i + 1);
        scanf("%d", &coefficient);
        printf("Term %d exponent: ", i + 1);
        scanf("%d", &exponent);
        insert_term(&head, coefficient, exponent);
    }

    return head;
}

void display_polynomial(Term *head)
{
    Term *current = head;
    int printed = 0;

    while (current != NULL)
    {
        int coefficient = current->coefficient;
        int exponent = current->exponent;

        if (coefficient != 0)
        {
            if (printed == 1 && coefficient > 0)
            {
                printf(" + ");
            }
            else if (printed == 1 && coefficient < 0)
            {
                printf(" - ");
            }
            else if (coefficient < 0)
            {
                printf("-");
            }

            if (coefficient < 0)
            {
                coefficient = -coefficient;
            }

            if (exponent == 0)
            {
                printf("%d", coefficient);
            }
            else if (exponent == 1)
            {
                if (coefficient != 1)
                {
                    printf("%d", coefficient);
                }
                printf("x");
            }
            else
            {
                if (coefficient != 1)
                {
                    printf("%d", coefficient);
                }
                printf("x^%d", exponent);
            }

            printed = 1;
        }

        current = current->next;
    }

    if (printed == 0)
    {
        printf("0");
    }

    printf("\n");
}

Term *add_polynomials(Term *first, Term *second)
{
    Term *result = NULL;
    Term *current;

    for (current = first; current != NULL; current = current->next)
    {
        insert_term(&result, current->coefficient, current->exponent);
    }

    for (current = second; current != NULL; current = current->next)
    {
        insert_term(&result, current->coefficient, current->exponent);
    }

    return result;
}

Term *multiply_polynomials(Term *first, Term *second)
{
    Term *result = NULL;
    Term *left;
    Term *right;

    for (left = first; left != NULL; left = left->next)
    {
        for (right = second; right != NULL; right = right->next)
        {
            insert_term(&result,
                        left->coefficient * right->coefficient,
                        left->exponent + right->exponent);
        }
    }

    return result;
}

void free_polynomial(Term *head)
{
    Term *current = head;
    Term *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

int main(void)
{
    Term *first;
    Term *second;
    Term *sum;
    Term *product;

    printf("First polynomial:\n");
    first = read_polynomial();

    printf("Second polynomial:\n");
    second = read_polynomial();

    printf("First polynomial: ");
    display_polynomial(first);

    printf("Second polynomial: ");
    display_polynomial(second);

    sum = add_polynomials(first, second);
    printf("Sum: ");
    display_polynomial(sum);

    product = multiply_polynomials(first, second);
    printf("Product: ");
    display_polynomial(product);

    free_polynomial(first);
    free_polynomial(second);
    free_polynomial(sum);
    free_polynomial(product);

    return 0;
}
