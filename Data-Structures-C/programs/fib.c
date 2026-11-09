#include <stdio.h>
void main()
	{
		int a=0,b=1,next,n=10;
		printf("%d %d ",a,b);
		for (int i=0;i<=n;i++){
			next = a+b;
			printf("%d ",next);
			a=b;
			b=next;
		}
	}
			
