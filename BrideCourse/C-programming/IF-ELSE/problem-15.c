#include <stdio.h>
void main()
{
	int num;
	printf("Enter a number: ");
	scanf("%d",&num);
	if (num % 2 == 0)
	{
		printf("The number entered is a prime number\n");
	}
	else
	{
		printf("The entered number isn't prime");
	}
}
