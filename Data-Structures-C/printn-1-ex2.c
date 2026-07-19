#include <stdio.h>
int main(){
	int n;
	printf("Enter the value of N: ");
	scanf("%d",&n);
	for ( int i=n;i>=2;i-=2){
		printf("%d - ",i);
	}
	return 0;
}
