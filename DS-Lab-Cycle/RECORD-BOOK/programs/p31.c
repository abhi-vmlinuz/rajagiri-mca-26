#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int count = 5;
    int i;
    int *malloc_array;
    int *calloc_array;

    malloc_array = malloc(count * sizeof(int));

    if (malloc_array == NULL)
    {
        printf("malloc failed.\n");
        return 1;
    }

    printf("Values allocated with malloc:\n");

    for (i = 0; i < count; i++)
    {
        malloc_array[i] = (i + 1) * 10;
        printf("%d ", malloc_array[i]);
    }

    printf("\n");
    free(malloc_array);
    printf("Memory allocated with malloc has been freed.\n");

    calloc_array = calloc(count, sizeof(int));

    if (calloc_array == NULL)
    {
        printf("calloc failed.\n");
        return 1;
    }

    printf("Values allocated with calloc:\n");

    for (i = 0; i < count; i++)
    {
        printf("%d ", calloc_array[i]);
    }

    printf("\n");
    free(calloc_array);
    printf("Memory allocated with calloc has been freed.\n");

    return 0;
}
