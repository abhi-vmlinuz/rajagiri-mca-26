#include <stdio.h>
void main()
{
	int n,i,sum;
	printf("Enter a number: ");
	scanf("%d",&n);
	i=1;
	sum=0;
	while (i<=n){
		printf("%d Sum\n",sum);
		sum=sum+i;
		i++;
	}
	
}

