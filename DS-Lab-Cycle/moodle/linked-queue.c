#include <stdio.h>
#include <stdlib.h>

struct student {
    char name[50];
    int roll_no;
    int marks;
    struct student *next;
};

typedef struct student node;

node *front = NULL;
node *rear = NULL;

void enqueue() {
    node *temp = (node *)malloc(sizeof(node));
    if (temp == NULL) {
        printf("Memory allocation failed!\n\n");
        return;
    }

    printf("Enter name: ");
    scanf(" %s", temp->name);

    printf("Enter roll no: ");
    scanf("%d", &temp->roll_no);

    printf("Enter marks: ");
    scanf("%d", &temp->marks);

    temp->next = NULL;

    if (rear == NULL) {
        front = rear = temp;
    } else {
        rear->next = temp;
        rear = temp; 
    }

    printf("[+] Enqueued successfully!\n\n");
}

void dequeue() {
    if (front == NULL) {
        printf("[-] Queue Underflow! No records to dequeue.\n\n");
        return;
    }

    node *temp = front;
    printf("[+] Dequeued: Roll No: %d | Name: %s | Marks: %d\n\n", 
           temp->roll_no, temp->name, temp->marks);

    front = front->next;

    if (front == NULL) {
        rear = NULL;
    }

    free(temp);
}

void display() {
    if (front == NULL) {
        printf("[-] Queue is empty.\n\n");
        return;
    }

    node *curr = front;
    printf("\n--- Student Queue ---\n");
    while (curr != NULL) {
        printf("Roll No: %d | Name: %s | Marks: %d\n", 
               curr->roll_no, curr->name, curr->marks);
        curr = curr->next;
    }
}

int main() {
    int choice;

    while (1) {
        printf("1. Enqueue\n");
        printf("2. Dequeue\n");
        printf("3. Display Queue\n");
        printf("4. Exit\n");
        printf("Choice: ");

        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting...\n");
            break;
        }

        switch (choice) {
            case 1:
                enqueue();
                break;
            case 2:
                dequeue();
                break;
            case 3:
                display();
                break;
            case 4: {
                // Free any remaining nodes on exit
                node *curr = front;
                while (curr != NULL) {
                    node *next_node = curr->next;
                    free(curr);
                    curr = next_node;
                }
                front = rear = NULL;
                printf("Exiting program...\n");
                return 0;
            }
            default:
                printf("Invalid choice!\n\n");
        }
    }

    return 0;
}
