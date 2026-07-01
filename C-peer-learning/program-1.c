#include <stdio.h>
void main()
{
	int m,n;
	printf("Enter a number: ");
	scanf("%d",&m);
	if (m > 0){
		n = 1;
	}
	else if (m == 0)
	{
		n = 0;
	}else {
		n = -1;
	}
	printf("%d is N", n);
}

