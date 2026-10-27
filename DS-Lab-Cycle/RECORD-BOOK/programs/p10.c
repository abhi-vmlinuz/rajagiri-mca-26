#include <stdio.h>

#define MAX_STRINGS 20
#define MAX_LENGTH 50

int read_strings(char strings[][MAX_LENGTH])
{
    int count;
    int i;

    printf("Enter the number of strings (maximum %d): ", MAX_STRINGS);
    scanf("%d", &count);

    if (count < 1 || count > MAX_STRINGS)
    {
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        printf("Enter string %d: ", i + 1);
        scanf(" %49[^\n]", strings[i]);
    }

    return count;
}

int compare_strings(char first[], char second[])
{
    int i = 0;

    while (first[i] != '\0' && second[i] != '\0')
    {
        if (first[i] < second[i])
        {
            return -1;
        }
        if (first[i] > second[i])
        {
            return 1;
        }
        i++;
    }

    if (first[i] == '\0' && second[i] == '\0')
    {
        return 0;
    }
    if (first[i] == '\0')
    {
        return -1;
    }
    return 1;
}

void sort_strings(char strings[][MAX_LENGTH], int count)
{
    int i;
    int j;
    int k;
    char temporary;

    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (compare_strings(strings[j], strings[j + 1]) > 0)
            {
                for (k = 0; k < MAX_LENGTH; k++)
                {
                    temporary = strings[j][k];
                    strings[j][k] = strings[j + 1][k];
                    strings[j + 1][k] = temporary;
                }
            }
        }
    }
}

void display_strings(char strings[][MAX_LENGTH], int count)
{
    int i;

    for (i = 0; i < count; i++)
    {
        printf("%s\n", strings[i]);
    }
}

int main()
{
    char strings[MAX_STRINGS][MAX_LENGTH];
    int count;

    count = read_strings(strings);
    if (count == 0)
    {
        printf("Invalid number of strings.\n");
        return 0;
    }

    sort_strings(strings, count);

    printf("Strings in ascending order:\n");
    display_strings(strings, count);

    return 0;
}
