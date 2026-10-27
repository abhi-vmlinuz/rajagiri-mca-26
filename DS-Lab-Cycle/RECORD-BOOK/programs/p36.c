#include <stdio.h>

#define MAX 10
#define MAX_TERMS 50

typedef struct
{
    int row;
    int column;
    int value;
} Element;

int read_sparse(Element elements[], int *rows, int *columns)
{
    int count;
    int i;

    printf("Enter the number of rows and columns: ");
    scanf("%d %d", rows, columns);

    printf("Enter the number of non-zero elements: ");
    scanf("%d", &count);

    if (count < 1 || count > MAX_TERMS)
    {
        printf("Invalid number of elements.\n");
        return 0;
    }

    for (i = 0; i < count; i++)
    {
        printf("Element %d (row column value): ", i + 1);
        scanf("%d %d %d",
              &elements[i].row,
              &elements[i].column,
              &elements[i].value);
    }

    return count;
}

void display_triplets(Element elements[], int count)
{
    int i;

    printf("%-6s %-8s %-6s\n", "Row", "Column", "Value");

    for (i = 0; i < count; i++)
    {
        printf("%-6d %-8d %-6d\n",
               elements[i].row,
               elements[i].column,
               elements[i].value);
    }
}

void display_matrix(Element elements[], int count, int rows, int columns)
{
    int matrix[MAX][MAX] = {0};
    int i;
    int j;

    for (i = 0; i < count; i++)
    {
        matrix[elements[i].row][elements[i].column] = elements[i].value;
    }

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main(void)
{
    Element elements[MAX_TERMS];
    int rows;
    int columns;
    int count;

    count = read_sparse(elements, &rows, &columns);

    if (count == 0)
    {
        return 0;
    }

    printf("Sparse matrix in triplet form:\n");
    display_triplets(elements, count);

    printf("Sparse matrix in full form:\n");
    display_matrix(elements, count, rows, columns);

    return 0;
}
