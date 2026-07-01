#include <stdio.h>
void main()
{
	int n, sum, i;
	printf("Enter a number: \n"); scanf("%d",&n);
	sum = 0;
	for (i;i<=n;i++)
	{
		sum = sum + i;
		printf("Sum is %d\n",sum);
	}
}
