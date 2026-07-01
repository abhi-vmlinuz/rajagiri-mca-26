#include <stdio.h>
void main()
{
	int choice, num1, num2;
	printf("Enter the Numbers for the operations to be done: ");
	scanf("%d%d",&num1,&num2);

	printf("Choose the operation: ");
	printf("\n=====================\n");
	printf("1. Addition\n");
	printf("2. Subtraction\n");
	printf("3. Multiplication\n");
	printf("4. Division\n");
	printf("5. Modulo\n");
	printf("\n\n");
	scanf("%d",&choice);
	switch(choice)
	{
		case 1:
			printf("You chose Addition\n");
			printf("%d",(num1+num2));
			break;
		case 2:
			printf("You chose Subtraction\n");
			printf("%d",(num1 - num2));
			break;
		case 3:
			printf("You chose Multiplication\n");
			printf("%d",(num1 * num2));
			break;
		case 4:
			printf("You chose Division: \n");
			printf("%d",(num1 / num2));
			break;
		case 5:
			printf("You chose Modulo: \n");
			printf("%d",(num1 % num2));
			break;
		default:
			printf("baka");
			break;
	}
}


