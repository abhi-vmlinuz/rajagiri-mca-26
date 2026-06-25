#include <stdio.h>
#define PI 3.14159

int main() {

float radius, area, perimeter;
printf("Enter the radius: ");
 if(scanf("%f",&radius) == 1){
    area = PI * radius * radius;
    perimeter = 2 * PI * radius;

    printf("Area: %.2f\n", area);
    printf("Perimeter: %.2f\n", perimeter);

}
else
{
  printf("Invalid Input\n");
}
return 0;
}
