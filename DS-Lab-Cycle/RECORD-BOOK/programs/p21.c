#include <stdio.h>

typedef struct
{
    int day;
    int month;
    int year;
} Date;

void read_date(Date *date)
{
    printf("Enter the date (dd mm yyyy): ");
    scanf("%d %d %d", &date->day, &date->month, &date->year);
}

void display_date(Date date)
{
    printf("%02d/%02d/%04d\n", date.day, date.month, date.year);
}

int compare_dates(Date first, Date second)
{
    if (first.day == second.day &&
        first.month == second.month &&
        first.year == second.year)
    {
        return 1;
    }

    return 0;
}

int main(void)
{
    Date first;
    Date second;

    printf("First date:\n");
    read_date(&first);

    printf("Second date:\n");
    read_date(&second);

    printf("First date: ");
    display_date(first);

    printf("Second date: ");
    display_date(second);

    if (compare_dates(first, second) == 1)
    {
        printf("The dates are equal.\n");
    }
    else
    {
        printf("The dates are not equal.\n");
    }

    return 0;
}
