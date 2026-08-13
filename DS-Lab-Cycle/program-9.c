#include <stdio.h>

#define MAX_LENGTH 100

void read_string(char text[])
{
    printf("Enter a string: ");
    scanf(" %99[^\n]", text);
}

void reverse_string(char text[])
{
    int length = 0;
    int left;
    int right;
    char temporary;

    while (text[length] != '\0')
    {
        length++;
    }

    left = 0;
    right = length - 1;
    while (left < right)
    {
        temporary = text[left];
        text[left] = text[right];
        text[right] = temporary;
        left++;
        right--;
    }
}

int main()
{
    char text[MAX_LENGTH];

    read_string(text);
    reverse_string(text);
    printf("String in reverse order: %s\n", text);

    return 0;
}
