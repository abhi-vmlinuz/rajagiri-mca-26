#include <stdio.h>
void main()
{
	int fact=1;
	int n=5;
	for (int i=1;i<=n;i++){
		fact*=i;
	}
	printf("Factorial = %d",fact);
}

