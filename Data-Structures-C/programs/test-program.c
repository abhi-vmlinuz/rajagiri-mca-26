#include <stdio.h>

int players[10];
int n;
void add_players(){
       printf("Enter the player number for pos %d: \n",players[n]);
       scanf("%d",&players[n]); 
       n+=1;
}

void display(){
	register int i;
	for (i=0;i<=n;i++){
		printf(" |[%d]",&players[n]);
	}
}

int menu(){
	int choice;
	printf("1. Add players\n2.Display All players\n3.EXIT\n\nEnter your choice\n");
	scanf("%d",&choice);
	return choice;
}

void process(){
	register int choice;
	for (choice = menu();choice !=3;menu()){
		switch(choice){
			case 1:
				add_players();
				break;
			case 2:
				display();
				break;
			default:
				printf("Wrong Choice");
			}
	}
}
void main()
{
	process();
}
