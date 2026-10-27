#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_LENGTH 50
#define SUBJECTS 5
#define FILE_NAME "students.txt"

typedef struct Student
{
    int roll;
    char name[NAME_LENGTH];
    int marks[SUBJECTS];
    int total;
    struct Student *next;
} Student;

Student *create_student(int roll, const char *name, int marks[])
{
    Student *student = malloc(sizeof(Student));
    int i;

    if (student == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    student->roll = roll;
    strcpy(student->name, name);
    student->total = 0;

    for (i = 0; i < SUBJECTS; i++)
    {
        student->marks[i] = marks[i];
        student->total += marks[i];
    }

    student->next = NULL;

    return student;
}

void insert_end(Student **head, Student *student)
{
    Student *current;

    if (student == NULL)
    {
        return;
    }

    if (*head == NULL)
    {
        *head = student;
        return;
    }

    current = *head;

    while (current->next != NULL)
    {
        current = current->next;
    }

    current->next = student;
}

Student *find_student(Student *head, int roll)
{
    Student *current = head;

    while (current != NULL)
    {
        if (current->roll == roll)
        {
            return current;
        }

        current = current->next;
    }

    return NULL;
}

void read_marks(int marks[])
{
    int i;

    for (i = 0; i < SUBJECTS; i++)
    {
        printf("Enter mark %d: ", i + 1);
        scanf("%d", &marks[i]);
    }
}

void add_student(Student **head)
{
    int roll;
    char name[NAME_LENGTH];
    int marks[SUBJECTS];
    Student *student;

    printf("Enter roll number: ");
    scanf("%d", &roll);

    if (find_student(*head, roll) != NULL)
    {
        printf("Roll number %d already exists.\n", roll);
        return;
    }

    printf("Enter name: ");
    scanf(" %49[^\n]", name);
    read_marks(marks);

    student = create_student(roll, name, marks);

    if (student != NULL)
    {
        insert_end(head, student);
        printf("Student added.\n");
    }
}

void display_students(Student *head)
{
    Student *current = head;
    int i;

    if (current == NULL)
    {
        printf("No student records.\n");
        return;
    }

    printf("%-8s %-20s %-20s %-8s\n", "Roll", "Name", "Marks", "Total");

    while (current != NULL)
    {
        printf("%-8d %-20s ", current->roll, current->name);

        for (i = 0; i < SUBJECTS; i++)
        {
            printf("%d ", current->marks[i]);
        }

        printf("%-8d\n", current->total);
        current = current->next;
    }
}

void update_student(Student *head)
{
    int roll;
    char name[NAME_LENGTH];
    int marks[SUBJECTS];
    int i;
    Student *student;

    printf("Enter the roll number to update: ");
    scanf("%d", &roll);

    student = find_student(head, roll);

    if (student == NULL)
    {
        printf("Student %d not found.\n", roll);
        return;
    }

    printf("Enter the new name: ");
    scanf(" %49[^\n]", name);
    read_marks(marks);

    strcpy(student->name, name);
    student->total = 0;

    for (i = 0; i < SUBJECTS; i++)
    {
        student->marks[i] = marks[i];
        student->total += marks[i];
    }

    printf("Student updated.\n");
}

void delete_student(Student **head)
{
    int roll;
    Student *current = *head;
    Student *previous = NULL;

    printf("Enter the roll number to delete: ");
    scanf("%d", &roll);

    while (current != NULL && current->roll != roll)
    {
        previous = current;
        current = current->next;
    }

    if (current == NULL)
    {
        printf("Student %d not found.\n", roll);
        return;
    }

    if (previous == NULL)
    {
        *head = current->next;
    }
    else
    {
        previous->next = current->next;
    }

    free(current);
    printf("Student %d deleted.\n", roll);
}

void swap_data(Student *first, Student *second)
{
    int roll = first->roll;
    char name[NAME_LENGTH];
    int marks[SUBJECTS];
    int total = first->total;
    int i;

    strcpy(name, first->name);

    for (i = 0; i < SUBJECTS; i++)
    {
        marks[i] = first->marks[i];
    }

    first->roll = second->roll;
    strcpy(first->name, second->name);
    first->total = second->total;

    for (i = 0; i < SUBJECTS; i++)
    {
        first->marks[i] = second->marks[i];
    }

    second->roll = roll;
    strcpy(second->name, name);
    second->total = total;

    for (i = 0; i < SUBJECTS; i++)
    {
        second->marks[i] = marks[i];
    }
}

void sort_by_roll(Student *head)
{
    Student *current;
    Student *next;
    int swapped;

    do
    {
        swapped = 0;
        current = head;

        while (current != NULL && current->next != NULL)
        {
            next = current->next;

            if (current->roll > next->roll)
            {
                swap_data(current, next);
                swapped = 1;
            }

            current = current->next;
        }
    } while (swapped == 1);
}

void sort_by_name(Student *head)
{
    Student *current;
    Student *next;
    int swapped;

    do
    {
        swapped = 0;
        current = head;

        while (current != NULL && current->next != NULL)
        {
            next = current->next;

            if (strcmp(current->name, next->name) > 0)
            {
                swap_data(current, next);
                swapped = 1;
            }

            current = current->next;
        }
    } while (swapped == 1);
}

void save_to_file(Student *head)
{
    FILE *file = fopen(FILE_NAME, "w");
    Student *current = head;
    int i;

    if (file == NULL)
    {
        printf("Unable to open %s for writing.\n", FILE_NAME);
        return;
    }

    while (current != NULL)
    {
        fprintf(file, "%d|%s|", current->roll, current->name);

        for (i = 0; i < SUBJECTS; i++)
        {
            fprintf(file, "%d", current->marks[i]);

            if (i < SUBJECTS - 1)
            {
                fprintf(file, " ");
            }
        }

        fprintf(file, "\n");
        current = current->next;
    }

    fclose(file);
    printf("Records saved to %s.\n", FILE_NAME);
}

void free_list(Student *head)
{
    Student *current = head;
    Student *next;

    while (current != NULL)
    {
        next = current->next;
        free(current);
        current = next;
    }
}

void load_from_file(Student **head)
{
    FILE *file = fopen(FILE_NAME, "r");
    int roll;
    char name[NAME_LENGTH];
    int marks[SUBJECTS];
    Student *student;

    if (file == NULL)
    {
        printf("Unable to open %s for reading.\n", FILE_NAME);
        return;
    }

    free_list(*head);
    *head = NULL;

    while (fscanf(file, "%d|%49[^|]|%d %d %d %d %d",
                  &roll,
                  name,
                  &marks[0],
                  &marks[1],
                  &marks[2],
                  &marks[3],
                  &marks[4]) == 7)
    {
        student = create_student(roll, name, marks);

        if (student != NULL)
        {
            insert_end(head, student);
        }
    }

    fclose(file);
    printf("Records loaded from %s.\n", FILE_NAME);
}

void print_menu(void)
{
    printf("\n1. Add student\n");
    printf("2. Display students\n");
    printf("3. Save to file\n");
    printf("4. Load from file\n");
    printf("5. Update student\n");
    printf("6. Delete student\n");
    printf("7. Sort by roll number\n");
    printf("8. Sort by name\n");
    printf("9. Exit\n");
}

int main(void)
{
    Student *head = NULL;
    int choice;

    do
    {
        print_menu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
            case 1:
                add_student(&head);
                break;
            case 2:
                display_students(head);
                break;
            case 3:
                save_to_file(head);
                break;
            case 4:
                load_from_file(&head);
                break;
            case 5:
                update_student(head);
                break;
            case 6:
                delete_student(&head);
                break;
            case 7:
                sort_by_roll(head);
                printf("Sorted by roll number.\n");
                break;
            case 8:
                sort_by_name(head);
                printf("Sorted by name.\n");
                break;
            case 9:
                printf("Program ended.\n");
                break;
            default:
                printf("Invalid choice.\n");
        }
    } while (choice != 9);

    free_list(head);

    return 0;
}
