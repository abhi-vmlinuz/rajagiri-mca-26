#include <stdio.h>
#include <stdlib.h>

struct student {
    char name[50];
    int roll_no;
    int marks;
    struct student *next;
};

typedef struct student list;
list *head = NULL;

void insert() {
    list *temp = (list *)malloc(sizeof(list));
    if (temp == NULL) {
        printf("Memory allocation failed!\n");
        return;
    }

    printf("Enter name: ");
    scanf("%s", temp->name);
    printf("Enter roll no: ");
    scanf("%d", &temp->roll_no);
    printf("Enter marks: ");
    scanf("%d", &temp->marks);

    temp->next = head;
    head = temp;

    printf("Inserted successfully!\n\n");
}

void display() {
    if (head == NULL) {
        printf("List is empty.\n\n");
        return;
    }

    list *curr = head;
    printf("\n--- Records ---\n");
    while (curr != NULL) {
        printf("Roll No: %d | Name: %s | Marks: %d\n", curr->roll_no, curr->name, curr->marks);
        curr = curr->next;
    }
    printf("---------------\n\n");
}

void search() {
    if (head == NULL) {
        printf("List is empty.\n\n");
        return;
    }

    int target_roll;
    printf("Enter roll number to search: ");
    scanf("%d", &target_roll);

    list *curr = head;
    while (curr != NULL) {
        if (curr->roll_no == target_roll) {
            printf("[+] Found: Roll No: %d | Name: %s | Marks: %d\n\n", curr->roll_no, curr->name, curr->marks);
            return;
        }
        curr = curr->next;
    }
    printf("[-] Roll No %d not found.\n\n", target_roll);
}

void delete_student() {
    if (head == NULL) {
        printf("List is empty.\n\n");
        return;
    }

    int target_roll;
    printf("Enter roll number to delete: ");
    scanf("%d", &target_roll);

    list *curr = head;
    list *prev = NULL;

    if (curr != NULL && curr->roll_no == target_roll) {
        head = curr->next;
        free(curr);
        printf("[+] Deleted successfully!\n\n");
        return;
    }

    while (curr != NULL && curr->roll_no != target_roll) {
        prev = curr;
        curr = curr->next;
    }

    if (curr == NULL) {
        printf("[-] Roll No %d not found.\n\n", target_roll);
        return;
    }

    prev->next = curr->next;
    free(curr);
    printf("[+] Deleted successfully!\n\n");
}

int main() {
    int choice;

    while (1) {
        printf("1. Insert\n2. Display\n3. Search\n4. Delete\n5. Exit\n");
        printf("Choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                insert();
                break;
            case 2:
                display();
                break;
            case 3:
                search();
                break;
            case 4:
                delete_student();
                break;
            case 5: {
                list *curr = head;
                while (curr != NULL) {
                    list *next_node = curr->next;
                    free(curr);
                    curr = next_node;
                }
                return 0;
            }
            default:
                printf("Invalid choice.\n\n");
        }
    }

    return 0;
}
