#include <stdio.h>

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

    if (count < 0 || count > MAX_TERMS / 2)
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

void sort_elements(Element elements[], int count)
{
    int i;
    int j;
    Element temporary;

    for (i = 0; i < count - 1; i++)
    {
        for (j = 0; j < count - i - 1; j++)
        {
            if (elements[j].row > elements[j + 1].row ||
                (elements[j].row == elements[j + 1].row &&
                 elements[j].column > elements[j + 1].column))
            {
                temporary = elements[j];
                elements[j] = elements[j + 1];
                elements[j + 1] = temporary;
            }
        }
    }
}

void combine_elements(Element elements[], int *count)
{
    int i;
    int j;
    int k;

    sort_elements(elements, *count);

    for (i = 0; i < *count; i++)
    {
        j = i + 1;

        while (j < *count)
        {
            if (elements[i].row == elements[j].row &&
                elements[i].column == elements[j].column)
            {
                elements[i].value += elements[j].value;

                for (k = j; k < *count - 1; k++)
                {
                    elements[k] = elements[k + 1];
                }

                (*count)--;
            }
            else
            {
                j++;
            }
        }
    }

    i = 0;

    while (i < *count)
    {
        if (elements[i].value == 0)
        {
            for (k = i; k < *count - 1; k++)
            {
                elements[k] = elements[k + 1];
            }

            (*count)--;
        }
        else
        {
            i++;
        }
    }
}

int add_sparse(Element first[], int first_count,
               Element second[], int second_count,
               Element result[])
{
    int i;
    int count = 0;

    for (i = 0; i < first_count; i++)
    {
        result[count] = first[i];
        count++;
    }

    for (i = 0; i < second_count; i++)
    {
        result[count] = second[i];
        count++;
    }

    combine_elements(result, &count);

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

int main(void)
{
    Element first[MAX_TERMS / 2];
    Element second[MAX_TERMS / 2];
    Element result[MAX_TERMS];
    int first_rows;
    int first_columns;
    int second_rows;
    int second_columns;
    int first_count;
    int second_count;
    int result_count;

    printf("First sparse matrix:\n");
    first_count = read_sparse(first, &first_rows, &first_columns);

    printf("Second sparse matrix:\n");
    second_count = read_sparse(second, &second_rows, &second_columns);

    if (first_count < 0 || second_count < 0)
    {
        return 0;
    }

    if (first_rows != second_rows || first_columns != second_columns)
    {
        printf("Matrix dimensions do not match.\n");
        return 0;
    }

    result_count = add_sparse(first, first_count, second, second_count, result);

    printf("Sum in triplet form:\n");
    display_triplets(result, result_count);

    return 0;
}
