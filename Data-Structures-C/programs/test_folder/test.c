#include <string.h>
#include <stdio.h>
int main()
{
	char ch[5];
	int len;
	printf("Enter a string value: ");
	scanf("%s",ch);
	len = strlen(ch);
	printf("Size of string is: %d\n",len);
	for(int i=0;i<=len;i++)
	{
		printf("%c %d\n",ch[i],i);
	}
	return 0;
}
