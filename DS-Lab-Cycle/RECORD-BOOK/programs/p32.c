#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int count;
    int i;
    int sum = 0;
    float mean;
    int *numbers;

    printf("Enter the number of integers: ");
    scanf("%d", &count);

    if (count < 1)
    {
        printf("Invalid number of integers.\n");
        return 0;
    }

    numbers = malloc(count * sizeof(int));

    if (numbers == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (i = 0; i < count; i++)
    {
        printf("Enter integer %d: ", i + 1);
        scanf("%d", &numbers[i]);
        sum += numbers[i];
    }

    mean = (float) sum / count;

    printf("Mean = %.2f\n", mean);

    free(numbers);

    return 0;
}
