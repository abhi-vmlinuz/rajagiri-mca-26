#include <stdio.h>
void main()
{
	int choice, num1, num2;
	printf("Enter the Numbers for the operations to be done: ");
	scanf("%d%d",&num1,&num2);

	printf("Choose the operation: ");
	printf("\n=====================\n");
	printf("1. BITWISE OR\n");
	printf("2. BITWISE AND\n");
	printf("3. BITWISE XOR\n");
	printf("4. Left Shift\n");
	printf("5. Right Shift\n");
	printf("\n\n");
	scanf("%d",&choice);
	switch(choice)
	{
		case 1:
			printf("You chose BITWISE OR\n");
			printf("%d",(num1|num2));
			break;
		case 2:
			printf("You chose BITWISE AND\n");
			printf("%d",(num1 & num2));
			break;
		case 3:
			printf("You chose BITWISE XOR\n");
			printf("%d",(num1 ^ num2));
			break;
		case 4:
			printf("You chose Left shift: \n");
			printf("%d",(num1 << num2));
			break;
		case 5:
			printf("You chose right shift: \n");
			printf("%d",(num1 >> num2));
			break;
		default:
			printf("baka");
			break;
	}
}


