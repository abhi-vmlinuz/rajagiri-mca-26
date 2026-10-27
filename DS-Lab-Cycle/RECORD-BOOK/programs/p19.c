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

int subtract_polynomials(int first[], int first_degree, int second[], int second_degree, int result[])
{
    int degree;
    int i;

    degree = first_degree > second_degree ? first_degree : second_degree;

    for (i = 0; i <= degree; i++)
    {
        result[i] = 0;

        if (i <= first_degree)
        {
            result[i] += first[i];
        }

        if (i <= second_degree)
        {
            result[i] -= second[i];
        }
    }

    return degree;
}

int main(void)
{
    int first[MAX_DEGREE + 1] = {0};
    int second[MAX_DEGREE + 1] = {0};
    int result[MAX_DEGREE + 1] = {0};
    int first_degree;
    int second_degree;
    int result_degree;

    printf("First polynomial:\n");
    first_degree = read_polynomial(first);

    if (first_degree == -1)
    {
        return 0;
    }

    printf("Second polynomial:\n");
    second_degree = read_polynomial(second);

    if (second_degree == -1)
    {
        return 0;
    }

    result_degree = subtract_polynomials(first, first_degree, second, second_degree, result);

    printf("First polynomial: ");
    display_polynomial(first, first_degree);
    printf("Second polynomial: ");
    display_polynomial(second, second_degree);
    printf("Difference: ");
    display_polynomial(result, result_degree);

    return 0;
}
