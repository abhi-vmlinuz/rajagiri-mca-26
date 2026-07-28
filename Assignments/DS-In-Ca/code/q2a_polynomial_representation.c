#include <stdio.h>

int main()
{
    int degree, i;
    int poly1[20], poly2[20], result[20];

    printf("Enter the highest degree of polynomial: ");
    scanf("%d", &degree);

    printf("\nEnter coefficients of first polynomial:\n");

    for(i = 0; i <= degree; i++)
    {
        printf("Coefficient of x^%d : ", i);
        scanf("%d", &poly1[i]);
    }

    printf("\nEnter coefficients of second polynomial:\n");

    for(i = 0; i <= degree; i++)
    {
        printf("Coefficient of x^%d : ", i);
        scanf("%d", &poly2[i]);
    }

    for(i = 0; i <= degree; i++)
    {
        result[i] = poly1[i] + poly2[i];
    }

    printf("\nResultant Polynomial:\n");

    for(i = degree; i >= 0; i--)
    {
        if(result[i] != 0)
        {
            if(i == 0)
                printf("%d", result[i]);
            else if(i == 1)
                printf("%dx + ", result[i]);
            else
                printf("%dx^%d + ", result[i], i);
        }
    }

    printf("\n");

    return 0;
}
