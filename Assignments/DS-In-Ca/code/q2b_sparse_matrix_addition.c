#include <stdio.h>

#define MAX 100

void readSparseMatrix(int sparse[][3], int rows, int cols) {
    int count = 0;
    int value;
    printf("Enter elements of matrix (%dx%d):\n", rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &value);
            if (value != 0) {
                sparse[++count][0] = i;
                sparse[count][1] = j;
                sparse[count][2] = value;
            }
        }
    }
    sparse[0][0] = rows;
    sparse[0][1] = cols;
    sparse[0][2] = count;
}

void addSparseMatrices(int sparse1[][3], int sparse2[][3], int result[][3]) {
    int rows1 = sparse1[0][0], cols1 = sparse1[0][1], count1 = sparse1[0][2];
    int rows2 = sparse2[0][0], cols2 = sparse2[0][1], count2 = sparse2[0][2];

    if (rows1 != rows2 || cols1 != cols2) {
        printf("Matrices dimensions do not match for addition.\n");
        result[0][2] = -1;
        return;
    }

    result[0][0] = rows1;
    result[0][1] = cols1;
    int k = 0;
    int i = 1, j = 1;

    while (i <= count1 && j <= count2) {
        if (sparse1[i][0] < sparse2[j][0] ||
            (sparse1[i][0] == sparse2[j][0] && sparse1[i][1] < sparse2[j][1])) {
            result[++k][0] = sparse1[i][0];
            result[k][1] = sparse1[i][1];
            result[k][2] = sparse1[i][2];
            i++;
        } else if (sparse1[i][0] > sparse2[j][0] ||
                   (sparse1[i][0] == sparse2[j][0] && sparse1[i][1] > sparse2[j][1])) {
            result[++k][0] = sparse2[j][0];
            result[k][1] = sparse2[j][1];
            result[k][2] = sparse2[j][2];
            j++;
        } else {
            int sum = sparse1[i][2] + sparse2[j][2];
            if (sum != 0) {
                result[++k][0] = sparse1[i][0];
                result[k][1] = sparse1[i][1];
                result[k][2] = sum;
            }
            i++;
            j++;
        }
    }

    while (i <= count1) {
        result[++k][0] = sparse1[i][0];
        result[k][1] = sparse1[i][1];
        result[k][2] = sparse1[i][2];
        i++;
    }

    while (j <= count2) {
        result[++k][0] = sparse2[j][0];
        result[k][1] = sparse2[j][1];
        result[k][2] = sparse2[j][2];
        j++;
    }

    result[0][2] = k;
}

void printSparseMatrix(int sparse[][3]) {
    if (sparse[0][2] == -1) return;
    printf("Row\tCol\tValue\n");
    for (int i = 1; i <= sparse[0][2]; i++) {
        printf("%d\t%d\t%d\n", sparse[i][0], sparse[i][1], sparse[i][2]);
    }
}

int main() {
    int rows, cols;
    int sparse1[MAX][3], sparse2[MAX][3], result[MAX][3];

    printf("Enter rows and columns: ");
    scanf("%d %d", &rows, &cols);

    printf("\n--- First Sparse Matrix ---\n");
    readSparseMatrix(sparse1, rows, cols);

    printf("\n--- Second Sparse Matrix ---\n");
    readSparseMatrix(sparse2, rows, cols);

    addSparseMatrices(sparse1, sparse2, result);

    printf("\n--- Resultant Sparse Matrix (Sum) ---\n");
    printSparseMatrix(result);

    return 0;
}