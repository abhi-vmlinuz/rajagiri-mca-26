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

void preorder_iterative(Node *root)
{
    Node *stack[MAX];
    int top = -1;
    Node *current;

    if (root != NULL)
    {
        top++;
        stack[top] = root;
    }

    while (top != -1)
    {
        current = stack[top];
        top--;

        printf("%d ", current->data);

        if (current->right != NULL)
        {
            top++;
            stack[top] = current->right;
        }

        if (current->left != NULL)
        {
            top++;
            stack[top] = current->left;
        }
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

    printf("Preorder without recursion: ");
    preorder_iterative(root);
    printf("\n");

    free_tree(root);

    return 0;
}
