#include <stdio.h>

#define MAX 10

void readMatrix(int mat[MAX][MAX], int rows, int cols)
{
    int i, j;

    for(i = 0; i < rows; i++)
    {
        for(j = 0; j < cols; j++)
        {
            scanf("%d", &mat[i][j]);
        }
    }
}

int convertToSparse(int mat[MAX][MAX], int rows, int cols, int sparse[MAX*MAX][3])
{
    int i, j;
    int k = 1;

    sparse[0][0] = rows;
    sparse[0][1] = cols;
    sparse[0][2] = 0;

    for(i = 0; i < rows; i++)
    {
        for(j = 0; j < cols; j++)
        {
            if(mat[i][j] != 0)
            {
                sparse[k][0] = i;
                sparse[k][1] = j;
                sparse[k][2] = mat[i][j];

                k++;
                sparse[0][2]++;
            }
        }
    }

    return k;
}

void addMatrices(int a[MAX][MAX], int b[MAX][MAX], int result[MAX][MAX], int rows, int cols)
{
    int i, j;

    for(i = 0; i < rows; i++)
    {
        for(j = 0; j < cols; j++)
        {
            result[i][j] = a[i][j] + b[i][j];
        }
    }
}

void displaySparse(int sparse[MAX*MAX][3], int size)
{
    int i;

    printf("\nTriplet Representation\n");

    for(i = 0; i < size; i++)
    {
        printf("%d\t%d\t%d\n",
               sparse[i][0],
               sparse[i][1],
               sparse[i][2]);
    }
}

void displayMatrix(int mat[MAX][MAX], int rows, int cols)
{
    int i, j;

    printf("\nMatrix\n");

    for(i = 0; i < rows; i++)
    {
        for(j = 0; j < cols; j++)
        {
            printf("%d ", mat[i][j]);
        }

        printf("\n");
    }
}

int main()
{
    int rows, cols;
    int a[MAX][MAX], b[MAX][MAX], result[MAX][MAX];
    int sparse1[MAX * MAX][3];
    int sparse2[MAX * MAX][3];
    int sparseResult[MAX * MAX][3];

    int size1, size2, sizeResult;

    printf("Enter number of rows and columns: ");
    scanf("%d%d", &rows, &cols);

    printf("\nEnter first matrix:\n");
    readMatrix(a, rows, cols);

    printf("\nEnter second matrix:\n");
    readMatrix(b, rows, cols);

    size1 = convertToSparse(a, rows, cols, sparse1);
    size2 = convertToSparse(b, rows, cols, sparse2);

    addMatrices(a, b, result, rows, cols);

    sizeResult = convertToSparse(result, rows, cols, sparseResult);

    printf("\nFirst Matrix in Triplet Form:\n");
    displaySparse(sparse1, size1);

    printf("\nSecond Matrix in Triplet Form:\n");
    displaySparse(sparse2, size2);

    printf("\nResultant Triplet:\n");
    displaySparse(sparseResult, sizeResult);

    printf("\nResultant Sparse Matrix:\n");
    displayMatrix(result, rows, cols);

    return 0;
}
