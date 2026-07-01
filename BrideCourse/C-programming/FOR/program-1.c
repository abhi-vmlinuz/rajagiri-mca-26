#include <stdio.h>
void main()
{
	int i, num;
	printf("Enter the number: \n");
	scanf("%d",&num);
	for (i=1;i<=10;i++){
		printf("%d x %d is %d\n",i,num,(i*num));
	}
}
