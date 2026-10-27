#include <stdio.h>
#include <string.h>

#define MAX_EMPLOYEES 50

typedef struct
{
    int eno;
    char ename[50];
    float esal;
    int dno;
} Employee;

void read_employees(Employee employees[], int count)
{
    int i;

    for (i = 0; i < count; i++)
    {
        printf("Employee %d\n", i + 1);
        printf("Enter employee number: ");
        scanf("%d", &employees[i].eno);
        printf("Enter employee name: ");
        scanf(" %49[^\n]", employees[i].ename);
        printf("Enter employee salary: ");
        scanf("%f", &employees[i].esal);
        printf("Enter department number: ");
        scanf("%d", &employees[i].dno);
    }
}

void display_employees(Employee employees[], int count)
{
    int i;

    printf("%-8s %-25s %-10s %-8s\n", "Eno", "Name", "Salary", "Dno");

    for (i = 0; i < count; i++)
    {
        printf("%-8d %-25s %-10.2f %-8d\n",
               employees[i].eno,
               employees[i].ename,
               employees[i].esal,
               employees[i].dno);
    }
}

void search_by_number(Employee employees[], int count, int number)
{
    int i;

    for (i = 0; i < count; i++)
    {
        if (employees[i].eno == number)
        {
            printf("Employee found: %d %s %.2f %d\n",
                   employees[i].eno,
                   employees[i].ename,
                   employees[i].esal,
                   employees[i].dno);
            return;
        }
    }

    printf("Employee %d not found.\n", number);
}

void sort_by_name(Employee employees[], int count)
{
    int i;
    int j;
    Employee temporary;

    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (strcmp(employees[j].ename, employees[j + 1].ename) > 0)
            {
                temporary = employees[j];
                employees[j] = employees[j + 1];
                employees[j + 1] = temporary;
            }
        }
    }
}

void sort_by_salary(Employee employees[], int count)
{
    int i;
    int j;
    Employee temporary;

    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (employees[j].esal < employees[j + 1].esal)
            {
                temporary = employees[j];
                employees[j] = employees[j + 1];
                employees[j + 1] = temporary;
            }
        }
    }
}

int delete_employee(Employee employees[], int count, int number)
{
    int i;
    int position = -1;

    for (i = 0; i < count; i++)
    {
        if (employees[i].eno == number)
        {
            position = i;
            break;
        }
    }

    if (position == -1)
    {
        printf("Employee %d not found.\n", number);
        return count;
    }

    for (i = position; i < count - 1; i++)
    {
        employees[i] = employees[i + 1];
    }

    printf("Employee %d deleted.\n", number);
    return count - 1;
}

int main(void)
{
    Employee employees[MAX_EMPLOYEES];
    int count;

    printf("Enter the number of employees: ");
    scanf("%d", &count);

    if (count < 1 || count > MAX_EMPLOYEES)
    {
        printf("Invalid number of employees.\n");
        return 0;
    }

    read_employees(employees, count);

    printf("\nEmployee records:\n");
    display_employees(employees, count);

    printf("\nSearch by employee number 102:\n");
    search_by_number(employees, count, 102);

    printf("\nSorted by name:\n");
    sort_by_name(employees, count);
    display_employees(employees, count);

    printf("\nSorted by salary:\n");
    sort_by_salary(employees, count);
    display_employees(employees, count);

    printf("\nDelete employee number 102:\n");
    count = delete_employee(employees, count, 102);
    display_employees(employees, count);

    return 0;
}
