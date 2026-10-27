#include <stdio.h>

#define MAX_TERMS 50

typedef struct
{
    int coefficient;
    int exponent;
} Term;

typedef struct
{
    Term terms[MAX_TERMS];
    int count;
} Polynomial;

void sort_terms(Polynomial *polynomial)
{
    int i;
    int j;
    Term temporary;

    for (i = 0; i < polynomial->count - 1; i++)
    {
        for (j = 0; j < polynomial->count - i - 1; j++)
        {
            if (polynomial->terms[j].exponent < polynomial->terms[j + 1].exponent)
            {
                temporary = polynomial->terms[j];
                polynomial->terms[j] = polynomial->terms[j + 1];
                polynomial->terms[j + 1] = temporary;
            }
        }
    }
}

void read_polynomial(Polynomial *polynomial)
{
    int i;

    printf("Enter the number of terms: ");
    scanf("%d", &polynomial->count);

    if (polynomial->count < 1 || polynomial->count > MAX_TERMS)
    {
        printf("Invalid number of terms.\n");
        polynomial->count = 0;
        return;
    }

    for (i = 0; i < polynomial->count; i++)
    {
        printf("Term %d coefficient: ", i + 1);
        scanf("%d", &polynomial->terms[i].coefficient);
        printf("Term %d exponent: ", i + 1);
        scanf("%d", &polynomial->terms[i].exponent);
    }

    sort_terms(polynomial);
}

void display_polynomial(Polynomial polynomial)
{
    int i;
    int printed = 0;

    for (i = 0; i < polynomial.count; i++)
    {
        int coefficient = polynomial.terms[i].coefficient;
        int exponent = polynomial.terms[i].exponent;

        if (coefficient == 0)
        {
            continue;
        }

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

    if (printed == 0)
    {
        printf("0");
    }

    printf("\n");
}

void combine_terms(Polynomial *polynomial)
{
    int i;
    int j;
    int k;

    sort_terms(polynomial);

    for (i = 0; i < polynomial->count; i++)
    {
        j = i + 1;

        while (j < polynomial->count)
        {
            if (polynomial->terms[i].exponent == polynomial->terms[j].exponent)
            {
                polynomial->terms[i].coefficient += polynomial->terms[j].coefficient;

                for (k = j; k < polynomial->count - 1; k++)
                {
                    polynomial->terms[k] = polynomial->terms[k + 1];
                }

                polynomial->count--;
            }
            else
            {
                j++;
            }
        }
    }

    i = 0;

    while (i < polynomial->count)
    {
        if (polynomial->terms[i].coefficient == 0)
        {
            for (k = i; k < polynomial->count - 1; k++)
            {
                polynomial->terms[k] = polynomial->terms[k + 1];
            }

            polynomial->count--;
        }
        else
        {
            i++;
        }
    }
}

void subtract_polynomials(Polynomial first, Polynomial second, Polynomial *result)
{
    int i;

    result->count = 0;

    for (i = 0; i < first.count; i++)
    {
        result->terms[result->count] = first.terms[i];
        result->count++;
    }

    for (i = 0; i < second.count; i++)
    {
        result->terms[result->count] = second.terms[i];
        result->terms[result->count].coefficient = -second.terms[i].coefficient;
        result->count++;
    }

    combine_terms(result);
}

int main(void)
{
    Polynomial first;
    Polynomial second;
    Polynomial result;

    printf("First polynomial:\n");
    read_polynomial(&first);

    printf("Second polynomial:\n");
    read_polynomial(&second);

    if (first.count == 0 || second.count == 0)
    {
        return 0;
    }

    subtract_polynomials(first, second, &result);

    printf("First polynomial: ");
    display_polynomial(first);

    printf("Second polynomial: ");
    display_polynomial(second);

    printf("Difference: ");
    display_polynomial(result);

    return 0;
}
