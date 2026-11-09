#include <stdio.h>
void main()
{
	int n;
	printf("Enter the value of n: ");
	scanf("%d",&n);
	printf("\n\n");
	for(int i=n;i>=1;i--){
		if( i != 1){
			printf("%d - ",i);
		}else {
			printf("%d",i);
		}
	}
}
	
