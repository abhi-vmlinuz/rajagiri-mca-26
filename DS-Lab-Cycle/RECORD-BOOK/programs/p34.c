#include <stdio.h>
#include <stdlib.h>

#define MAX_LENGTH 50

typedef struct
{
    char author_name[MAX_LENGTH];
    char book_name[MAX_LENGTH];
} Book;

void read_books(Book *books, int count)
{
    int i;

    for (i = 0; i < count; i++)
    {
        printf("Book %d\n", i + 1);
        printf("Enter author name: ");
        scanf(" %49[^\n]", books[i].author_name);
        printf("Enter book name: ");
        scanf(" %49[^\n]", books[i].book_name);
    }
}

void display_books(Book *books, int count)
{
    int i;

    printf("%-25s %-25s\n", "Author", "Book");

    for (i = 0; i < count; i++)
    {
        printf("%-25s %-25s\n",
               (books + i)->author_name,
               (books + i)->book_name);
    }
}

int main(void)
{
    Book *books;
    int count;

    printf("Enter the number of books: ");
    scanf("%d", &count);

    if (count < 1)
    {
        printf("Invalid number of books.\n");
        return 0;
    }

    books = malloc(count * sizeof(Book));

    if (books == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    read_books(books, count);
    display_books(books, count);

    free(books);

    return 0;
}
