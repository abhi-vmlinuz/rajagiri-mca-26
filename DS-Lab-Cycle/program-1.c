#include <stdio.h>

/* This declaration refers to the definition below.  No separate header file
   is needed for this single-file demonstration. */
extern int global_variable;
int global_variable = 10;

void show_local_variable()
{
    auto int local_variable = 5;

    printf("Local variable: %d\n", local_variable);
}

void show_global_variable()
{
    printf("Global variable accessed through extern declaration: %d\n",
           global_variable);
}

void show_static_variable()
{
    static int static_variable = 1;

    printf("Static variable: %d\n", static_variable);
    static_variable++;
}

void show_register_variable()
{
    register int register_variable;

    for (register_variable = 1; register_variable <= 3; register_variable++)
    {
        printf("Register variable: %d\n", register_variable);
    }
}

int main()
{
    printf("Storage class demonstration\n\n");

    show_local_variable();
    show_global_variable();

    printf("First call to the static variable function:\n");
    show_static_variable();
    printf("Second call to the static variable function:\n");
    show_static_variable();

    show_register_variable();

    return 0;
}
