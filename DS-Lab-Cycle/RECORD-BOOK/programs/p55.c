#include <stdio.h>
#include <stdlib.h>

#define MAX 100

typedef struct Node
{
    int data;
    struct Node *left;
    struct Node *right;
} Node;

Node *create_node(int value)
{
    Node *node = malloc(sizeof(Node));

    if (node == NULL)
    {
        printf("Memory allocation failed.\n");
        return NULL;
    }

    node->data = value;
    node->left = NULL;
    node->right = NULL;

    return node;
}

Node *insert(Node *root, int value)
{
    if (root == NULL)
    {
        return create_node(value);
    }

    if (value < root->data)
    {
        root->left = insert(root->left, value);
    }
    else if (value > root->data)
    {
        root->right = insert(root->right, value);
    }

    return root;
}

void postorder_iterative(Node *root)
{
    Node *first[MAX];
    Node *second[MAX];
    int first_top = -1;
    int second_top = -1;
    Node *current;

    if (root != NULL)
    {
        first_top++;
        first[first_top] = root;
    }

    while (first_top != -1)
    {
        current = first[first_top];
        first_top--;

        second_top++;
        second[second_top] = current;

        if (current->left != NULL)
        {
            first_top++;
            first[first_top] = current->left;
        }

        if (current->right != NULL)
        {
            first_top++;
            first[first_top] = current->right;
        }
    }

    while (second_top != -1)
    {
        printf("%d ", second[second_top]->data);
        second_top--;
    }
}

void free_tree(Node *root)
{
    if (root == NULL)
    {
        return;
    }

    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main(void)
{
    Node *root = NULL;

    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 70);
    root = insert(root, 20);
    root = insert(root, 40);
    root = insert(root, 60);
    root = insert(root, 80);

    printf("Postorder without recursion: ");
    postorder_iterative(root);
    printf("\n");

    free_tree(root);

    return 0;
}
