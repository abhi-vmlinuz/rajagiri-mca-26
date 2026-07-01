#include <stdio.h>
void main()
{
	int x,y;
	printf("Enter the value of X and Y: ");
	scanf("%d%d", &x,&y);
	if ( x > 0 && y > 0){
		printf("Your point lies on the first coordinate");
	}
	else if ( x < 0 && y > 0)
	{
		printf("Your point lies on the second coordinate");
	}
	else if ( x < 0 && y < 0)
	{
		printf("Your point lies on the third quadrant");
	}
	else if ( x > 0 && y < 0)
	{
		printf("Your point lies on the 4th Quadrant");
	}else{
		printf("Invalid Input");
	}}
