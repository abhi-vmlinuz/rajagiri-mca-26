#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int count;
    int i;
    int maximum;
    int mode;
    int highest_frequency = 0;
    int *numbers;
    int *frequency;

    printf("Enter the number of values: ");
    scanf("%d", &count);

    if (count < 1)
    {
        printf("Invalid number of values.\n");
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
        printf("Enter value %d: ", i + 1);
        scanf("%d", &numbers[i]);
    }

    maximum = numbers[0];

    for (i = 1; i < count; i++)
    {
        if (numbers[i] > maximum)
        {
            maximum = numbers[i];
        }
    }

    frequency = calloc(maximum + 1, sizeof(int));

    if (frequency == NULL)
    {
        printf("Memory allocation failed.\n");
        free(numbers);
        return 1;
    }

    for (i = 0; i < count; i++)
    {
        frequency[numbers[i]]++;
    }

    mode = 0;

    for (i = 0; i <= maximum; i++)
    {
        if (frequency[i] > highest_frequency)
        {
            highest_frequency = frequency[i];
            mode = i;
        }
    }

    printf("Mode = %d (frequency %d)\n", mode, highest_frequency);

    free(numbers);
    free(frequency);

    return 0;
}
