#include <stdio.h>
int n=0;
int a[];
int read(){
	for(int i=0;i<n;i++){
		printf("Enter the element at a[%d]: ",i);
		scanf("%d",&a[i]);
	}
}

void disp(){
	int i=0;
	for(i=0;i<n;i++){
		printf("[%d] ",a[i]);
	}
}

int search(){
	int s,i;
	printf("\nEnter the element to search: ");
	scanf("%d",&s);
	for(i=0;i<n;i++){
		if(a[i] == s){
		return i;
		}
	}
	return -1;
}

void deletee()
{
	int del;
	int i;
	printf("Current Array: \n");
	for ( i=0;i<n;i++){
		printf("[%d] ",a[i]);
	}
	
	// basic 
	printf("\nEnter the element to delete: \n");
	scanf("%d",&del);
	for(i=0;i<n;i++){
		if(del == a[i])
		continue;
		printf("[%d] ",a[i]);
	}
}
int menu(){
	// menu function for prompting user
	int ch;
	printf("\n1.Insert\n2.Display\n3.Search\n4.Delete\n5.Exit\nEnter your choice: ");
	scanf("%d",&ch);
	return ch;
}
void process()
{
	// process menu with switch
	int ch;
	for(ch = menu();ch!=5;ch = menu()){
		switch(ch){
			case 1:
			read();
			break;
			case 2:
				disp();
				break;
			case 3:
				ch=search();
				if (ch == -1)
				printf("\nElement not found");
				else
				printf("\nElement found at index: %d",ch);
				break;
			case 4:
				deletee();
				break;
			default:
				printf("Wrong Choice\n");
		}
	}
}

void main()
{
	printf("Enter the size of the array: ");
	scanf("%d",&n);
	process();
}
