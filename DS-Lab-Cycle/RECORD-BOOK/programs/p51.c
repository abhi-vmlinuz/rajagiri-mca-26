#include <stdio.h>
#include <string.h>

#define MAX_STRINGS 50
#define MAX_LENGTH 50

int binary_search_strings(char strings[][MAX_LENGTH], int count, char value[])
{
    int low = 0;
    int high = count - 1;
    int middle;
    int comparison;

    while (low <= high)
    {
        middle = (low + high) / 2;
        comparison = strcmp(strings[middle], value);

        if (comparison == 0)
        {
            return middle;
        }

        if (comparison < 0)
        {
            low = middle + 1;
        }
        else
        {
            high = middle - 1;
        }
    }

    return -1;
}

int main(void)
{
    char strings[MAX_STRINGS][MAX_LENGTH];
    char value[MAX_LENGTH];
    int count;
    int position;
    int i;

    printf("Enter the number of sorted strings: ");
    scanf("%d", &count);

    if (count < 1 || count > MAX_STRINGS)
    {
        printf("Invalid number of strings.\n");
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        printf("Enter string %d: ", i + 1);
        scanf(" %49[^\n]", strings[i]);
    }

    printf("Enter the string to search: ");
    scanf(" %49[^\n]", value);

    position = binary_search_strings(strings, count, value);

    if (position == -1)
    {
        printf("%s not found.\n", value);
    }
    else
    {
        printf("%s found at position %d.\n", value, position + 1);
    }

    return 0;
}
