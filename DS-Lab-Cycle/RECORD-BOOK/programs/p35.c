#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int capacity = 2;
    int length = 0;
    char character;
    char *text;
    char *resized;

    text = malloc(capacity * sizeof(char));

    if (text == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    printf("Enter a string of any length: ");

    while ((character = (char) getchar()) != '\n' && character != EOF)
    {
        if (length + 1 >= capacity)
        {
            capacity = capacity * 2;
            resized = realloc(text, capacity * sizeof(char));

            if (resized == NULL)
            {
                printf("Memory reallocation failed.\n");
                free(text);
                return 1;
            }

            text = resized;
        }

        text[length] = character;
        length++;
    }

    text[length] = '\0';

    printf("You entered: %s\n", text);
    printf("Length: %d\n", length);

    free(text);

    return 0;
}
