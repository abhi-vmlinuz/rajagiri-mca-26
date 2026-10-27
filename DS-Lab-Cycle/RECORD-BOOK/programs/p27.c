#include <stdio.h>
#include <string.h>

#define MAX_LENGTH 100

void read_string(char text[])
{
    printf("Enter a string: ");
    scanf(" %99[^\n]", text);
}

void print_reverse(char text[])
{
    int i;

    printf("Reverse order: ");

    for (i = (int) strlen(text) - 1; i >= 0; i--)
    {
        printf("%c", text[i]);
    }

    printf("\n");
}

void reverse_in_place(char text[])
{
    int i;
    int j;
    char temporary;

    i = 0;
    j = (int) strlen(text) - 1;

    while (i < j)
    {
        temporary = text[i];
        text[i] = text[j];
        text[j] = temporary;
        i++;
        j--;
    }
}

int main(void)
{
    char text[MAX_LENGTH];

    read_string(text);

    print_reverse(text);

    reverse_in_place(text);
    printf("Reversed string: %s\n", text);

    return 0;
}
