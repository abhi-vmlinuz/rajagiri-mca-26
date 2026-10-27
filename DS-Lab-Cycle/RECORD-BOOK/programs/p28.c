#include <stdio.h>
#include <string.h>

#define MAX_STRINGS 20
#define MAX_LENGTH 50

int read_strings(char strings[][MAX_LENGTH])
{
    int count;
    int i;

    printf("Enter the number of strings: ");
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

    return count;
}

void display_strings(char strings[][MAX_LENGTH], int count)
{
    int i;

    for (i = 0; i < count; i++)
    {
        printf("%s\n", strings[i]);
    }
}

void sort_strings(char strings[][MAX_LENGTH], int count)
{
    int i;
    int j;
    char temporary[MAX_LENGTH];

    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (strcmp(strings[j], strings[j + 1]) > 0)
            {
                strcpy(temporary, strings[j]);
                strcpy(strings[j], strings[j + 1]);
                strcpy(strings[j + 1], temporary);
            }
        }
    }
}

int main(void)
{
    char strings[MAX_STRINGS][MAX_LENGTH];
    int count;

    count = read_strings(strings);

    if (count == 0)
    {
        return 0;
    }

    printf("Before sorting:\n");
    display_strings(strings, count);

    sort_strings(strings, count);

    printf("After sorting:\n");
    display_strings(strings, count);

    return 0;
}
