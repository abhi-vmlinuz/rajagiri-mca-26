#include <stdio.h>

#define MAX_DEGREE 20

int read_polynomial(int coefficients[])
{
    int degree;
    int i;

    printf("Enter the degree of the polynomial: ");
    scanf("%d", &degree);

    if (degree < 0 || degree > MAX_DEGREE)
    {
        printf("Invalid degree.\n");
        return -1;
    }

    for (i = degree; i >= 0; i--)
    {
        printf("Enter the coefficient of x^%d: ", i);
        scanf("%d", &coefficients[i]);
    }

    return degree;
}

void display_polynomial(int coefficients[], int degree)
{
    int i;
    int printed = 0;

    for (i = degree; i >= 0; i--)
    {
        if (coefficients[i] == 0)
        {
            continue;
        }

        if (printed == 1 && coefficients[i] > 0)
        {
            printf(" + ");
        }
        else if (printed == 1 && coefficients[i] < 0)
        {
            printf(" - ");
        }
        else if (coefficients[i] < 0)
        {
            printf("-");
        }

        if (i == 0)
        {
            printf("%d", coefficients[i] < 0 ? -coefficients[i] : coefficients[i]);
        }
        else if (i == 1)
        {
            if (coefficients[i] == 1 || coefficients[i] == -1)
            {
                printf("x");
            }
            else
            {
                printf("%dx", coefficients[i] < 0 ? -coefficients[i] : coefficients[i]);
            }
        }
        else
        {
            if (coefficients[i] == 1 || coefficients[i] == -1)
            {
                printf("x^%d", i);
            }
            else
            {
                printf("%dx^%d", coefficients[i] < 0 ? -coefficients[i] : coefficients[i], i);
            }
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
    int coefficients[MAX_DEGREE + 1] = {0};
    int degree;

    degree = read_polynomial(coefficients);

    if (degree != -1)
    {
        printf("Polynomial: ");
        display_polynomial(coefficients, degree);
    }

    return 0;
}
