#include <stdio.h>
int main()
{
	int a = 10, b=20;
	printf("Original Values: A: %d , B: %d",a,b);

	int temp = a;
	a = b;
	b = temp;
	printf("\nValues after temp swap: A: %d, B: %d\n", a,b);

	a = a+b;
	b = a-b;
	a = a-b;
	printf("After math swap: A: %d, B: %d\n",a,b);

	a = a ^ b;
	b = a ^ b;
	a = a ^ b;
	printf("After XOR Swap: A: %d, B: %d",a,b);

	return 0;
}
