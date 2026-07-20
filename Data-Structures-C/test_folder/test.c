#include <stdio.h>

int a[10];
int n=-1;

void read_a_value()
{
	if ( n == 9 ){
		printf("Array is Full\n");
	}
	else
	{
		n++;
		printf("Enter the value of A[%d]",n);
		scanf("%d",&a[n]);
	}
}

void display_array()
{
	int i;
	for(i=0;i<=0;i++){
		printf("%d\t",a[i]);
	}
}



void main()
{

read_a_value();
read_a_value();
read_a_value();
read_a_value();
display_array();
}
