#include <stdio.h>

int a[10];
int n;

void read()
{
 	printf("Enter");
	scanf("%d",&a[n]);
	n++;
}

void display(){
        register int i;
        for (i=0;i<=n;i++){
                printf(" |[%d]",&a[n]);
        }
}
void main()
{
	read();
	read();
	read();
	display();
}
