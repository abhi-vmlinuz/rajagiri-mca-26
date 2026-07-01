#include <stdio.h>
void main()
{
	
	int count=0, n, total_sum, current_no;
	printf("Enter the total count of numbers: ");
	scanf("%d",&n);
	while (count < n){
		printf("Enter the number: ");
		scanf("%d",&current_no);
		total_sum += current_no;

		count++;
	}
	printf("\nTotal Sum is %d", total_sum);
}
