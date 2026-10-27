#include <stdio.h>

#define MAX 10
#define MAX_TERMS 100

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

    if (count < 0 || count > MAX_TERMS)
    {
        printf("Invalid number of elements.\n");
        return -1;
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

void to_dense(Element elements[], int count, int matrix[MAX][MAX])
{
    int i;
    int j;

    for (i = 0; i < MAX; i++)
    {
        for (j = 0; j < MAX; j++)
        {
            matrix[i][j] = 0;
        }
    }

    for (i = 0; i < count; i++)
    {
        matrix[elements[i].row][elements[i].column] = elements[i].value;
    }
}

int to_sparse(int matrix[MAX][MAX], int rows, int columns, Element result[])
{
    int i;
    int j;
    int count = 0;

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            if (matrix[i][j] != 0)
            {
                result[count].row = i;
                result[count].column = j;
                result[count].value = matrix[i][j];
                count++;
            }
        }
    }

    return count;
}

void display_dense(int matrix[MAX][MAX], int rows, int columns)
{
    int i;
    int j;

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
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

int main(void)
{
    Element first[MAX_TERMS];
    Element second[MAX_TERMS];
    Element result[MAX_TERMS];
    int first_dense[MAX][MAX];
    int second_dense[MAX][MAX];
    int product[MAX][MAX];
    int first_rows;
    int first_columns;
    int second_rows;
    int second_columns;
    int first_count;
    int second_count;
    int result_count;
    int i;
    int j;
    int k;

    printf("First sparse matrix:\n");
    first_count = read_sparse(first, &first_rows, &first_columns);

    printf("Second sparse matrix:\n");
    second_count = read_sparse(second, &second_rows, &second_columns);

    if (first_count < 0 || second_count < 0)
    {
        return 0;
    }

    if (first_columns != second_rows)
    {
        printf("Matrix multiplication is not possible.\n");
        return 0;
    }

    to_dense(first, first_count, first_dense);
    to_dense(second, second_count, second_dense);

    for (i = 0; i < first_rows; i++)
    {
        for (j = 0; j < second_columns; j++)
        {
            product[i][j] = 0;

            for (k = 0; k < first_columns; k++)
            {
                product[i][j] += first_dense[i][k] * second_dense[k][j];
            }
        }
    }

    printf("Product in full form:\n");
    display_dense(product, first_rows, second_columns);

    result_count = to_sparse(product, first_rows, second_columns, result);

    printf("Product in triplet form:\n");
    display_triplets(result, result_count);

    return 0;
}
