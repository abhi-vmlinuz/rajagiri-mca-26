#include <stdio.h>
#include <string.h>

int main()
{
    char str[6] = "HELLO";

    printf("strlen = %zu\n", strlen(str));
    printf("sizeof = %zu\n", sizeof(str));

    return 0;
}
