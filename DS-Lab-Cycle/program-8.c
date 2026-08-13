#include <stdio.h>

#define MAX 3

void read_matrix(int matrix[][MAX], int rows, int columns)
{
    int i;
    int j;

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            printf("Enter element at row %d, column %d: ", i + 1, j + 1);
            scanf("%d", &matrix[i][j]);
        }
    }
}

void display_matrix(int matrix[][MAX], int rows, int columns)
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

void add_matrices()
{
    int first[MAX][MAX];
    int second[MAX][MAX];
    int result[MAX][MAX];
    int rows;
    int columns;
    int i;
    int j;

    printf("Enter rows and columns (maximum %d): ", MAX);
    scanf("%d %d", &rows, &columns);
    if (rows < 1 || rows > MAX || columns < 1 || columns > MAX)
    {
        printf("Invalid matrix size.\n");
        return;
    }

    printf("Enter the first matrix:\n");
    read_matrix(first, rows, columns);
    printf("Enter the second matrix:\n");
    read_matrix(second, rows, columns);

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            result[i][j] = first[i][j] + second[i][j];
        }
    }

    printf("Sum of the matrices:\n");
    display_matrix(result, rows, columns);
}

void subtract_matrices(void)
{
    int first[MAX][MAX];
    int second[MAX][MAX];
    int result[MAX][MAX];
    int rows;
    int columns;
    int i;
    int j;

    printf("Enter rows and columns (maximum %d): ", MAX);
    scanf("%d %d", &rows, &columns);
    if (rows < 1 || rows > MAX || columns < 1 || columns > MAX)
    {
        printf("Invalid matrix size.\n");
        return;
    }

    printf("Enter the first matrix:\n");
    read_matrix(first, rows, columns);
    printf("Enter the second matrix:\n");
    read_matrix(second, rows, columns);

    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < columns; j++)
        {
            result[i][j] = first[i][j] - second[i][j];
        }
    }

    printf("First matrix minus second matrix:\n");
    display_matrix(result, rows, columns);
}

void multiply_matrices(void)
{
    int first[MAX][MAX];
    int second[MAX][MAX];
    int result[MAX][MAX];
    int first_rows;
    int first_columns;
    int second_rows;
    int second_columns;
    int i;
    int j;
    int k;

    printf("Enter rows and columns of the first matrix: ");
    scanf("%d %d", &first_rows, &first_columns);
    printf("Enter rows and columns of the second matrix: ");
    scanf("%d %d", &second_rows, &second_columns);

    if (first_rows < 1 || first_rows > MAX || first_columns < 1 ||
        first_columns > MAX || second_rows < 1 || second_rows > MAX ||
        second_columns < 1 || second_columns > MAX)
    {
        printf("Invalid matrix size.\n");
        return;
    }

    if (first_columns != second_rows)
    {
        printf("Matrix multiplication is not possible.\n");
        return;
    }

    printf("Enter the first matrix:\n");
    read_matrix(first, first_rows, first_columns);
    printf("Enter the second matrix:\n");
    read_matrix(second, second_rows, second_columns);

    for (i = 0; i < first_rows; i++)
    {
        for (j = 0; j < second_columns; j++)
        {
            result[i][j] = 0;
            for (k = 0; k < first_columns; k++)
            {
                result[i][j] = result[i][j] +
                               first[i][k] * second[k][j];
            }
        }
    }

    printf("Product of the matrices:\n");
    display_matrix(result, first_rows, second_columns);
}

void transpose_matrix(void)
{
    int matrix[MAX][MAX];
    int rows;
    int columns;
    int i;
    int j;

    printf("Enter rows and columns (maximum %d): ", MAX);
    scanf("%d %d", &rows, &columns);
    if (rows < 1 || rows > MAX || columns < 1 || columns > MAX)
    {
        printf("Invalid matrix size.\n");
        return;
    }

    read_matrix(matrix, rows, columns);

    printf("Transpose of the matrix:\n");
    for (i = 0; i < columns; i++)
    {
        for (j = 0; j < rows; j++)
        {
            printf("%d ", matrix[j][i]);
        }
        printf("\n");
    }
}

void find_determinant(void)
{
    int matrix[MAX][MAX];
    int order;
    int determinant;

    printf("Enter the order of the matrix (2 or 3): ");
    scanf("%d", &order);
    if (order != 2 && order != 3)
    {
        printf("Only 2x2 and 3x3 matrices are supported.\n");
        return;
    }

    read_matrix(matrix, order, order);

    if (order == 2)
    {
        determinant = matrix[0][0] * matrix[1][1] -
                      matrix[0][1] * matrix[1][0];
    }
    else
    {
        determinant = matrix[0][0] *
                          (matrix[1][1] * matrix[2][2] -
                           matrix[1][2] * matrix[2][1]) -
                      matrix[0][1] *
                          (matrix[1][0] * matrix[2][2] -
                           matrix[1][2] * matrix[2][0]) +
                      matrix[0][2] *
                          (matrix[1][0] * matrix[2][1] -
                           matrix[1][1] * matrix[2][0]);
    }

    printf("Determinant = %d\n", determinant);
}

int main(void)
{
    int choice;

    do
    {
        printf("\n1. Add two matrices\n");
        printf("2. Subtract two matrices\n");
        printf("3. Multiply two matrices\n");
        printf("4. Transpose a matrix\n");
        printf("5. Find determinant\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
            case 1:
                add_matrices();
                break;
            case 2:
                subtract_matrices();
                break;
            case 3:
                multiply_matrices();
                break;
            case 4:
                transpose_matrix();
                break;
            case 5:
                find_determinant();
                break;
            case 6:
                printf("Program ended.\n");
                break;
            default:
                printf("Invalid choice.\n");
        }
    } while (choice != 6);

    return 0;
}
