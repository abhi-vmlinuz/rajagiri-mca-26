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

int main(void)
{
    Polynomial polynomial;

    read_polynomial(&polynomial);

    if (polynomial.count > 0)
    {
        printf("Polynomial: ");
        display_polynomial(polynomial);
    }

    return 0;
}
