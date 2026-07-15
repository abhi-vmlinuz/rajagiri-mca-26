#include <stdio.h>
#include <stdlib.h> // Included for the exit() function

// Function declarations (prototypes)
int getStringLength(char str[]);
void copyString(char dest[], char src[]);
void concatenateString(char str1[], char str2[]);
void reverseString(char str[]);
int compareStrings(char str1[], char str2[]);

int main()
{
    char s1[100], s2[100], copy[100];
    int ch;

    // Move initial inputs inside the loop if you want to change strings per run,
    // or keep them outside if you want to run operations on the same strings.
    printf("Enter first string: ");
    scanf("%s", s1);

    printf("Enter second string: ");
    scanf("%s", s2);

    // Infinite loop starts here
    while(1) 
    {
        printf("\n\n--- String Operations Menu ---");
        printf("\n1. strlen\n2. strcpy\n3. strcat\n4. strrev\n5. strcmp\n6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &ch);

        switch(ch)
        {
            case 1:
                printf("Length = %d", getStringLength(s1));
                break;

            case 2:
                copyString(copy, s1);
                printf("Copied String = %s", copy);
                break;

            case 3:
                // Note: Modifies s1 in place. Subsequent operations will use the modified s1.
                concatenateString(s1, s2);
                printf("Concatenated String = %s", s1);
                break;

            case 4:
                reverseString(s1);
                printf("Reversed String = %s", s1);
                break;

            case 5:
                if(compareStrings(s1, s2) == 1)
                    printf("Strings are Equal");
                else
                    printf("Strings are Not Equal");
                break;

            case 6:
                printf("Exiting program. Goodbye!\n");
                exit(0); // Safely terminates the program execution

            default:
                printf("Invalid Choice. Please try again.");
        }
    }

    return 0;
}

// 1. Function to find string length
int getStringLength(char str[])
{
    int i = 0;
    while(str[i] != '\0')
        i++;
    return i;
}

// 2. Function to copy a string
void copyString(char dest[], char src[])
{
    int i = 0;
    while(src[i] != '\0')
    {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0'; // Append the null terminator
}

// 3. Function to concatenate two strings
void concatenateString(char str1[], char str2[])
{
    int i = 0, j = 0;
    
    // Find the end of the first string
    while(str1[i] != '\0')
        i++;

    // Append the second string
    while(str2[j] != '\0')
    {
        str1[i] = str2[j];
        i++;
        j++;
    }
    str1[i] = '\0'; // Append the null terminator
}

// 4. Function to reverse a string
void reverseString(char str[])
{
    int i = 0;
    int j = getStringLength(str) - 1; // Reusing our length function
    char temp;

    while(i < j)
    {
        temp = str[i];
        str[i] = str[j];
        str[j] = temp;
        i++;
        j--;
    }
}

// 5. Function to compare two strings (returns 1 if equal, 0 if not)
int compareStrings(char str1[], char str2[])
{
    int i = 0;
    while(str1[i] == str2[i] && str1[i] != '\0')
        i++;

    if(str1[i] == str2[i])
        return 1; // Equal
    else
        return 0; // Not Equal
}
