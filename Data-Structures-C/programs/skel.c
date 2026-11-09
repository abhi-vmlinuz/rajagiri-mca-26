#include <stdio.h>
void main()
{

int n, digit,reverse=0;
printf("Enter N: ");
scanf("%d",&n);
while(n > 0)
{
    digit = n % 10;

    // Do something with digit
    reverse = reverse * 10 + digit;	

    n = n / 10;
}
printf("rev: %d",reverse);
}
