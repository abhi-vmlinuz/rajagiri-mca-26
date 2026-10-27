#include<stdio.h>

  int a[10],n=0;
  void read()
  {
  	printf("\nEnter a elemnt:\t");
	  scanf("%d",&a[n]);
	  n++;	  
  }
  
  void disp()
  {
  	int i;
  	if(n==0)
  	{
  		printf("\n___NO ELEMENT TO DISPLAY___\n\n");
	  }else
	  {
	  
  	for(i=0;i<n;i++)
  	 {
  		printf("%d\t",a[i]);
	 }
  }
}
  void search()
  {
  	int s,i,flag=0;
  	printf("Enter element to search:\t");
  	scanf("%d",&s);
  	for(i=0;i<n;i++)
  	{
  		if(a[i]==s)
  		{
  			printf("%d found at position %d\n",s,i+1);
  			flag=1;
		  }
		  
	  }
	  if(flag==0)
	  {
	  	printf("%d Not found\n\n",s);

	  }

  }
  void deletee()
  {
	int i, j, del, flag=0;
  	printf("Enter the element to delete:\t");
  	scanf("%d",&del);
  	for(i=0;i<n;i++)
  	{
  		if(a[i]==del)
  		{
			for(j=i;j<n-1;j++)
			{
				a[j]=a[j+1];
			}
			n--;
			flag=1;
			printf("%d Deleted\n\n",del);
			break;
		  }
	  }
	  if(flag==0)
  {
  	printf("%d Not found\n\n",del);
  }
}
  void sort()
  {
  	int i,j,temp;
    for(i=0;i<n-1;i++)
    {
    	for(j=i+1;j<n;j++)
    	{
    		if(a[i]>a[j])
    		{
    			temp=a[i];
    			a[i]=a[j];
    			a[j]=temp;
            }
        }    
  }
  for(i=0;i<n;i++)
  {
  	printf("%d\t",a[i]);
  }
}  
  int main()
  {
  		int ch;
  	do{
  	printf(" 1.Insert \n 2.Display \n 3.Search \n 4.Delete \n 5.Sort \n 6.Exit\nEnter a Option:\t");
  	scanf("%d",&ch);
	  switch(ch)
	  {
	  	case 1: read();
	  	break;
	  	case 2: disp();
	  	break;
	  	case 3: search();
	  	break;
        case 4: deletee();
      	break;
        case 5: sort();
        break;
      	case 6: printf("Exiting............");
	  	break;
	  	default: printf("______Invalid Option________");
	  }
	  } while(ch != 6);
	  return 0;
  }
